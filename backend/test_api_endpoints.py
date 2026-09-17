import json
from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

print("--- Health ---")
resp = client.get("/health")
print(resp.status_code)

print("--- Predict ---")
resp = client.post("/predict", json={"url": "https://google.com"})
print(resp.status_code)

print("--- Email Predict ---")
resp = client.post("/api/analyze-email", json={"subject": "Hello", "body": "Please click https://google.com"})
print(resp.status_code)
