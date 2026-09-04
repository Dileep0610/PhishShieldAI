from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes.predict import router as predict_router
from routes.health import router as health_router
from config.settings import ALLOWED_ORIGINS

app = FastAPI(
    title="PhishShield AI",
    version="1.0",
    description="AI Powered Phishing Detection System"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=("*" not in ALLOWED_ORIGINS),
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(predict_router)
app.include_router(health_router)