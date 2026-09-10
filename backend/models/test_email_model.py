import os
import joblib
import re

def test_email_model():
    model_path = os.path.join(os.path.dirname(__file__), "email_linear_svm.pkl")
    vectorizer_path = os.path.join(os.path.dirname(__file__), "email_tfidf_vectorizer.pkl")

    print(f"Loading model from {model_path}")
    print(f"Loading vectorizer from {vectorizer_path}")

    try:
        model = joblib.load(model_path)
        vectorizer = joblib.load(vectorizer_path)
        print("Model and vectorizer successfully loaded.")
    except Exception as e:
        print(f"Failed to load artifacts: {e}")
        return

    print(f"Model type: {type(model)}")
    print(f"Vectorizer vocabulary size: {len(vectorizer.vocabulary_)}")
    
    # Vectorizer configuration checks
    v_params = vectorizer.get_params()
    print(f"Vectorizer config:")
    print(f"  ngram_range: {v_params.get('ngram_range')}")
    print(f"  min_df: {v_params.get('min_df')}")
    print(f"  max_df: {v_params.get('max_df')}")
    print(f"  max_features: {v_params.get('max_features')}")
    print(f"  sublinear_tf: {v_params.get('sublinear_tf')}")
    print(f"  lowercase: {v_params.get('lowercase')}")
    print(f"  strip_accents: {v_params.get('strip_accents')}")

    # Check classes
    print(f"Model classes: {model.classes_}")
    
    # Format classes to expected strings
    def decode_prediction(pred):
        if isinstance(pred, str):
            if pred.lower() in ['phishing', '1']:
                return "Phishing"
            else:
                return "Legitimate"
        return "Phishing" if pred == 1 else "Legitimate"

    test_cases = [
        {
            "subject": "Meeting schedule for tomorrow",
            "body": "Hi team, our project meeting is scheduled for tomorrow at 10 AM. Please bring your progress updates. Regards, Team Lead.",
            "expected": "Legitimate"
        },
        {
            "subject": "Urgent: Verify your account immediately",
            "body": "Your account has been temporarily restricted. Click the link below and verify your username, password, and security information immediately to avoid permanent suspension.",
            "expected": "Phishing"
        },
        {
            "subject": "Your bank account requires verification",
            "body": "We detected unusual activity on your bank account. Please confirm your account details immediately using the secure verification link provided below.",
            "expected": "Phishing"
        },
        {
            "subject": "Project update",
            "body": "The backend integration is progressing well. I completed the API testing and will share the updated results with the team this afternoon.",
            "expected": "Legitimate"
        },
        {
            "subject": "Congratulations! You have won a cash prize",
            "body": "You have been selected as a winner. Claim your cash reward now by providing your personal information and completing the verification process.",
            "expected": "Phishing"
        },
        {
            "subject": "Hello",
            "body": "How are you?",
            "expected": "Legitimate"
        },
        {
            "subject": "",
            "body": "Please review the attached project document and let me know if any changes are required.",
            "expected": "Legitimate"
        },
        {
            "subject": "Password expires today",
            "body": "Your password will expire today. Sign in now to keep your account active and enter your login credentials to complete the verification.",
            "expected": "Phishing"
        }
    ]

    total_tests = len(test_cases)
    correct_predictions = 0
    disagreements = 0
    feature_count = 0

    print("-" * 50)
    for i, tc in enumerate(test_cases, 1):
        subject = tc["subject"]
        body = tc["body"]
        expected = tc["expected"]

        # Preprocessing
        combined_text = f"SUBJECT: {subject} BODY: {body}"
        normalized_text = re.sub(r'\s+', ' ', combined_text).strip()

        # Transform
        features = vectorizer.transform([normalized_text])
        feature_count = features.shape[1]

        # Predict
        pred_raw = model.predict(features)[0]
        decision_score = model.decision_function(features)[0]
        
        predicted_label = decode_prediction(pred_raw)
        
        status = "PASS" if predicted_label == expected else "REVIEW"
        if status == "PASS":
            correct_predictions += 1
        else:
            disagreements += 1

        print(f"Test {i}:")
        print(f"Subject: {subject}")
        print(f"Predicted label: {predicted_label} (Raw: {pred_raw})")
        print(f"SVM decision score: {decision_score:.4f} (Model Confidence/Score)")
        print(f"Expected label: {expected}")
        print(f"Status: {status}")
        print("-" * 50)
        
    print("FINAL SUMMARY:")
    print(f"Total tests: {total_tests}")
    print(f"Correct sanity-check predictions: {correct_predictions}")
    print(f"Disagreements: {disagreements}")
    print(f"Model/vectorizer successfully loaded: True")
    print(f"TF-IDF transformed feature count: {feature_count}")

if __name__ == '__main__':
    test_email_model()
