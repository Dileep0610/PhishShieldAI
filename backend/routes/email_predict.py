from fastapi import APIRouter, HTTPException
import time
from services.logger import logger

from schemas.request_models import EmailRequest
from schemas.response_models import EmailPredictionResponse

from services.email_prediction_service import EmailPredictionService
from services.email_url_extractor import extract_urls
from services.prediction_service import PredictionService
from services.email_forensics import EmailForensicService
from services.email_explainability import EmailExplainabilityService

from services.email_risk_aggregator import aggregate_email_risk

router = APIRouter()
email_service = EmailPredictionService()
url_service = PredictionService()
forensics_service = EmailForensicService()
explainability_service = EmailExplainabilityService()

@router.post(
    "/api/analyze-email",
    response_model=EmailPredictionResponse
)
def analyze_email(request: EmailRequest):
    if not request.body or not request.body.strip():
        raise HTTPException(status_code=400, detail="Invalid email body")

    start_time = time.time()

    try:
        # 1. Email NLP Prediction
        result = email_service.predict(request.subject, request.body)
        
        # 1.5 Email Forensics
        forensics_result = forensics_service.analyze(request.subject, request.body)
        
        # 2. Extract URLs
        extracted_urls = extract_urls(request.subject, request.body)
        
        # 3. Analyze each unique URL using existing URL engine
        url_analysis = []
        for url in extracted_urls:
            try:
                analysis = url_service.analyze_url(url)
                url_analysis.append(analysis)
            except Exception as e:
                logger.error(f"URL analysis failed for {url}: {e}")
                # Provide an error fallback so email prediction still succeeds
                fallback = {
                    "url": url,
                    "prediction": "Analysis Failed",
                    "confidence": 0.0,
                    "risk_score": 0.0,
                    "risk_level": "Error",
                    "processing_time_ms": 0.0,
                    "recommendation": "URL analysis failed or timed out.",
                    "whois": {},
                    "ssl": {"ssl_valid": False},
                    "redirect": {"redirected": False, "redirect_count": 0, "redirect_chain": [], "protocol_changed": False, "domain_changed": False, "uses_shortener": False},
                    "virustotal": {"malicious": 0, "suspicious": 0, "harmless": 0, "undetected": 0}
                }
                url_analysis.append(fallback)

        # 4. Aggregate Risk
        aggregated = aggregate_email_risk(
            email_prediction=result["prediction"],
            decision_score=result["decision_score"],
            url_analysis=url_analysis
        )

        # 5. Explainability
        explanation = explainability_service.generate_explanation(
            ml_prediction=result["prediction"],
            ml_decision_score=result["decision_score"],
            forensic_indicators=forensics_result["indicators"],
            url_analysis=url_analysis,
            overall_prediction=aggregated["overall_prediction"],
            overall_risk_level=aggregated["overall_risk_level"]
        )

        elapsed = round((time.time() - start_time) * 1000, 2)
        logger.info(f"Email prediction completed in {elapsed} ms")

        # 6. Build Unified Security Report
        from schemas.response_models import SecurityReport, SecurityVerdict, SecurityMetadata
        
        security_report = SecurityReport(
            analysis_type="email",
            verdict=SecurityVerdict(
                prediction=aggregated["overall_prediction"],
                risk_level=aggregated["overall_risk_level"],
                primary_reason=aggregated["primary_reason"]
            ),
            metadata=SecurityMetadata(
                processing_time_ms=elapsed
            ),
            ml_evidence={"prediction": result["prediction"], "decision_score": result["decision_score"]},
            forensic_evidence={"summary": forensics_result["forensic_summary"], "indicators": forensics_result["indicators"]},
            url_evidence=url_analysis,
            explainability=explanation
        )

        return EmailPredictionResponse(
            prediction=result["prediction"],
            decision_score=result["decision_score"],
            processing_time_ms=elapsed,
            extracted_urls=extracted_urls,
            url_analysis=url_analysis,
            overall_prediction=aggregated["overall_prediction"],
            overall_risk_level=aggregated["overall_risk_level"],
            primary_reason=aggregated["primary_reason"],
            forensic_summary=forensics_result["forensic_summary"],
            forensic_indicators=forensics_result["indicators"],
            explainability=explanation,
            security_report=security_report
        )
    except Exception as e:
        logger.error(f"Email prediction failed: {e}")
        raise HTTPException(
            status_code=500,
            detail="Prediction service temporarily unavailable."
        )
