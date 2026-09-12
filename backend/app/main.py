"""
Employee Attrition Prediction API

FastAPI-based REST API for employee attrition prediction with database integration.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import database and models after loading env
from app.database import init_db
from app.routes import predictions, employees, health

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Context manager for application startup and shutdown.
    """
    # Startup: Initialize database
    print("Initializing database...")
    init_db()
    yield
    # Shutdown: cleanup (if needed)
    print("Shutting down...")

# Create FastAPI app with lifespan context
app = FastAPI(
    title="Employee Attrition Prediction API",
    description="API for predicting employee attrition and managing employee records",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS
cors_origins = os.getenv('CORS_ORIGINS', '["http://localhost:3000", "http://localhost:5173"]')
# Parse CORS origins from environment variable (JSON string)
import json
try:
    origins = json.loads(cors_origins)
except (json.JSONDecodeError, TypeError):
    origins = [
    "http://localhost:3000",
    "http://localhost:5173",
    "https://employee-attrition-prediction-2-4olh.onrender.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health.router, prefix="/api", tags=["Health"])
app.include_router(predictions.router, prefix="/api", tags=["Predictions"])
app.include_router(employees.router, prefix="/api", tags=["Employees"])

@app.get("/")
def read_root():
    """Root endpoint."""
    return {
        "message": "Employee Attrition Prediction API",
        "docs": "/docs",
        "version": "1.0.0"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
