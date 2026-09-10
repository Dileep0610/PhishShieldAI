import os
import joblib
import re
from typing import Dict, Any

class EmailPredictionService:
    def __init__(self):
        base_dir = os.path.dirname(os.path.dirname(__file__))
        model_path = os.path.join(base_dir, "models", "email_linear_svm.pkl")
        vectorizer_path = os.path.join(base_dir, "models", "email_tfidf_vectorizer.pkl")

        # Load artifacts once
        self.model = joblib.load(model_path)
        self.vectorizer = joblib.load(vectorizer_path)

    def predict(self, subject: str, body: str) -> Dict[str, Any]:
        # Normalize and combine
        subject_str = str(subject) if subject is not None else ""
        body_str = str(body) if body is not None else ""
        
        combined_text = f"SUBJECT: {subject_str} BODY: {body_str}"
        normalized_text = re.sub(r'\s+', ' ', combined_text).strip()

        # Transform using saved vectorizer
        features = self.vectorizer.transform([normalized_text])

        # Predict using saved model
        pred_raw = self.model.predict(features)[0]
        decision_score = self.model.decision_function(features)[0]

        # Model mapping: [0, 1] where 0 = Legitimate, 1 = Phishing
        prediction_label = "Phishing" if pred_raw == 1 else "Legitimate"

        # Explicit fallback if classes are strings
        if isinstance(pred_raw, str):
            prediction_label = "Phishing" if pred_raw.lower() in ['1', 'phishing'] else "Legitimate"

        return {
            "prediction": prediction_label,
            "decision_score": float(decision_score)
        }
