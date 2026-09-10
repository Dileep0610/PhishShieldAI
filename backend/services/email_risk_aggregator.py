from typing import List, Dict, Any, Tuple

def aggregate_email_risk(email_prediction: str, decision_score: float, url_analysis: List[Dict[str, Any]]) -> Dict[str, str]:
    """
    Deterministically aggregates email and URL signals into an overall risk assessment.
    """
    
    url_severities = {
        "Very Safe": 0,
        "Safe": 1,
        "Suspicious": 2,
        "High Risk": 3,
        "Very High Risk": 4
    }
    
    # Filter out failed analyses
    valid_urls = [u for u in url_analysis if u.get("risk_level") in url_severities]
    
    has_urls = len(url_analysis) > 0
    has_valid_urls = len(valid_urls) > 0
    
    if has_valid_urls:
        # Step 6: Highest-risk URL controls URL severity
        highest_risk_url = max(valid_urls, key=lambda u: url_severities[u["risk_level"]])
        max_url_level = highest_risk_url["risk_level"]
        max_url_severity = url_severities[max_url_level]
    else:
        max_url_severity = -1
        max_url_level = None

    overall_prediction = email_prediction
    overall_risk_level = "Unknown"
    primary_reason = ""
    
    # Step 4: No URL emails or all URLs failed
    if not has_valid_urls:
        if email_prediction == "Phishing":
            overall_risk_level = "High Risk"
            overall_prediction = "Phishing"
            primary_reason = "The email content was classified as phishing."
        else:
            overall_risk_level = "Safe"
            overall_prediction = "Legitimate"
            if has_urls:
                primary_reason = "The email content appears legitimate, but embedded URLs could not be analyzed."
            else:
                primary_reason = "The email content appears legitimate and no suspicious URLs were detected."
                
        return {
            "overall_prediction": overall_prediction,
            "overall_risk_level": overall_risk_level,
            "primary_reason": primary_reason
        }

    # Step 5: Combine Email + URL Signals
    if email_prediction == "Legitimate":
        if max_url_severity <= 1:
            # Case A: Legitimate + Safe URL
            overall_risk_level = "Safe"
            overall_prediction = "Legitimate"
            primary_reason = "The email and its links appear safe."
        elif max_url_severity == 2:
            # Case B: Legitimate + Suspicious URL
            overall_risk_level = "Suspicious"
            overall_prediction = "Legitimate"
            primary_reason = "The email contains a suspicious link."
        else:
            # Case C: Legitimate + High Risk URL
            overall_risk_level = max_url_level # "High Risk" or "Very High Risk"
            overall_prediction = "Phishing"
            primary_reason = "The email contains a high-risk URL."
    else:
        # Email = Phishing
        overall_prediction = "Phishing"
        if max_url_severity <= 1:
            # Case D: Phishing + Safe URL
            overall_risk_level = "High Risk"
            primary_reason = "The email content was classified as phishing despite safe-looking links."
        elif max_url_severity == 2:
            # Case E: Phishing + Suspicious URL
            overall_risk_level = "High Risk"
            primary_reason = "The email content and embedded URL both indicate phishing risk."
        else:
            # Case F: Phishing + High Risk URL
            overall_risk_level = "Very High Risk"
            primary_reason = "The email content is phishing and it contains a highly dangerous URL."
            
    return {
        "overall_prediction": overall_prediction,
        "overall_risk_level": overall_risk_level,
        "primary_reason": primary_reason
    }
