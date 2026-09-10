from fastapi.testclient import TestClient
from app import app
import json

client = TestClient(app)

def verify_email_security_report(data):
    if "security_report" not in data:
        return
    sr = data["security_report"]
    assert sr["analysis_type"] == "email", f"Expected 'email', got {sr.get('analysis_type')}"
    assert sr["verdict"]["prediction"] == data["overall_prediction"]
    assert sr["verdict"]["risk_level"] == data["overall_risk_level"]
    assert sr["ml_evidence"]["prediction"] == data["prediction"]
    assert sr["ml_evidence"]["decision_score"] == data["decision_score"]
    assert sr["forensic_evidence"]["summary"] == data["forensic_summary"]
    assert sr["forensic_evidence"]["indicators"] == data["forensic_indicators"]
    assert sr["explainability"] == data["explainability"]
    print("  -> Security Report Validated")

def run_tests():
    print("--- CHECKPOINT 12 TESTS ---")

    # Test A: Legitimate
    print("\nTest A - Legitimate:")
    res_a = client.post("/api/analyze-email", json={
        "subject": "Meeting schedule for tomorrow",
        "body": "Hi team, our project meeting is scheduled for tomorrow at 10 AM. Please bring your progress updates."
    })
    print(res_a.status_code)
    data_a = res_a.json()
    print(data_a)
    verify_email_security_report(data_a)

    # Test B: Phishing
    print("\nTest B - Phishing:")
    res_b = client.post("/api/analyze-email", json={
        "subject": "Urgent: Verify your account immediately",
        "body": "Your account has been temporarily restricted. Click the link below and verify your username, password, and security information immediately."
    })
    print(res_b.status_code)
    data_b = res_b.json()
    print(data_b)
    verify_email_security_report(data_b)

    # Test C: Empty subject
    print("\nTest C - Empty subject:")
    res_c = client.post("/api/analyze-email", json={
        "subject": "",
        "body": "Please review the project document and let me know if any changes are required."
    })
    print(res_c.status_code)
    print(res_c.json())

    # Test D: Short email
    print("\nTest D - Short email:")
    res_d = client.post("/api/analyze-email", json={
        "subject": "Hello",
        "body": "How are you?"
    })
    print(res_d.status_code)
    print(res_d.json())
    
    # Empty body test
    print("\nTest E - Empty body:")
    res_e = client.post("/api/analyze-email", json={
        "subject": "Hello",
        "body": "   "
    })
    print(res_e.status_code)
    print(res_e.json())

    # Regression Test: URL Endpoint
    print("\nRegression Test - URL endpoint:")
    res_url = client.post("/predict", json={
        "url": "https://www.google.com"
    })
    print(res_url.status_code)
    if res_url.status_code == 200:
        data = res_url.json()
        print({"prediction": data.get("prediction"), "risk_score": data.get("risk_score")})
    else:
        print(res_url.text)

if __name__ == "__main__":
    run_tests()
