from fastapi import APIRouter, HTTPException
import time
import urllib.parse
from services.logger import logger

from schemas.request_models import URLRequest
from schemas.response_models import PredictionResponse

from services.prediction_service import PredictionService


router = APIRouter()

service = PredictionService()


@router.post(
    "/predict",
    response_model=PredictionResponse
)
def predict(request: URLRequest):

    try:
        from utils.url import normalize_url
        url_str = normalize_url(str(request.url))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    start_time = time.time()

    try:

        result = service.analyze_url(url_str)
        
        # Build Unified Security Report
        from schemas.response_models import SecurityReport, SecurityVerdict, SecurityMetadata
        
        security_report = SecurityReport(
            analysis_type="url",
            verdict=SecurityVerdict(
                prediction=result.get("final_security_verdict", result.get("prediction", "")),
                risk_level=result.get("risk_level", ""),
                recommendation=result.get("recommendation", "")
            ),
            metadata=SecurityMetadata(
                processing_time_ms=result.get("processing_time_ms", 0.0)
            ),
            ml_evidence={"prediction": result.get("ml_prediction", result.get("prediction", "")), "confidence": result.get("ml_confidence", result.get("confidence", 0.0))},
            url_evidence={"url": result.get("url", "")},
            threat_intelligence={
                "whois": result.get("whois", {}),
                "ssl": result.get("ssl", {}),
                "redirect": result.get("redirect", {}),
                "virustotal": result.get("virustotal", {})
            },
            trust_assessment=result.get("trust_assessment")
        )
        
        result["security_report"] = security_report

        return PredictionResponse(**result)

    except Exception as e:
        
        logger.error(f"Prediction failed: {e}")

        raise HTTPException(
                                    
            status_code=500,

            detail="Prediction service temporarily unavailable."
        )