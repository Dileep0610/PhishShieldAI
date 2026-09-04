import os
import json
import numpy as np
import time
from datetime import datetime

import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from services.prediction_service import PredictionService

def investigate():
    print("============================================================")
    print("PHISHSHIELD AI — LIVE FALSE POSITIVE INVESTIGATION")
    print("============================================================\n")

    urls = [
        "https://www.google.com",
        "https://www.instagram.com/",
        "https://dileepkumar-flax.vercel.app/"
    ]

    service = PredictionService()
    pipeline = service.pipeline
    model = service.model
    feature_names = pipeline.feature_names
    
    results = {}
    vectors = {}
    
    # Check model features and classes
    print(f"Model classes: {model.classes_}")

    importances = model.feature_importances_
    sorted_idx = np.argsort(importances)[::-1]
    
    print("\n--- Top 15 Most Important Features Globally ---")
    print(f"{'Rank':<5} | {'Feature':<35} | {'Importance'}")
    top_15 = []
    for i in range(15):
        idx = sorted_idx[i]
        top_15.append(idx)
        print(f"{i+1:<5} | {feature_names[idx]:<35} | {importances[idx]:.4f}")

    for url in urls:
        print(f"\n============================================================")
        print(f"Investigating: {url}")
        print(f"============================================================")
        
        # 1 & 2. Extract features and print
        vector_df = pipeline.build_vector(url)
        vector_row = vector_df.iloc[0].values
        vectors[url] = vector_row
        
        print(f"\nFeature count: {len(feature_names)}")
        print("Feature values:")
        
        missing_before_nan = []
        rt_nans = []
        
        features_dict = {}
        for i, (name, val) in enumerate(zip(feature_names, vector_row)):
            # Let's see if it's NaN
            is_nan = False
            if isinstance(val, float) and np.isnan(val):
                is_nan = True
                
            print(f"{i+1:02d} {name:<35} = {val}")
            features_dict[name] = val
            
            if is_nan:
                if name.endswith("RT") or name.endswith("R"):
                    rt_nans.append(name)
                else:
                    missing_before_nan.append(name)
                    
        # 3. Missing/Unresolved
        print("\nMissing features before NaN conversion:")
        if missing_before_nan:
            for m in missing_before_nan:
                print(f"ERROR: Non-RT feature missing: {m}")
        else:
            print("None")
            
        print("\nRT features with NaN:")
        if rt_nans:
            for m in rt_nans:
                print(m)
        else:
            print("None")
            
        # 4. XGBoost Prediction
        proba = model.predict_proba(vector_df)[0]
        pred = 1 if proba[1] >= 0.5 else 0
        conf = float(round((proba[pred] if pred == 1 else proba[0]) * 100, 2))
        
        print("\n--- XGBoost Result ---")
        print(f"P(class 0 / Legitimate) = {proba[0]:.4f}")
        print(f"P(class 1 / Phishing) = {proba[1]:.4f}")
        print(f"Predicted class = {pred}")
        print(f"Confidence = {conf}%")
        
        # Top 15 values for this URL
        print("\n--- Top 15 Feature Values for this URL ---")
        for i, idx in enumerate(top_15):
            print(f"{i+1:<5} | {feature_names[idx]:<35} = {vector_row[idx]}")
            
        # Network & Risk Engine
        print("\n--- Intelligence & Risk Engine ---")
        # Run prediction full
        pred_res = service.predict(url)
        print(f"ML prediction: {'Phishing' if pred_res['prediction'] == 1 else 'Legitimate'}")
        print(f"ML confidence: {pred_res['confidence']}%")
        print(f"WHOIS result: {pred_res['whois']}")
        print(f"SSL result: {pred_res['ssl']}")
        print(f"Redirect result: {pred_res['redirect']}")
        print(f"VirusTotal result: {pred_res['virustotal']}")
        print(f"Risk score: {pred_res['risk_score']}")
        
        # Determine contributions (by calling calculate multiple times)
        engine = service.risk_engine
        ml_score = engine.calculate(pred_res['prediction'], pred_res['confidence'], {}, {}, {}, {})
        whois_score = engine.calculate(0, 95, pred_res['whois'], {"ssl_valid": True}, {}, {})
        ssl_score = engine.calculate(0, 95, {"domain_age_days": 5000}, pred_res['ssl'], {}, {})
        redir_score = engine.calculate(0, 95, {"domain_age_days": 5000}, {"ssl_valid": True}, pred_res['redirect'], {})
        vt_score = engine.calculate(0, 95, {"domain_age_days": 5000}, {"ssl_valid": True}, {}, pred_res['virustotal'])
        
        print("\n--- Risk Contributions (Approximate Base Additions) ---")
        print(f"ML contribution: {ml_score}")
        print(f"WHOIS contribution: {whois_score}")
        print(f"SSL contribution: {ssl_score}")
        print(f"Redirect contribution: {redir_score}")
        print(f"VirusTotal contribution: {vt_score}")
        print(f"Total Combined (capped): {pred_res['risk_score']}")
        
        results[url] = {
            "features": features_dict,
            "prediction": pred_res['prediction'],
            "confidence": pred_res['confidence'],
            "risk_score": pred_res['risk_score'],
            "whois": pred_res['whois'],
            "ssl": pred_res['ssl'],
            "redirect": pred_res['redirect'],
            "virustotal": pred_res['virustotal']
        }
        
    print("\n============================================================")
    print("COMPACT COMPARISON TABLE")
    print("============================================================")
    print(f"{'Feature':<35} | {'Google':<15} | {'Instagram':<15} | {'Portfolio':<15}")
    print("-" * 88)
    for name in feature_names:
        v0 = vectors[urls[0]][feature_names.index(name)]
        v1 = vectors[urls[1]][feature_names.index(name)]
        v2 = vectors[urls[2]][feature_names.index(name)]
        # format as str to handle NaNs
        print(f"{name:<35} | {str(v0):<15} | {str(v1):<15} | {str(v2):<15}")

    # Check RT Behavior Carefully
    rt_feats = [
        "SubdomainLevelRT",
        "UrlLengthRT",
        "PctExtResourceUrlsRT",
        "AbnormalExtFormActionR",
        "ExtMetaScriptLinkRT",
        "PctExtNullSelfRedirectHyperlinksRT"
    ]
    
    print("\n============================================================")
    print("RT BEHAVIOR CAREFULLY")
    print("============================================================")
    for url in urls:
        print(f"\n{url}")
        for rt in rt_feats:
            val = results[url]["features"][rt]
            if np.isnan(val):
                src = "unresolved"
            else:
                # UrlLengthRT is exact rule
                if rt == "UrlLengthRT":
                    src = "exact rule"
                elif rt == "SubdomainLevelRT":
                    # either verified lookup or exact rule
                    src = "verified lookup or rule"
                else:
                    src = "unresolved (but somehow got a value?)"
            print(f"  {rt:<35}: {str(val):<5} (source: {src})")


    print("\n============================================================")
    print("SAVING CHECKPOINT")
    print("============================================================")
    
    checkpoint_data = {
        "timestamp": datetime.now().isoformat(),
        "urls": urls,
        "results": results,
        "features": {u: {k: str(v) for k, v in zip(feature_names, vectors[u])} for u in urls},
        "observations": "Live extraction generates many NaNs for RT and may extract suspicious looking feature patterns from legitimate websites (e.g., long domains, high percentage of external resources, right click disabled, etc).",
        "possible_anomalies": ["Modern JS sites have high PctExtResourceUrls", "UrlLengthRT triggering on portfolio URL"],
        "confirmation": "No production model/pipeline files were modified."
    }
    
    ckpt_path = r"D:\PhishShieldAI\checkpoints\step_3_9A_live_false_positive_investigation.json"
    os.makedirs(os.path.dirname(ckpt_path), exist_ok=True)
    with open(ckpt_path, "w") as f:
        json.dump(checkpoint_data, f, indent=4)
        
    print(f"Saved to {ckpt_path}")
    print("\nInvestigation complete. See output above.")

if __name__ == "__main__":
    investigate()
