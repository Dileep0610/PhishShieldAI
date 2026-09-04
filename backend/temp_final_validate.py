import joblib
import pandas as pd
import numpy as np
import os
import sys

# Ensure backend in path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.prediction_service import PredictionService
from services.feature_pipeline import FeaturePipeline
from extractors.url_extractor import FeatureExtractor
from extractors.html_extractor import HTMLExtractor

def main():
    print("=== 1. Artifact Validation ===")
    model = joblib.load("models/xgboost_frozen.pkl")
    feature_names = joblib.load("models/feature_names.pkl")
    rt_mappings = joblib.load("models/verified_rt_lookup_mappings.pkl")
    
    print(f"model type = {type(model).__name__}")
    print(f"n_features_in_ = {getattr(model, 'n_features_in_', 'unknown')}")
    print(f"classes_ = {getattr(model, 'classes_', 'unknown')}")
    print(f"feature_names length = {len(feature_names)}")
    
    urls = [
        "https://www.google.com",
        "https://www.microsoft.com",
        "https://github.com",
        "https://www.python.org"
    ]
    
    url_extractor = FeatureExtractor()
    html_extractor = HTMLExtractor(timeout=5)
    pipeline = FeaturePipeline()
    service = PredictionService()
    
    overall_pass = True

    print("\n=== URL-by-URL Validation ===")
    for url in urls:
        print(f"\n--- URL: {url} ---")
        
        soup = html_extractor.fetch_html(url)
        if soup is None:
            print("Access failure. Skipping.")
            continue
            
        print("HTML Fetched successfully.")
        
        url_features = url_extractor.extract_url_features(url)
        print("URL Extractor Features:", list(url_features.keys()))
        
        html_features_raw = {}
        html_features_raw["MissingTitle"] = html_extractor.extract_title(soup)
        html_features_raw["IframeOrFrame"] = html_extractor.extract_iframe(soup)
        html_features_raw["InsecureForms"] = html_extractor.extract_insecure_forms(soup)
        html_features_raw["PctExtHyperlinks"] = html_extractor.extract_external_hyperlinks(soup, url)
        html_features_raw["PctExtResourceUrls"] = html_extractor.extract_external_resources(soup, url)
        html_features_raw.update(html_extractor.extract_form_features(soup, url))
        html_features_raw["ExtFavicon"] = html_extractor.extract_external_favicon(soup, url)
        html_features_raw["ExtMetaScriptLinkRT"] = html_extractor.extract_meta_script_link_rt(soup, url)
        html_features_raw["PctNullSelfRedirectHyperlinks"] = html_extractor.extract_null_redirect_links(soup)
        html_features_raw["FrequentDomainNameMismatch"] = html_extractor.extract_domain_mismatch(soup, url)
        
        print("HTML Extractor Features:", list(html_features_raw.keys()))
        
        req_features = ["EmbeddedBrandName", "FakeLinkInStatusBar", "PopUpWindow", "RightClickDisabled"]
        combined = {**url_features, **html_features_raw}
        
        for r in req_features:
            if r not in combined:
                print(f"Missing req non-RT feature: {r}")
                overall_pass = False
                
        print(f"HttpsInHostname absent: {'HttpsInHostname' not in combined}")
        if 'HttpsInHostname' in combined:
            overall_pass = False
            
        try:
            df = pipeline.build_vector(url)
            print("exact feature count =", df.shape[1])
            print("exact feature order =", list(df.columns) == feature_names)
            
            rt_cols = ["SubdomainLevelRT", "UrlLengthRT", "PctExtResourceUrlsRT", "AbnormalExtFormActionR", "ExtMetaScriptLinkRT", "PctExtNullSelfRedirectHyperlinksRT"]
            
            unavailable_rt = sum(1 for c in rt_cols if pd.isna(df[c].iloc[0]))
            print("unavailable RT values =", unavailable_rt)
            
            if url == urls[0]:
                print("Ordered feature list:", list(df.columns))
                
        except Exception as e:
            print("Pipeline Error:", e)
            overall_pass = False
            continue
            
        try:
            proba_direct = model.predict_proba(df)[0]
            pred_direct = 1 if proba_direct[1] >= 0.5 else 0
            
            print(f"input shape = {df.shape}")
            print(f"predict_proba shape = {model.predict_proba(df).shape}")
            print(f"P(class=0) = {proba_direct[0]}")
            print(f"P(class=1) = {proba_direct[1]}")
            print(f"P(class=0) + P(class=1) = {proba_direct[0] + proba_direct[1]}")
            print(f"direct prediction = {pred_direct}")
            
            result_service = service.predict(url)
            print("PredictionService probability =", result_service['phishing_probability'])
            print("PredictionService prediction =", result_service['prediction'])
            
            diff = abs(proba_direct[1] - result_service['phishing_probability'])
            pred_mismatch = abs(pred_direct - result_service['prediction'])
            print("probability difference =", diff)
            print("prediction mismatch =", pred_mismatch)
            
            if diff > 1e-5 or pred_mismatch > 0:
                overall_pass = False
        except Exception as e:
            print("Prediction Error:", e)
            overall_pass = False

    print("\n=== Existing Unit Tests ===")
    os.system("python -m pytest tests/")

if __name__ == '__main__':
    main()
