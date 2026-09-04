import joblib
import os
import pandas as pd

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

FEATURE_PATH = os.path.join(BASE_DIR, "models", "feature_names.pkl")

feature_names = joblib.load(FEATURE_PATH)


def build_vector(features):

    df = pd.DataFrame([features])

    df = df.reindex(
        columns=feature_names,
        fill_value=0
    )

    return df