import joblib
import numpy as np
import time
import urllib.parse

from concurrent.futures import ThreadPoolExecutor
from config.settings import FROZEN_MODEL_PATH

from services.feature_pipeline import FeaturePipeline
from services.logger import logger

from services.whois_service import WHOISService
from services.ssl_service import SSLService
from services.redirect_service import RedirectService
from services.risk_engine import RiskEngine
from services.virustotal_service import VirusTotalService
from services.explainability_service import ExplainabilityService
from services.forensic_engine import ForensicEngine

class PredictionService:

    def __init__(self):

        self.pipeline = FeaturePipeline()

        self.model = joblib.load(
            FROZEN_MODEL_PATH
        )
        self.executor = ThreadPoolExecutor(max_workers=4)

        self.whois = WHOISService()
        self.ssl = SSLService()
        self.redirect = RedirectService()
        self.risk_engine = RiskEngine()
        self.virustotal = VirusTotalService()
        self.explainability = ExplainabilityService()
        self.forensic_engine = ForensicEngine()

        logger.info("PhishShield AI - Prediction Service Initialized")
        logger.info(f"Model loaded: {type(self.model).__name__}")
        logger.info(f"Features loaded: {len(self.pipeline.feature_names)}")

    def predict(self, url):

        overall_start = time.perf_counter()

        parsed_url = urllib.parse.urlparse(url)
        safe_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
        logger.info(f"Scanning URL: {safe_url}")

        # =====================================================
        # 1. FEATURE PIPELINE
        # =====================================================

        pipeline_start = time.perf_counter()

        vector = self.pipeline.build_vector(url)

        pipeline_time = round(
            (time.perf_counter() - pipeline_start) * 1000,
            2
        )

        logger.info(f"Feature Pipeline : {pipeline_time} ms")

        # =====================================================
        # 2. ML PREDICTION
        # =====================================================

        ml_start = time.perf_counter()

        probability = self.model.predict_proba(vector)[0]
        
        # P(class=1) is the phishing probability
        classes = self.model.classes_
        class_1_index = list(classes).index(1)
        phishing_probability = float(probability[class_1_index])

        # Apply threshold 0.5 explicitly
        prediction = 1 if phishing_probability >= 0.5 else 0

        ml_time = round(
            (time.perf_counter() - ml_start) * 1000,
            2
        )

        logger.info(f"ML Prediction : {ml_time} ms")

        # -----------------------------------------------------
        # Get probability belonging to the predicted class
        # -----------------------------------------------------

        prediction_probability = phishing_probability if prediction == 1 else float(probability[list(classes).index(0)])

        confidence = float(
            round(
                prediction_probability * 100,
                2
            )
        )

        logger.info(f"ML RESULT: Prediction={prediction} ({'Legitimate' if prediction == 0 else 'Phishing'}), Confidence={confidence}%")

        # =====================================================
        # 3. EXTERNAL INTELLIGENCE SERVICES
        # =====================================================

        network_start = time.perf_counter()

        whois_future = self.executor.submit(self.whois.get_domain_info, url)
        ssl_future = self.executor.submit(self.ssl.get_ssl_info, url)
        redirect_future = self.executor.submit(self.redirect.analyze, url)
        vt_future = self.executor.submit(self.virustotal.analyze, url)

        try:
            whois_info = whois_future.result()
        except Exception as e:
            logger.error(f"WHOIS service failed: {e}")
            whois_info = {}

        try:
            ssl_info = ssl_future.result()
        except Exception as e:
            logger.error(f"SSL service failed: {e}")
            ssl_info = {"ssl_valid": False, "error": "Service unavailable"}

        try:
            redirect_info = redirect_future.result()
        except Exception as e:
            logger.error(f"Redirect service failed: {e}")
            redirect_info = {"redirected": False, "redirect_count": 0, "redirect_chain": [], "protocol_changed": False, "domain_changed": False, "uses_shortener": False}

        try:
            vt_info = vt_future.result()
        except Exception as e:
            logger.error(f"VirusTotal service failed: {e}")
            vt_info = {"error": "Service unavailable"}

        network_time = round(
            (time.perf_counter() - network_start) * 1000,
            2
        )

        logger.info(f"Network Services : {network_time} ms")



        # =====================================================
        # 5. RISK ENGINE
        # =====================================================

        risk_start = time.perf_counter()

        risk_score = self.risk_engine.calculate(

            prediction=prediction,

            confidence=confidence,

            whois=whois_info,

            ssl=ssl_info,

            redirect=redirect_info,

            virustotal=vt_info
        )

        risk_time = round(
            (time.perf_counter() - risk_start) * 1000,
            2
        )

        logger.info(f"Risk Engine : {risk_time} ms")

        # =====================================================
        # 6. EXPLAINABILITY
        # =====================================================

        explainability_start = time.perf_counter()
        
        # Verify prediction integrity is maintained
        explainability = self.explainability.generate_explanation(
            model=self.model,
            feature_names=self.pipeline.feature_names,
            feature_vector=vector,
            existing_whois_info=whois_info,
            existing_ssl_info=ssl_info,
            existing_redirect_info=redirect_info,
            existing_virustotal_info=vt_info
        )

        # =====================================================
        # 7. FORENSIC ENGINE
        # =====================================================
        
        forensic_start = time.perf_counter()

        forensic_report = self.forensic_engine.generate_findings(
            feature_vector=vector,
            whois=whois_info,
            ssl=ssl_info,
            redirect=redirect_info,
            virustotal=vt_info
        )

        forensic_time = round((time.perf_counter() - forensic_start) * 1000, 2)
        logger.info(f"Forensic Engine : {forensic_time} ms")

        # =====================================================
        # 8. LOGGING
        # =====================================================

        logger.info(
            f"Prediction={prediction}, "
            f"Confidence={confidence}, "
            f"RiskScore={risk_score}"
        )

        # =====================================================
        # 9. TOTAL PROCESSING TIME
        # =====================================================

        overall_time = round(
            (time.perf_counter() - overall_start) * 1000,
            2
        )

        logger.info(f"Total Backend Time : {overall_time} ms")

        # =====================================================
        # 10. RETURN RESULT
        # =====================================================

        return {

            "prediction": prediction,

            "confidence": confidence,

            "risk_score": risk_score,

            "whois": whois_info,

            "ssl": ssl_info,

            "redirect": redirect_info,

            "virustotal": vt_info,
            
            "explainability": explainability,
            
            "forensic_report": forensic_report
        }