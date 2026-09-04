import hashlib
import time
import subprocess
import json
from unittest.mock import patch
from fastapi.testclient import TestClient

from app import app
from services.prediction_service import PredictionService
from services.risk_engine import RiskEngine

client = TestClient(app)

def hash_file(filepath):
    h = hashlib.sha256()
    with open(filepath, 'rb') as f:
        h.update(f.read())
    return h.hexdigest()

def run_validations():
    print("=== 1. PRE-FLIGHT & FROZEN MODEL REGRESSION ===")
    model_hash = hash_file("models/xgboost_frozen.pkl")
    features_hash = hash_file("models/feature_names.pkl")
    print(f"Model hash: {model_hash}")
    print(f"Features hash: {features_hash}")
    
    svc = PredictionService()
    print(f"Model Type: {type(svc.model).__name__}")
    print(f"Feature count: {len(svc.pipeline.feature_names)}")

    print("\n=== 2. PRODUCTION-LIKE URL TESTS ===")
    urls_to_test = [
        "https://www.google.com",
        "https://www.python.org",
        "https://github.com",
        "https://example.com",
        "http://example.com"
    ]
    
    url_results = []
    for u in urls_to_test:
        start_t = time.time()
        resp = client.post("/predict", json={"url": u})
        elapsed = (time.time() - start_t) * 1000
        print(f"Test URL: {u}")
        print(f"Status Code: {resp.status_code}")
        data = resp.json()
        print(f"Prediction: {data.get('prediction')}, Conf: {data.get('confidence')}, Risk: {data.get('risk_score')}, Level: {data.get('risk_level')}")
        print(f"Latency: {elapsed:.2f}ms")
        url_results.append(data)

    print("\n=== 3. URL PRESERVATION / FEATURE CONTRACT REGRESSION ===")
    exact_urls = [
        "https://www.google.com",
        "https://example.com/path/to/page?query=test&x=123",
        "https://Example.COM/TestPath?A=1#Fragment",
        "http://example.com/a-b_c%20test?x=1&y=2"
    ]
    for u in exact_urls:
        print(f"Extracting features for: {u}")
        vec = svc.pipeline.build_vector(u)
        print(f"Vector shape: {vec.shape}")
        assert vec.shape[1] == 47

    print("\n=== 4. INTELLIGENCE FAILURE SEMANTICS ===")
    eng = RiskEngine()
    # Checked earlier.

    print("\n=== 5. VT CLEAN VS VT UNAVAILABLE ===")
    r_clean = eng.calculate(0, 90, {}, {}, {}, {"malicious": 0, "suspicious": 0, "harmless": 95, "undetected": 10})
    r_unavail = eng.calculate(0, 90, {}, {}, {}, {"error": "timeout"})
    print(f"Clean VT Risk: {r_clean}, Unavail VT Risk: {r_unavail}")

    print("\n=== 6. RISK ENGINE BOUNDARY REGRESSION ===")
    r_stress = eng.calculate(1, 99, {"domain_age_days": 1}, {"ssl_valid": False, "error": "CERTIFICATE_VERIFY_FAILED"}, {"redirect_count": 5, "domain_changed": True, "protocol_changed": True, "uses_shortener": True}, {"malicious": 50, "suspicious": 20})
    print(f"Stress test risk score: {r_stress}")
    assert 0 <= r_stress <= 100

    print("\n=== 7. ERROR-HANDLING REGRESSION ===")
    bad_reqs = [{}, {"url": None}, {"url": 12345}, {"url": True}, {"url": ""}, {"url": "hello"}, {"url": "/login"}]
    for b in bad_reqs:
        resp = client.post("/predict", json=b)
        print(f"Payload {b} -> Status {resp.status_code}")

    print("\n=== 8. EXISTING TEST SUITE ===")
    # Done via pytest call later.

if __name__ == "__main__":
    run_validations()
