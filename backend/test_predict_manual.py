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
    
    print("\n--- TEST: Endpoint with security_report ---")
    from fastapi.testclient import TestClient
    from app import app
    client = TestClient(app)
    res_ep = client.post("/predict", json={"url": "https://www.google.com"})
    assert res_ep.status_code == 200
    data_ep = res_ep.json()
    assert "security_report" in data_ep
    sr = data_ep["security_report"]
    assert sr["analysis_type"] == "url"
    assert sr["verdict"]["prediction"] == data_ep["prediction"]
    assert sr["verdict"]["risk_level"] == data_ep["risk_level"]
    assert sr["verdict"]["recommendation"] == data_ep["recommendation"]
    assert sr["ml_evidence"]["prediction"] == data_ep["prediction"]
    assert sr["ml_evidence"]["confidence"] == data_ep["confidence"]
    if sr["threat_intelligence"]["whois"] != data_ep["whois"]: print("whois mismatch", sr["threat_intelligence"]["whois"], data_ep["whois"])
    if sr["threat_intelligence"]["ssl"] != data_ep["ssl"]: print("ssl mismatch", sr["threat_intelligence"]["ssl"], data_ep["ssl"])
    
    assert sr["threat_intelligence"]["whois"] == data_ep["whois"]
    assert sr["threat_intelligence"]["ssl"] == data_ep["ssl"]
    for k in data_ep["redirect"]:
        assert sr["threat_intelligence"]["redirect"][k] == data_ep["redirect"][k]
    for k in data_ep["virustotal"]:
        assert sr["threat_intelligence"]["virustotal"][k] == data_ep["virustotal"][k]
    print("  -> Endpoint Security Report Validated")

if __name__ == "__main__":
    run_tests()
