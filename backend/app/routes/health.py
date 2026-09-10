"""
Health check endpoints.
"""

from fastapi import APIRouter
from app.schemas import HealthCheckResponse

router = APIRouter()

@router.get("/health", response_model=HealthCheckResponse, tags=["Health"])
def health_check():
    """
    Health check endpoint.
    """
    return HealthCheckResponse(
        status="healthy",
        version="1.0.0",
        database="connected",
        model="loaded"
    )
