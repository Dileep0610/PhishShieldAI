import asyncio
import json
from services.prediction_service import PredictionService

def get_risk_level(risk_score):
    if risk_score <= 15: return "Very Safe"
    elif risk_score <= 30: return "Safe"
    elif risk_score <= 50: return "Suspicious"
    elif risk_score <= 75: return "High Risk"
    else: return "Very High Risk"

def run_tests():
    service = PredictionService()
    urls = [
        "https://www.linkedin.com/in/dileep0610/",
        "https://www.google.com/",
        "https://www.webex.com/",
        "http://paypal.update-account-verify.info",  # standard phishing
        "http://login.microsoftonline.com.borderline-test.com", # borderline
        "https://github.com",
        "https://www.intellipaat.com/",
        "https://docs.github.com",
        "https://accounts.google.com",
        "https://github.com.evil.com",
        "https://evilgithub.com",
        "https://intellipaat.webex.com/intellipaat/j.php?MTID=m87035a45b9c4509f1120ad43fab1a443",
    ]
    
    for url in urls:
        print(f"\n--- Testing URL: {url} ---")
        try:
            result = service.analyze_url(url)
            trust = result.get("trust_assessment", {})
            
            print(f"URL: {url}")
            print(f"ML Prediction: {result['prediction']}")
            print(f"ML Confidence: {result['confidence']}%")
            if trust:
                print(f"Original Risk: {trust.get('original_risk_score', 'N/A')}")
                print(f"Trust Score: {trust.get('trust_score', 'N/A')}")
                print(f"Trust Signals: {', '.join(trust.get('signals', [])) if trust.get('signals') else 'None'}")
                print(f"Veto Status: {trust.get('veto_status', 'N/A')}")
                print(f"Veto Reason: {trust.get('veto_reason') or 'None'}")
                print(f"Risk Adjustment: {trust.get('risk_adjustment', 'N/A')}")
                print(f"Final Risk: {trust.get('final_risk_score', 'N/A')}")
            else:
                print("Trust Assessment missing!")
                print(f"Final Risk: {result['risk_score']}")
            print(f"Final Risk Level: {result['risk_level']}")
        except Exception as e:
            print(f"Error testing {url}: {e}")

if __name__ == "__main__":
    run_tests()
