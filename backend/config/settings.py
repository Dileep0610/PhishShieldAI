import os
from pathlib import Path

allowed_origins_str = os.getenv("PHISHSHIELD_ALLOWED_ORIGINS", "http://localhost:3000,http://localhost:5173,http://127.0.0.1:5173")
ALLOWED_ORIGINS = [origin.strip() for origin in allowed_origins_str.split(",") if origin.strip()]

APP_NAME = "PhishShield AI"

VERSION = "1.0"

DESCRIPTION = "AI Powered Phishing Detection System"

REQUEST_TIMEOUT = 5

BACKEND_DIR = Path(__file__).resolve().parent.parent

MODEL_PATH = str(BACKEND_DIR / "models" / "url_phishing_model.pkl")

FROZEN_MODEL_PATH = str(BACKEND_DIR / "models" / "xgboost_frozen.pkl")

FEATURE_PATH = str(BACKEND_DIR / "models" / "feature_names.pkl")

RT_MAPPINGS_PATH = str(BACKEND_DIR / "models" / "verified_rt_lookup_mappings.pkl")