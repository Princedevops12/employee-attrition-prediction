"""
SQLAlchemy ORM models for Employee Attrition database.
"""

from datetime import datetime

from sqlalchemy import (
    JSON,
    Boolean,
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.orm import relationship

from app.database import Base


class Employee(Base):
    """
    Employee record model.
    """
    __tablename__ = "employees"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    department = Column(String, index=True)
    job_role = Column(String)
    age = Column(Integer)
    gender = Column(String)
    monthly_income = Column(Float)
    hourly_rate = Column(Float)
    years_at_company = Column(Integer)
    years_in_current_role = Column(Integer)
    years_with_curr_manager = Column(Integer)
    total_working_years = Column(Integer)
    job_satisfaction = Column(Integer)  # 1-4 scale
    work_life_balance = Column(Integer)  # 1-4 scale
    distance_from_home = Column(Integer)
    over_time = Column(String)  # 'Yes' or 'No'
    marital_status = Column(String)
    education_field = Column(String)
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    predictions = relationship("Prediction", back_populates="employee", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Employee(id={self.id}, name={self.name}, department={self.department})>"

class Prediction(Base):
    """
    Attrition prediction record model.
    """
    __tablename__ = "predictions"
    
    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"), index=True)
    
    # Prediction results
    attrition_risk = Column(Boolean)  # True = Yes, False = No
    probability = Column(Float)  # 0.0-1.0
    risk_level = Column(String)  # 'Low', 'Medium', 'High'
    confidence = Column(Float)  # Model confidence
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    employee = relationship("Employee", back_populates="predictions")
    
    def __repr__(self):
        return f"<Prediction(id={self.id}, employee_id={self.employee_id}, probability={self.probability:.2f})>"

class ModelMetrics(Base):
    """
    Model performance metrics record.
    """
    __tablename__ = "model_metrics"
    
    id = Column(Integer, primary_key=True, index=True)
    model_version = Column(String, index=True)
    model_name = Column(String)  # 'RandomForest', 'XGBoost', etc.
    training_date = Column(DateTime, default=datetime.utcnow)
    
    # Performance metrics
    accuracy = Column(Float)
    precision = Column(Float)
    recall = Column(Float)
    f1_score = Column(Float)
    roc_auc = Column(Float)
    
    # Additional data
    confusion_matrix = Column(JSON)  # Stored as JSON
    training_samples = Column(Integer)
    test_samples = Column(Integer)
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<ModelMetrics(id={self.id}, model_version={self.model_version}, f1_score={self.f1_score:.4f})>"
