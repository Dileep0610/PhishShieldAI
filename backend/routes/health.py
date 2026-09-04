from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
def health():

    return {
        "status": "healthy",
        "service": "PhishShield AI",
        "model": "Random Forest",
        "version": "1.0"
    }