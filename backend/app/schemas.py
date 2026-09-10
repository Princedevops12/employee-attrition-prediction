"""
Pydantic models for API request/response validation.
"""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class PredictionRequest(BaseModel):
    """Request model for single prediction."""
    age: int = Field(..., ge=18, le=100, description="Employee age")
    monthly_income: float = Field(..., gt=0, description="Monthly income")
    years_at_company: int = Field(..., ge=0, description="Years at company")
    years_in_current_role: int = Field(..., ge=0, description="Years in current role")
    years_with_curr_manager: int = Field(..., ge=0, description="Years with current manager")
    total_working_years: int = Field(..., ge=0, description="Total working years")
    job_satisfaction: int = Field(..., ge=1, le=4, description="Job satisfaction (1-4)")
    work_life_balance: int = Field(..., ge=1, le=4, description="Work-life balance (1-4)")
    job_role: str = Field(..., description="Job role")
    department: str = Field(..., description="Department")
    distance_from_home: int = Field(..., ge=0, description="Distance from home (km)")
    over_time: str = Field(..., description="'Yes' or 'No'")
    
    class Config:
        json_schema_extra = {
            "example": {
                "age": 45,
                "monthly_income": 5000,
                "years_at_company": 10,
                "years_in_current_role": 5,
                "years_with_curr_manager": 3,
                "total_working_years": 15,
                "job_satisfaction": 3,
                "work_life_balance": 3,
                "job_role": "Sales Executive",
                "department": "Sales",
                "distance_from_home": 5,
                "over_time": "No"
            }
        }

class PredictionResponse(BaseModel):
    """Response model for predictions."""
    attrition_risk: bool = Field(..., description="Whether employee is at risk of attrition")
    probability: float = Field(..., ge=0, le=1, description="Probability of attrition (0-1)")
    risk_level: str = Field(..., description="Risk level: 'Low', 'Medium', or 'High'")
    confidence: float = Field(..., ge=0, le=1, description="Model confidence")
    
    class Config:
        json_schema_extra = {
            "example": {
                "attrition_risk": True,
                "probability": 0.72,
                "risk_level": "High",
                "confidence": 0.85
            }
        }

class EmployeeBase(BaseModel):
    """Base employee model."""
    name: str
    department: str
    job_role: str = "Not Specified"
    age: int = Field(ge=18, le=100)
    gender: Optional[str] = "Unknown"
    monthly_income: float = Field(gt=0)
    years_at_company: int = Field(ge=0)
    job_satisfaction: int = Field(ge=1, le=4)
    work_life_balance: int = Field(ge=1, le=4)

class EmployeeCreate(EmployeeBase):
    """Model for creating employees."""
    pass

class EmployeeUpdate(BaseModel):
    """Model for updating employees."""
    name: Optional[str] = None
    department: Optional[str] = None
    job_role: Optional[str] = None
    age: Optional[int] = Field(None, ge=18, le=100)
    monthly_income: Optional[float] = Field(None, gt=0)
    job_satisfaction: Optional[int] = Field(None, ge=1, le=4)

class EmployeeResponse(EmployeeBase):
    """Response model for employees."""
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class EmployeeWithPredictions(EmployeeResponse):
    """Employee response with latest predictions."""
    latest_prediction: Optional[PredictionResponse] = None

class ModelMetricsResponse(BaseModel):
    """Response model for model metrics."""
    model_version: str
    model_name: str
    training_date: datetime
    accuracy: float
    precision: float
    recall: float
    f1_score: float
    roc_auc: float
    confusion_matrix: Optional[List[List[int]]] = None
    
    class Config:
        from_attributes = True

class HealthCheckResponse(BaseModel):
    """Response model for health check."""
    status: str = "healthy"
    version: str = "1.0.0"
    database: str = "connected"
    model: str = "loaded"

class BatchPredictionResponse(BaseModel):
    """Response model for batch predictions."""
    processed_count: int
    success_count: int
    error_count: int
    results_file: Optional[str] = None
    download_url: Optional[str] = None
