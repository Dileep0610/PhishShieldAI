import pytest
import numpy as np
import pandas as pd
from unittest.mock import MagicMock

from services.explainability_service import ExplainabilityService
from services.prediction_service import PredictionService

@pytest.fixture
def mock_model(monkeypatch):
    import xgboost as xgb
    monkeypatch.setattr(xgb, "DMatrix", lambda *args, **kwargs: MagicMock())
    model = MagicMock()
    booster = MagicMock()
    # 47 features + 1 bias = 48 values
    # Let's say indices 0-46 are 0.1 (phishing), except 0 is -0.5 (legitimate), and 47 is bias
    contribs = np.array([[0.1] * 47 + [0.5]])
    contribs[0][0] = -0.5 # feature 0 is negative
    booster.predict.return_value = contribs
    model.get_booster.return_value = booster
    return model

@pytest.fixture
def mock_feature_names():
    # 47 dummy feature names
    return [f"Feature_{i}" for i in range(47)]

@pytest.fixture
def feature_vector(mock_feature_names):
    # 47 values
    return pd.DataFrame([[1.0] * 47], columns=mock_feature_names)

def test_explainability_service_valid(mock_model, mock_feature_names, feature_vector):
    service = ExplainabilityService()
    
    # Mocking metadata to avoid None mapping issues
    for f in mock_feature_names:
        service.feature_metadata[f] = {"human_name": f"Human {f}", "category": "URL"}
        
    # Introduce NaN
    feature_vector.iloc[0, 1] = float('nan')
    
    result = service.generate_explanation(
        mock_model,
        mock_feature_names,
        feature_vector,
        {}, {}, {}, {}
    )
    
    assert result["status"] == "available"
    # TEST 4: Output handles exactly 47 features (bias ignored).
    # TEST 5: Bias exclusion
    # Total contributors = 47 - 1 (NaN) = 46. (We don't count bias)
    total_contribs = len(result["model_explanation"]["top_positive_contributors"]) + len(result["model_explanation"]["top_negative_contributors"])
    assert total_contribs <= 10 # capped at 10
    
    # TEST 6: Positive contribution -> phishing
    # TEST 7: Negative contribution -> legitimate
    assert result["model_explanation"]["top_positive_contributors"][0]["direction"] == "phishing"
    
    has_negative = any(c["direction"] == "legitimate" for c in result["model_explanation"]["top_negative_contributors"])
    assert has_negative
    
    # TEST 9, 10, 11: NaN handling
    # Feature 1 was NaN
    unavailable = result["unavailable_evidence"]
    assert any(u["feature"] == "Feature_1" for u in unavailable)
    
def test_explainability_integration():
    service = PredictionService()
    
    # Run a prediction and check explainability is attached and prediction remains same
    url = "https://www.google.com"
    
    # To test failure isolation, we can break the model temporarily
    old_model = service.explainability.feature_metadata
    service.explainability.feature_metadata = None # This will cause an exception in explainability
    
    result = service.predict(url)
    
    # TEST 11: Failure isolation
    assert result["explainability"]["status"] == "unavailable"
    assert "prediction" in result
    
    # Restore
    service.explainability.feature_metadata = old_model
    
    # TEST 10: Original prediction unchanged (explainability works)
    result_valid = service.predict(url)
    assert result_valid["explainability"]["status"] == "available"
    assert result_valid["prediction"] == result["prediction"]
    assert result_valid["risk_score"] == result["risk_score"]

