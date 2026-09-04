import joblib
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_PATH = os.path.join(BASE_DIR, "models", "url_phishing_model.pkl")

model = joblib.load(MODEL_PATH)


def predict(vector):

    prediction = model.predict(vector)[0]

    probability = model.predict_proba(vector)[0]

    confidence = float(max(probability))

    return {
        "prediction": int(prediction),
        "confidence": round(confidence * 100, 2)
    }