from services.feature_pipeline import FeaturePipeline

pipeline = FeaturePipeline()

vector = pipeline.build_vector(
    "https://google.com"
)

print(vector.shape)

print(vector)