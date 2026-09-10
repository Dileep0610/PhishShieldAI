import pytest
from fastapi.testclient import TestClient
from app import app

@pytest.fixture
def client():
    return TestClient(app)

def test_legitimate_no_indicators(client):
    res = client.post("/api/analyze-email", json={
        "subject": "Project meeting tomorrow",
        "body": "Hello team,\n\nThe project meeting is scheduled for tomorrow at 10 AM.\nPlease bring the latest project progress update.\n\nRegards,\nDileep"
    })
    assert res.status_code == 200
    data = res.json()
    assert data["overall_prediction"] == "Legitimate"
    expl = data.get("explainability")
    assert expl is not None
    assert expl["explanation_summary"] == "The email was classified as legitimate and no suspicious forensic or URL evidence was detected."
    assert "No suspicious forensic or URL evidence was detected." in expl["explanation_reasons"]
    assert len(expl["forensic_evidence"]) == 0
    assert len(expl["url_evidence"]) == 0

def test_phishing_credential_urgency(client):
    res = client.post("/api/analyze-email", json={
        "subject": "URGENT: Verify your account immediately",
        "body": "Your account requires immediate verification.\nPlease confirm your login credentials to avoid account suspension."
    })
    assert res.status_code == 200
    data = res.json()
    expl = data.get("explainability")
    assert expl is not None
    indicators = [f["indicator"] for f in expl["forensic_evidence"]]
    assert "urgency_language" in indicators
    assert "credential_request" in indicators
    
    reason_texts = " ".join(expl["explanation_reasons"])
    assert "Urgent or time-pressure language was detected" in reason_texts
    assert "credential" in reason_texts.lower()

def test_financial_phishing(client):
    res = client.post("/api/analyze-email", json={
        "subject": "Payment verification required",
        "body": "Please verify your bank account and complete the required payment."
    })
    assert res.status_code == 200
    data = res.json()
    expl = data.get("explainability")
    indicators = [f["indicator"] for f in expl["forensic_evidence"]]
    assert "financial_request" in indicators

def test_prize_reward(client):
    res = client.post("/api/analyze-email", json={
        "subject": "Congratulations! You won a cash prize",
        "body": "You have been selected as a winner.\nClick the link to claim your reward."
    })
    assert res.status_code == 200
    data = res.json()
    expl = data.get("explainability")
    indicators = [f["indicator"] for f in expl["forensic_evidence"]]
    assert "reward_prize" in indicators

def test_suspicious_url(client):
    res = client.post("/api/analyze-email", json={
        "subject": "Check this",
        "body": "Look at this link: https://example.com/login"
    })
    assert res.status_code == 200
    data = res.json()
    expl = data.get("explainability")
    assert len(expl["url_evidence"]) > 0
    reason_texts = " ".join(expl["explanation_reasons"])
    assert "URL classified as " in reason_texts

def test_multiple_evidence(client):
    res = client.post("/api/analyze-email", json={
        "subject": "Action required",
        "body": "Your account will be suspended.\nClick here to verify your account:\nhttps://example.com/login"
    })
    assert res.status_code == 200
    data = res.json()
    expl = data.get("explainability")
    indicators = [f["indicator"] for f in expl["forensic_evidence"]]
    assert "urgency_language" in indicators
    assert "credential_request" in indicators
    assert len(expl["url_evidence"]) > 0
    
    # We should have separate ML, forensic, URL evidence
    assert expl["ml_evidence"]["prediction"] in ["Phishing", "Legitimate"]
    reason_texts = " ".join(expl["explanation_reasons"])
    assert "URL classified as" in reason_texts
    assert "credential" in reason_texts.lower()

def test_benign_security_awareness(client):
    res = client.post("/api/analyze-email", json={
        "subject": "Security training discussion",
        "body": "Today we discussed how phishing emails can request passwords,\nOTP codes, or account information. This was only a security\nawareness training session."
    })
    assert res.status_code == 200
    data = res.json()
    expl = data.get("explainability")
    assert len(expl["forensic_evidence"]) == 0

def test_empty_subject(client):
    res = client.post("/api/analyze-email", json={
        "subject": "",
        "body": "Hello, please find the project update attached in the email."
    })
    assert res.status_code == 200
    data = res.json()
    expl = data.get("explainability")
    assert expl is not None

def test_long_email(client):
    res = client.post("/api/analyze-email", json={
        "subject": "Long email",
        "body": "Hello, " * 1000
    })
    assert res.status_code == 200
    data = res.json()
    expl = data.get("explainability")
    assert expl is not None

def test_no_urls(client):
    res = client.post("/api/analyze-email", json={
        "subject": "No URLs here",
        "body": "Just some text without any links."
    })
    assert res.status_code == 200
    data = res.json()
    expl = data.get("explainability")
    assert len(expl["url_evidence"]) == 0
