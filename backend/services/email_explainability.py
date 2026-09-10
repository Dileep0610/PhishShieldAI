from typing import Dict, Any, List
from schemas.response_models import (
    EmailExplainability,
    EmailMLEvidence,
    EmailURLEvidence,
    EmailForensicFinding
)

class EmailExplainabilityService:
    def generate_explanation(
        self,
        ml_prediction: str,
        ml_decision_score: float,
        forensic_indicators: List[EmailForensicFinding],
        url_analysis: List[Dict[str, Any]],
        overall_prediction: str,
        overall_risk_level: str
    ) -> EmailExplainability:
        
        reasons = []
        
        # 1. Forensic Evidence Reasons
        for indicator in forensic_indicators:
            # Handle both dict and Pydantic model
            if isinstance(indicator, dict):
                reasons.append(indicator.get("description", ""))
            else:
                reasons.append(getattr(indicator, "description", ""))
            
        # 2. URL Evidence Reasons
        url_evidence = []
        highest_risk_level = None
        risk_order = {"Very High Risk": 4, "High Risk": 3, "Suspicious": 2, "Safe": 1, "Very Safe": 0, "Error": -1, "Unknown": -1}
        max_risk_val = -1

        for url_data in url_analysis:
            if isinstance(url_data, dict):
                url_str = url_data.get("url", "")
                url_pred = url_data.get("prediction", "")
                risk_level = url_data.get("risk_level", "Unknown")
            else:
                url_str = getattr(url_data, "url", "")
                url_pred = getattr(url_data, "prediction", "")
                risk_level = getattr(url_data, "risk_level", "Unknown")
                
            url_evidence.append(EmailURLEvidence(
                url=url_str,
                prediction=url_pred,
                risk_level=risk_level
            ))
            
            r_val = risk_order.get(risk_level, -1)
            if r_val > max_risk_val:
                max_risk_val = r_val
                highest_risk_level = risk_level
                
        if max_risk_val >= 2:
            reasons.append(f"The email contains a URL classified as {highest_risk_level}.")
            
        # 3. Formulate Summary
        if overall_prediction == "Legitimate":
            if not reasons:
                reasons.append("No suspicious forensic or URL evidence was detected.")
                summary = "The email was classified as legitimate and no suspicious forensic or URL evidence was detected."
            else:
                summary = "The email was classified as legitimate, though some security indicators were detected."
        else:
            if ml_prediction == "Phishing":
                if not reasons:
                    summary = "The email was classified as phishing based on the ML classification."
                else:
                    summary = "The email was classified as phishing based on the ML classification and supporting security indicators."
            else:
                summary = "The email was classified as phishing due to high-risk embedded URLs."

        return EmailExplainability(
            explanation_summary=summary,
            explanation_reasons=reasons,
            ml_evidence=EmailMLEvidence(
                prediction=ml_prediction,
                decision_score=ml_decision_score
            ),
            forensic_evidence=forensic_indicators,
            url_evidence=url_evidence
        )
