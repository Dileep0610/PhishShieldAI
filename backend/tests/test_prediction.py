from services.prediction_service import PredictionService

service = PredictionService()

result = service.predict(
    "https://google.com"
)

print(result)