import joblib
import pandas as pd
import os

# ------------------------------------------
# Load model only once (FastAPI startup)
# ------------------------------------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_PATH = os.path.join(BASE_DIR, "models", "url_phishing_model.pkl")
FEATURE_PATH = os.path.join(BASE_DIR, "models", "feature_names.pkl")

model = joblib.load(MODEL_PATH)
feature_names = joblib.load(FEATURE_PATH)


def predict(features):

    # Convert dictionary to DataFrame
    df = pd.DataFrame([features])

    # Ensure same feature order as training
    df = df.reindex(columns=feature_names, fill_value=0)

    # Prediction
    prediction = model.predict(df)[0]

    # Confidence
    probability = model.predict_proba(df)[0]

    confidence = max(probability)

    return {
        "prediction": int(prediction),
        "confidence": round(confidence * 100, 2)
    }