"""
Model inference script for making predictions on new employee data.

This script loads the trained model and preprocessor to make attrition predictions.
"""

import joblib
import pandas as pd
import numpy as np
from pathlib import Path

class AttritionPredictor:
    """
    Load trained model and preprocessor for making predictions.
    """
    
    def __init__(self, model_path='models/model.pkl', preprocessor_path='models/preprocessor.pkl'):
        """Load the model and preprocessor."""
        if not Path(model_path).exists():
            raise FileNotFoundError(f"Model not found at {model_path}. Train the model first using train.py")
        
        if not Path(preprocessor_path).exists():
            raise FileNotFoundError(f"Preprocessor not found at {preprocessor_path}. Train the model first.")
        
        self.model = joblib.load(model_path)
        self.preprocessor = joblib.load(preprocessor_path)
        print("Model and preprocessor loaded successfully")
    
    def predict_single(self, employee_data):
        """
        Make a prediction for a single employee.
        
        Args:
            employee_data: Dictionary with employee features
            
        Returns:
            Dictionary with prediction results
        """
        # Convert to DataFrame
        df = pd.DataFrame([employee_data])
        
        # Preprocess
        X_processed = self.preprocessor.transform(df)
        
        # Predict
        prediction = self.model.predict(X_processed)[0]
        probability = self.model.predict_proba(X_processed)[0][1]
        
        # Determine risk level
        if probability < 0.3:
            risk_level = 'Low'
        elif probability < 0.6:
            risk_level = 'Medium'
        else:
            risk_level = 'High'
        
        return {
            'attrition_risk': bool(prediction),
            'probability': float(probability),
            'risk_level': risk_level,
            'confidence': float(max(self.model.predict_proba(X_processed)[0]))
        }
    
    def predict_batch(self, df):
        """
        Make predictions for multiple employees.
        
        Args:
            df: DataFrame with employee records
            
        Returns:
            DataFrame with predictions added
        """
        # Preprocess
        X_processed = self.preprocessor.transform(df)
        
        # Predict
        predictions = self.model.predict(X_processed)
        probabilities = self.model.predict_proba(X_processed)[:, 1]
        
        # Add results to dataframe
        result_df = df.copy()
        result_df['Attrition_Predicted'] = predictions
        result_df['Probability'] = probabilities
        result_df['Risk_Level'] = pd.cut(
            probabilities,
            bins=[0, 0.3, 0.6, 1.0],
            labels=['Low', 'Medium', 'High']
        )
        
        return result_df

def test_prediction():
    """
    Test the predictor with sample data.
    """
    print("\nTesting AttritionPredictor...")
    
    try:
        predictor = AttritionPredictor()
        
        # Sample employee
        sample_employee = {
            'Age': 45,
            'DistanceFromHome': 5,
            'Education': 3,
            'EnvironmentSatisfaction': 3,
            'HourlyRate': 65,
            'JobInvolvement': 2,
            'JobLevel': 2,
            'JobRole': 'Sales Executive',
            'JobSatisfaction': 3,
            'Department': 'Sales',
            'MaritalStatus': 'Married',
            'MonthlyIncome': 5500,
            'MonthlyRate': 5500,
            'NumCompaniesWorked': 2,
            'OverTime': 'No',
            'PercentSalaryHike': 13,
            'PerformanceRating': 4,
            'RelationshipSatisfaction': 3,
            'StockOptionLevel': 1,
            'TotalWorkingYears': 12,
            'TrainingTimesLastYear': 3,
            'WorkLifeBalance': 3,
            'YearsAtCompany': 5,
            'YearsInCurrentRole': 3,
            'YearsSinceLastPromotion': 2,
            'YearsWithCurrManager': 2,
            'Gender': 'Female',
            'EducationField': 'Life Sciences'
        }
        
        result = predictor.predict_single(sample_employee)
        print(f"Prediction for sample employee:")
        print(f"  Attrition Risk: {result['attrition_risk']}")
        print(f"  Probability: {result['probability']:.2%}")
        print(f"  Risk Level: {result['risk_level']}")
        print(f"  Confidence: {result['confidence']:.2%}")
        
    except FileNotFoundError as e:
        print(f"Cannot test: {e}")
        print("Run train.py first to generate the model.")

if __name__ == '__main__':
    test_prediction()
