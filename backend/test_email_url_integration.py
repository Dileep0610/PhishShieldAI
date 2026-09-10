import json
from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def run_tests():
    print("--- CHECKPOINT 13 TESTS ---")

    # Test 1 - Email with one legitimate-looking URL
    print("\nTest 1 - One legitimate-looking URL:")
    res_1 = client.post("/api/analyze-email", json={
        "subject": "Project documentation",
        "body": "Please review the project documentation here:\nhttps://www.google.com"
    })
    print(f"Status: {res_1.status_code}")
    data = res_1.json()
    print(f"Extracted URLs: {data.get('extracted_urls')}")
    if data.get('url_analysis'):
        print(f"First URL Prediction: {data['url_analysis'][0].get('prediction')}")

    # Test 2 - Email with suspicious URL
    print("\nTest 2 - Suspicious URL:")
    res_2 = client.post("/api/analyze-email", json={
        "subject": "Urgent account verification",
        "body": "Your account requires immediate verification.\nPlease visit:\nhttps://example.com/login"
    })
    data = res_2.json()
    print(f"Extracted URLs: {data.get('extracted_urls')}")
    if data.get('url_analysis'):
        print(f"First URL Prediction: {data['url_analysis'][0].get('prediction')}")

    # Test 3 - Email with no URL
    print("\nTest 3 - No URL:")
    res_3 = client.post("/api/analyze-email", json={
        "subject": "Project update",
        "body": "The backend integration is progressing well. I completed the API testing today."
    })
    data = res_3.json()
    print(f"Extracted URLs: {data.get('extracted_urls')}")

    # Test 4 - Duplicate URLs
    print("\nTest 4 - Duplicate URLs:")
    res_4 = client.post("/api/analyze-email", json={
        "subject": "Important link",
        "body": "Visit https://example.com and then visit https://example.com again."
    })
    data = res_4.json()
    print(f"Extracted URLs: {data.get('extracted_urls')}")

    # Test 5 - Multiple URLs
    print("\nTest 5 - Multiple URLs:")
    res_5 = client.post("/api/analyze-email", json={
        "subject": "",
        "body": "Please check:\nhttps://example.com\nhttps://example.org/login"
    })
    data = res_5.json()
    print(f"Extracted URLs: {data.get('extracted_urls')}")
    print(f"URL Analysis Count: {len(data.get('url_analysis', []))}")

    # Test 6 - URL punctuation
    print("\nTest 6 - URL punctuation:")
    res_6 = client.post("/api/analyze-email", json={
        "subject": "",
        "body": "Click here: https://example.com/login."
    })
    data = res_6.json()
    print(f"Extracted URLs: {data.get('extracted_urls')}")

    # Test 7 - Unsupported schemes
    print("\nTest 7 - Unsupported schemes:")
    res_7 = client.post("/api/analyze-email", json={
        "subject": "",
        "body": "mailto:test@example.com\nftp://example.com/file\njavascript:alert(1)\nhttps://example.com"
    })
    data = res_7.json()
    print(f"Extracted URLs: {data.get('extracted_urls')}")

    # Regression Test: URL Endpoint
    print("\nRegression Test - URL endpoint:")
    res_url = client.post("/predict", json={
        "url": "https://www.google.com"
    })
    if res_url.status_code == 200:
        data = res_url.json()
        print({"prediction": data.get("prediction"), "risk_score": data.get("risk_score")})
    else:
        print(f"Error {res_url.status_code}: {res_url.text}")


if __name__ == "__main__":
    run_tests()
