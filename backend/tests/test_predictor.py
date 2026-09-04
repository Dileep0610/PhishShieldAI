from services.prediction_service import PredictionService

def test_predict_basic():
    url = "https://google.com"
    service = PredictionService()
    result = service.predict(url)
    assert result is not None
    assert "prediction" in result