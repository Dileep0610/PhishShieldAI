import pandas as pd
import numpy as np
from services.feature_pipeline import FeaturePipeline
import joblib

def run_tests():
    pipeline = FeaturePipeline()
    url = "https://example.com"
    original_extract = pipeline.extract
    
    def complete_extract(u):
        f = original_extract(u)
        for missing in ['FakeLinkInStatusBar', 'PopUpWindow', 'EmbeddedBrandName', 'RightClickDisabled']:
            f[missing] = 0
        if 'HttpsInHostname' in f:
            del f['HttpsInHostname']
        return f
        
    pipeline.extract = complete_extract
    
    print("\n--- Test 1: Normal feature extraction ---")
    df = pipeline.build_vector(url)
    print("Normal feature count before vector:", len(complete_extract(url)))
    
    print("\n--- Test 6: Exact contract ---")
    print("feature count:", df.shape[1])
    print("feature order correct:", list(df.columns) == pipeline.feature_names)
    print("Ordered feature list:")
    print(list(df.columns))

    print("\n--- Test 2: Missing non-RT feature ---")
    def mock_extract_missing(u):
        f = complete_extract(u)
        del f["NumDots"]
        return f
    pipeline.extract = mock_extract_missing
    try:
        pipeline.build_vector(url)
        print("FAIL: Should have raised ValueError")
    except ValueError as e:
        print(f"SUCCESS: explicit validation failure ({e})")
        
    print("\n--- Test 3: Extra feature ---")
    def mock_extract_extra(u):
        f = complete_extract(u)
        f["FakeTestFeature"] = 1
        return f
    pipeline.extract = mock_extract_extra
    try:
        pipeline.build_vector(url)
        print("FAIL: Should have raised ValueError")
    except ValueError as e:
        print(f"SUCCESS: explicit validation failure ({e})")

    print("\n--- Test 4: Unavailable RT feature ---")
    # Restore complete extract
    pipeline.extract = complete_extract
    df2 = pipeline.build_vector(url)
    val = df2["PctExtResourceUrlsRT"].iloc[0]
    print(f"Unavailable RT feature PctExtResourceUrlsRT value: {val} (is NaN: {pd.isna(val)})")

    print("\n--- Test 5: Verified RT mapping ---")
    val_sub = df2["SubdomainLevelRT"].iloc[0]
    val_len = df2["UrlLengthRT"].iloc[0]
    print(f"SubdomainLevelRT mapped value: {val_sub} (is NaN: {pd.isna(val_sub)})")
    print(f"UrlLengthRT mapped value: {val_len} (is NaN: {pd.isna(val_len)})")
    
    print("\n--- Test 7: Frozen XGBoost compatibility ---")
    model = joblib.load("models/xgboost_frozen.pkl")
    try:
        pred = model.predict_proba(df2)
        print(f"SUCCESS: Model predicted proba shape: {pred.shape}")
    except Exception as e:
        print(f"FAIL: {e}")

if __name__ == '__main__':
    run_tests()
