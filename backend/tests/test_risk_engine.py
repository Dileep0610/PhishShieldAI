from services.risk_engine import RiskEngine

engine = RiskEngine()

score = engine.calculate(

    prediction=0,

    confidence=85.62,

    whois={
        "domain_age_days":10541
    },

    ssl={
        "ssl_valid":True
    },

    redirect={
        "redirect_count":1,
        "uses_shortener":False
    },

    virustotal={
        "malicious": 0,
        "suspicious": 0,
        "harmless": 0,
        "undetected": 0
    }

)

print(score)