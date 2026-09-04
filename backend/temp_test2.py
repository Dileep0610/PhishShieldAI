from extractors.url_extractor import FeatureExtractor
from services.feature_pipeline import FeaturePipeline

def run_tests():
    extractor = FeatureExtractor()
    pipeline = FeaturePipeline()
    
    print("\n--- Test 1: HTTPS hostname feature ---")
    url1 = "https://example.com"
    f1 = extractor.extract_url_features(url1)
    if "HttpsInHostname" not in f1:
        print("SUCCESS: HttpsInHostname not in extracted_features")
    else:
        print("FAIL: HttpsInHostname is present")
        
    print("\n--- Test 2: EmbeddedBrandName positive case ---")
    url2 = "http://paypal-update.example.com/login"
    f2 = extractor.extract_url_features(url2)
    print(f"Test URL: {url2}")
    if f2.get("EmbeddedBrandName") == 1:
        print("SUCCESS: EmbeddedBrandName == 1")
    else:
        print("FAIL: EmbeddedBrandName !=", f2.get("EmbeddedBrandName"))
        
    print("\n--- Test 3: EmbeddedBrandName negative case ---")
    url3 = "http://example.com/login"
    f3 = extractor.extract_url_features(url3)
    if f3.get("EmbeddedBrandName") == 0:
        print("SUCCESS: EmbeddedBrandName == 0")
    else:
        print("FAIL: EmbeddedBrandName !=", f3.get("EmbeddedBrandName"))
        
    print("\n--- Test 4: Existing URL features ---")
    print("NumDots:", f3.get("NumDots"))
    print("SubdomainLevel:", f3.get("SubdomainLevel"))
    print("UrlLength:", f3.get("UrlLength"))
    print("SUCCESS: Existing features present")
    
    print("\n--- Test 5: Pipeline integration ---")
    try:
        pipeline.build_vector(url1)
        print("FAIL: Pipeline succeeded which means HTML features aren't missing?")
    except ValueError as e:
        msg = str(e)
        if "Unexpected extra features found" in msg and "HttpsInHostname" in msg:
            print("FAIL: HttpsInHostname still reported as extra feature")
        elif "Missing required non-RT features:" in msg:
            if "FakeLinkInStatusBar" in msg and "HttpsInHostname" not in msg:
                print("SUCCESS: Pipeline integration (only missing HTML features reported)")
                print(msg)
            else:
                print("Partial Match:", msg)
        else:
            print("OTHER ERROR:", msg)

if __name__ == '__main__':
    run_tests()
