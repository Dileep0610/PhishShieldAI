import warnings
warnings.filterwarnings("ignore")

from services.prediction_service import PredictionService

def run_tests():
    service = PredictionService()
    
    print("\n--- TEST: HTTPS URL ---")
    res1 = service.predict("https://www.google.com")
    print("Prediction:", res1["prediction"])
    print("Risk Score:", res1["risk_score"])
    print("WHOIS:", res1["whois"])
    
    print("\n--- TEST: HTTP URL ---")
    res2 = service.predict("http://example.com")
    print("Prediction:", res2["prediction"])
    print("Risk Score:", res2["risk_score"])
    print("WHOIS:", res2["whois"])

if __name__ == "__main__":
    run_tests()
