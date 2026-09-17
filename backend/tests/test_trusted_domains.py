import pytest
from services.risk_engine import RiskEngine
from config.trusted_domains import TRUSTED_DOMAINS

@pytest.fixture
def engine():
    return RiskEngine()

def test_trusted_clean_legitimate(engine):
    # ML predicted phishing (1), but confidence doesn't matter much here
    # Age > 5 years, valid SSL, clean VT, safe redirect
    prediction = 1
    confidence = 80
    whois = {"domain_age_days": 2000}
    ssl = {"ssl_valid": True}
    redirect = {"redirect_count": 0, "domain_changed": False, "uses_shortener": False}
    virustotal = {"malicious": 0, "suspicious": 0, "error": None}
    
    # We pass url="https://github.com" which is in TRUSTED_DOMAINS
    risk, trust = engine.calculate_with_trust(
        prediction, confidence, whois, ssl, redirect, virustotal, url="https://github.com"
    )
    
    assert trust["trusted_legitimate"] is True
    assert trust["veto_status"] is False
    assert risk <= 30

def test_trusted_subdomain_clean(engine):
    whois = {"domain_age_days": 2000}
    ssl = {"ssl_valid": True}
    redirect = {"redirect_count": 0, "domain_changed": False, "uses_shortener": False}
    virustotal = {"malicious": 0, "suspicious": 0, "error": None}
    
    risk, trust = engine.calculate_with_trust(
        1, 80, whois, ssl, redirect, virustotal, url="https://docs.github.com"
    )
    assert trust["trusted_legitimate"] is True
    assert risk <= 30

def test_lookalike_domain(engine):
    whois = {"domain_age_days": 2000}
    ssl = {"ssl_valid": True}
    redirect = {"redirect_count": 0, "domain_changed": False, "uses_shortener": False}
    virustotal = {"malicious": 0, "suspicious": 0, "error": None}
    
    risk, trust = engine.calculate_with_trust(
        1, 80, whois, ssl, redirect, virustotal, url="https://evilgithub.com"
    )
    assert trust["trusted_legitimate"] is False
    # Since it's not trusted legitimate, the risk should be higher than 30 (Suspicious)
    assert risk > 30

def test_lookalike_subdomain(engine):
    whois = {"domain_age_days": 2000}
    ssl = {"ssl_valid": True}
    redirect = {"redirect_count": 0, "domain_changed": False, "uses_shortener": False}
    virustotal = {"malicious": 0, "suspicious": 0, "error": None}
    
    risk, trust = engine.calculate_with_trust(
        1, 80, whois, ssl, redirect, virustotal, url="https://github.com.evil.com"
    )
    assert trust["trusted_legitimate"] is False
    assert risk > 30

def test_trusted_with_malicious_vt(engine):
    whois = {"domain_age_days": 2000}
    ssl = {"ssl_valid": True}
    redirect = {"redirect_count": 0, "domain_changed": False, "uses_shortener": False}
    # Malicious VT data
    virustotal = {"malicious": 1, "suspicious": 0, "error": None}
    
    risk, trust = engine.calculate_with_trust(
        1, 80, whois, ssl, redirect, virustotal, url="https://github.com"
    )
    # Should be vetoed
    assert trust.get("trusted_legitimate", False) is False
    assert trust["veto_status"] is True
    # Risk should remain high
    assert risk > 30

def test_trusted_with_suspicious_redirect(engine):
    whois = {"domain_age_days": 2000}
    ssl = {"ssl_valid": True}
    # Domain changed during redirect
    redirect = {"redirect_count": 1, "domain_changed": True, "uses_shortener": False}
    virustotal = {"malicious": 0, "suspicious": 0, "error": None}
    
    risk, trust = engine.calculate_with_trust(
        1, 80, whois, ssl, redirect, virustotal, url="https://github.com"
    )
    # Should be vetoed
    assert trust.get("trusted_legitimate", False) is False
    assert trust["veto_status"] is True
    assert risk > 30
