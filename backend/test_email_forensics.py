import pytest
from services.email_forensics import EmailForensicService

@pytest.fixture
def forensics_service():
    return EmailForensicService()

def test_normal_legitimate_email(forensics_service):
    subject = "Project meeting tomorrow"
    body = "Hello team,\n\nThe project meeting is scheduled for tomorrow at 10 AM.\nPlease bring the latest project progress update.\n\nRegards,\nDileep"
    
    result = forensics_service.analyze(subject, body)
    
    assert result["forensic_summary"].indicator_count == 0
    assert len(result["indicators"]) == 0

def test_urgent_account_verification(forensics_service):
    subject = "URGENT: Verify your account immediately"
    body = "Your account requires immediate verification.\nPlease confirm your login credentials to avoid account suspension."
    
    result = forensics_service.analyze(subject, body)
    
    indicators = {i.indicator for i in result["indicators"]}
    assert "urgency_language" in indicators
    assert "credential_request" in indicators
    assert "threat_consequence" in indicators
    assert "suspicious_capitalization" in indicators
    
def test_financial_request(forensics_service):
    subject = "Payment verification required"
    body = "Please verify your bank account and complete the required payment."
    
    result = forensics_service.analyze(subject, body)
    indicators = {i.indicator for i in result["indicators"]}
    assert "financial_request" in indicators
    
def test_prize_reward_scam_pattern(forensics_service):
    subject = "Congratulations! You won a cash prize"
    body = "You have been selected as a winner.\nClick the link to claim your reward."
    
    result = forensics_service.analyze(subject, body)
    indicators = {i.indicator for i in result["indicators"]}
    assert "reward_prize" in indicators
    assert "call_to_action" in indicators
    
def test_suspicious_action_request_and_url(forensics_service):
    subject = "Action required"
    body = "Your account will be suspended.\nClick here to verify your account:\nhttps://example.com/login"
    
    result = forensics_service.analyze(subject, body)
    indicators = {i.indicator for i in result["indicators"]}
    assert "urgency_language" in indicators
    assert "credential_request" in indicators
    assert "call_to_action" in indicators
    assert "threat_consequence" in indicators
    
def test_benign_security_discussion(forensics_service):
    subject = "Security training discussion"
    body = "Today we discussed how phishing emails can request passwords,\nOTP codes, or account information. This was only a security\nawareness training session."
    
    result = forensics_service.analyze(subject, body)
    assert result["forensic_summary"].indicator_count == 0
    
def test_empty_subject(forensics_service):
    subject = ""
    body = "Hello, please find the project update attached in the email."
    
    result = forensics_service.analyze(subject, body)
    assert result["forensic_summary"].indicator_count == 0
    
def test_long_email(forensics_service):
    subject = "Long email"
    body = "Hello, " * 10000
    
    result = forensics_service.analyze(subject, body)
    assert result["forensic_summary"].indicator_count == 0
