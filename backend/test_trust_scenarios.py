import json
from services.risk_engine import RiskEngine

engine = RiskEngine()

scenarios = [
    {
        "name": "LinkedIn profile",
        "prediction": 0, "confidence": 99.0,
        "whois": {"domain_age_days": 5000},
        "ssl": {"ssl_valid": True, "error": ""},
        "redirect": {"redirect_count": 0, "domain_changed": False, "uses_shortener": False},
        "virustotal": {"malicious": 0, "suspicious": 0, "harmless": 80, "undetected": 10},
        "forensic": None
    },
    {
        "name": "Google",
        "prediction": 0, "confidence": 99.9,
        "whois": {"domain_age_days": 8000},
        "ssl": {"ssl_valid": True, "error": ""},
        "redirect": {"redirect_count": 0, "domain_changed": False, "uses_shortener": False},
        "virustotal": {"malicious": 0, "suspicious": 0, "harmless": 90, "undetected": 0},
        "forensic": None
    },
    {
        "name": "Webex",
        "prediction": 0, "confidence": 95.0,
        "whois": {"domain_age_days": 6000},
        "ssl": {"ssl_valid": True, "error": ""},
        "redirect": {"redirect_count": 1, "domain_changed": False, "uses_shortener": False},
        "virustotal": {"malicious": 0, "suspicious": 0, "harmless": 85, "undetected": 5},
        "forensic": None
    },
    {
        "name": "Existing borderline phishing URL",
        "prediction": 1, "confidence": 55.0,
        "whois": {"domain_age_days": 200},
        "ssl": {"ssl_valid": False, "error": "CERTIFICATE_VERIFY_FAILED"},
        "redirect": {"redirect_count": 0, "domain_changed": False, "uses_shortener": False},
        "virustotal": {"malicious": 1, "suspicious": 1, "harmless": 50, "undetected": 30},
        "forensic": None
    },
    {
        "name": "Standard phishing URL",
        "prediction": 1, "confidence": 90.0,
        "whois": {"domain_age_days": 5},
        "ssl": {"ssl_valid": False, "error": "CERTIFICATE_VERIFY_FAILED"},
        "redirect": {"redirect_count": 2, "domain_changed": True, "uses_shortener": True},
        "virustotal": {"malicious": 5, "suspicious": 2, "harmless": 10, "undetected": 50},
        "forensic": None
    },
    {
        "name": "Established domain + malicious VirusTotal",
        "prediction": 0, "confidence": 60.0,
        "whois": {"domain_age_days": 4000},
        "ssl": {"ssl_valid": True, "error": ""},
        "redirect": {"redirect_count": 0, "domain_changed": False, "uses_shortener": False},
        "virustotal": {"malicious": 3, "suspicious": 0, "harmless": 70, "undetected": 10},
        "forensic": None
    },
    {
        "name": "Established domain + suspicious/domain-changing redirect",
        "prediction": 1, "confidence": 85.0,
        "whois": {"domain_age_days": 3000},
        "ssl": {"ssl_valid": True, "error": ""},
        "redirect": {"redirect_count": 2, "domain_changed": True, "uses_shortener": False},
        "virustotal": {"malicious": 0, "suspicious": 0, "harmless": 80, "undetected": 0},
        "forensic": None
    },
    {
        "name": "Young legitimate domain",
        "prediction": 0, "confidence": 90.0,
        "whois": {"domain_age_days": 45},
        "ssl": {"ssl_valid": True, "error": ""},
        "redirect": {"redirect_count": 0, "domain_changed": False, "uses_shortener": False},
        "virustotal": {"malicious": 0, "suspicious": 0, "harmless": 50, "undetected": 0},
        "forensic": None
    },
    {
        "name": "Young phishing URL",
        "prediction": 1, "confidence": 88.0,
        "whois": {"domain_age_days": 10},
        "ssl": {"ssl_valid": False, "error": "timeout"},
        "redirect": {"redirect_count": 0, "domain_changed": False, "uses_shortener": False},
        "virustotal": {"malicious": 2, "suspicious": 1, "harmless": 20, "undetected": 60},
        "forensic": None
    },
]

def get_risk_level(risk_score):
    if risk_score <= 15: return "Very Safe"
    elif risk_score <= 30: return "Safe"
    elif risk_score <= 50: return "Suspicious"
    elif risk_score <= 75: return "High Risk"
    else: return "Very High Risk"

for s in scenarios:
    risk, trust = engine.calculate_with_trust(
        prediction=s["prediction"],
        confidence=s["confidence"],
        whois=s["whois"],
        ssl=s["ssl"],
        redirect=s["redirect"],
        virustotal=s["virustotal"],
        forensic_report=s["forensic"]
    )
    print(f"--- {s['name']} ---")
    print(f"ML Prediction: {'Phishing' if s['prediction'] == 1 else 'Legitimate'}")
    print(f"ML Confidence: {s['confidence']}%")
    print(f"Original Risk Score: {trust['original_risk_score']}")
    print(f"Trust Score: {trust['trust_score']}")
    print(f"Trust Signals: {', '.join(trust['signals']) if trust['signals'] else 'None'}")
    print(f"Veto Status: {trust['veto_status']}")
    print(f"Veto Reason: {trust['veto_reason'] or 'None'}")
    print(f"Risk Adjustment: {trust['risk_adjustment']}")
    print(f"Final Risk Score: {trust['final_risk_score']}")
    print(f"Final Risk Level: {get_risk_level(trust['final_risk_score'])}")
    print()
