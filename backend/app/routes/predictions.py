"""
Prediction endpoints for attrition prediction.
"""

from fastapi import APIRouter, HTTPException, Depends, File, UploadFile, Form
from sqlalchemy.orm import Session
from io import StringIO
import csv
import os
from pathlib import Path
import joblib
import pandas as pd
from datetime import datetime

from app.database import get_db
from app.schemas import PredictionRequest, PredictionResponse, BatchPredictionResponse
from app.models import Prediction, Employee

router = APIRouter()

# Global model and preprocessor (loaded once at startup)
_model = None
_preprocessor = None

def load_model():
    """Load the trained model and preprocessor."""
    global _model, _preprocessor
    
    if _model is None:
        model_path = Path(__file__).parent.parent.parent / 'ml' / 'models' / 'model.pkl'
        preprocessor_path = Path(__file__).parent.parent.parent / 'ml' / 'models' / 'preprocessor.pkl'
        
        if model_path.exists() and preprocessor_path.exists():
            try:
                _model = joblib.load(model_path)
                _preprocessor = joblib.load(preprocessor_path)
                print("Model and preprocessor loaded successfully")
            except Exception as e:
                print(f"Error loading model: {e}")
                return False
        else:
            print(f"Model files not found at {model_path} or {preprocessor_path}")
            return False
    
    return True

def get_prediction_data(request: PredictionRequest):
    """Convert API request to a format compatible with the preprocessor."""
    # Create a dictionary matching the preprocessor's expected features
    data = {
        'Age': request.age,
        'MonthlyIncome': request.monthly_income,
        'YearsAtCompany': request.years_at_company,
        'YearsInCurrentRole': request.years_in_current_role,
        'YearsWithCurrManager': request.years_with_curr_manager,
        'TotalWorkingYears': request.total_working_years,
        'JobSatisfaction': request.job_satisfaction,
        'WorkLifeBalance': request.work_life_balance,
        'JobRole': request.job_role,
        'Department': request.department,
        'DistanceFromHome': request.distance_from_home,
        'OverTime': request.over_time,
        # Add default values for other required features
        'Education': 3,
        'EnvironmentSatisfaction': 3,
        'HourlyRate': 65,
        'JobInvolvement': 2,
        'JobLevel': 2,
        'MaritalStatus': 'Single',
        'MonthlyRate': 5000,
        'NumCompaniesWorked': 2,
        'PercentSalaryHike': 13,
        'PerformanceRating': 4,
        'RelationshipSatisfaction': 3,
        'StockOptionLevel': 1,
        'TrainingTimesLastYear': 3,
         'YearsSinceLastPromotion': 2, 
        'Gender': 'Male',
        'EducationField': 'Life Sciences'
    }
    return data

@router.post("/predict", response_model=PredictionResponse)
def predict_attrition(request: PredictionRequest):
    """
    Make a prediction for a single employee's attrition risk.
    
    Returns prediction with probability score and risk level.
    """
    if not load_model():
        raise HTTPException(status_code=503, detail="Model not available. Please train the model first.")
    
    try:
        # Prepare data
        prediction_data = get_prediction_data(request)
        df = pd.DataFrame([prediction_data])
        
        # Preprocess
        X_processed = _preprocessor.transform(df)
        
        # Make prediction
        prediction = _model.predict(X_processed)[0]
        probability = _model.predict_proba(X_processed)[0][1]
        
        # Determine risk level
        if probability < 0.3:
            risk_level = 'Low'
        elif probability < 0.6:
            risk_level = 'Medium'
        else:
            risk_level = 'High'
        
        # Get confidence
        confidence = float(max(_model.predict_proba(X_processed)[0]))
        
        return PredictionResponse(
            attrition_risk=bool(prediction),
            probability=float(probability),
            risk_level=risk_level,
            confidence=confidence
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")

@router.post("/predict/batch", response_model=BatchPredictionResponse)
def predict_batch(file: UploadFile = File(...), db: Session = Depends(get_db)):
    """
    Make predictions for multiple employees via CSV upload.
    
    Expected CSV columns: age, monthly_income, years_at_company, job_satisfaction, etc.
    """
    if not load_model():
        raise HTTPException(status_code=503, detail="Model not available. Please train the model first.")
    
    try:
        # Read CSV file
        content = file.file.read().decode('utf-8')
        csv_reader = csv.DictReader(StringIO(content))
        
        results = []
        errors = []
        
        for row_num, row in enumerate(csv_reader, start=2):
            try:
                # Convert row to PredictionRequest
                request = PredictionRequest(
                    age=int(row.get('age', 45)),
                    monthly_income=float(row.get('monthly_income', 5000)),
                    years_at_company=int(row.get('years_at_company', 5)),
                    years_in_current_role=int(row.get('years_in_current_role', 3)),
                    years_with_curr_manager=int(row.get('years_with_curr_manager', 2)),
                    total_working_years=int(row.get('total_working_years', 10)),
                    job_satisfaction=int(row.get('job_satisfaction', 3)),
                    work_life_balance=int(row.get('work_life_balance', 3)),
                    job_role=row.get('job_role', 'Not Specified'),
                    department=row.get('department', 'Unknown'),
                    distance_from_home=int(row.get('distance_from_home', 5)),
                    over_time=row.get('over_time', 'No'),
                )
                
                # Make prediction
                prediction_data = get_prediction_data(request)
                df = pd.DataFrame([prediction_data])
                X_processed = _preprocessor.transform(df)
                
                prediction = _model.predict(X_processed)[0]
                probability = _model.predict_proba(X_processed)[0][1]
                
                # Determine risk level
                if probability < 0.3:
                    risk_level = 'Low'
                elif probability < 0.6:
                    risk_level = 'Medium'
                else:
                    risk_level = 'High'
                
                results.append({
                    'row': row_num,
                    'employee_name': row.get('name', 'Unknown'),
                    'probability': float(probability),
                    'attrition_risk': bool(prediction),
                    'risk_level': risk_level
                })
            
            except Exception as e:
                errors.append({'row': row_num, 'error': str(e)})
        
        # Generate results file
        results_filename = f"predictions_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        results_path = Path('results') / results_filename
        results_path.parent.mkdir(exist_ok=True)
        
        # Write results to CSV
        if results:
            df_results = pd.DataFrame(results)
            df_results.to_csv(results_path, index=False)
        
        return BatchPredictionResponse(
            processed_count=len(results) + len(errors),
            success_count=len(results),
            error_count=len(errors),
            results_file=results_filename,
            download_url=f"/api/predict/batch/download/{results_filename}"
        )
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Batch processing error: {str(e)}")

@router.get("/model/metrics")
def get_model_metrics(db: Session = Depends(get_db)):
    """
    Get the latest model performance metrics.
    """
    from app.models import ModelMetrics
    
    latest_metrics = db.query(ModelMetrics).order_by(ModelMetrics.created_at.desc()).first()
    
    if not latest_metrics:
        raise HTTPException(status_code=404, detail="No model metrics found. Please train the model first.")
    
    return {
        'model_version': latest_metrics.model_version,
        'model_name': latest_metrics.model_name,
        'training_date': latest_metrics.training_date,
        'accuracy': latest_metrics.accuracy,
        'precision': latest_metrics.precision,
        'recall': latest_metrics.recall,
        'f1_score': latest_metrics.f1_score,
        'roc_auc': latest_metrics.roc_auc,
        'confusion_matrix': latest_metrics.confusion_matrix,
    }
