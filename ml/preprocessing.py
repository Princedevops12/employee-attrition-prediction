"""
Data preprocessing pipeline for Employee Attrition Prediction

This module implements the preprocessing pipeline that will be used both during
model training and during inference via the FastAPI backend.
"""

import numpy as np
import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, LabelEncoder, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.model_selection import train_test_split
import joblib
from pathlib import Path

class PreprocessingPipeline:
    """
    Scikit-learn compatible preprocessing pipeline for employee data.
    """
    
    def __init__(self):
        """Initialize the preprocessing pipeline."""
        self.pipeline = None
        self.label_encoder = None
        self.feature_columns = None
        self.target_column = 'Attrition'
        
    def create_pipeline(self):
        """
        Create the preprocessing pipeline with column transformers.
        """
        # Define numeric and categorical columns
        numeric_features = [
            'Age', 'DistanceFromHome', 'Education', 'EnvironmentSatisfaction',
            'HourlyRate', 'JobInvolvement', 'JobLevel', 'JobSatisfaction',
            'MonthlyIncome', 'MonthlyRate', 'NumCompaniesWorked',
            'PercentSalaryHike', 'PerformanceRating', 'RelationshipSatisfaction',
            'StockOptionLevel', 'TotalWorkingYears', 'TrainingTimesLastYear',
            'WorkLifeBalance', 'YearsAtCompany', 'YearsInCurrentRole',
            'YearsSinceLastPromotion', 'YearsWithCurrManager'
        ]
        
        categorical_features = [
            'Department', 'EducationField', 'Gender', 'JobRole',
            'MaritalStatus', 'OverTime'
        ]
        
        # Create transformers
        numeric_transformer = StandardScaler()
        categorical_transformer = OneHotEncoder(
            handle_unknown='ignore',
            sparse_output=False,
            drop='first'  # Avoid multicollinearity
        )
        
        # Combine transformers
        preprocessor = ColumnTransformer(
            transformers=[
                ('num', numeric_transformer, numeric_features),
                ('cat', categorical_transformer, categorical_features)
            ],
            remainder='drop'
        )
        
        self.pipeline = preprocessor
        self.feature_columns = numeric_features + categorical_features
        return self.pipeline
    
    def fit(self, X):
        """Fit the preprocessing pipeline."""
        if self.pipeline is None:
            self.create_pipeline()
        self.pipeline.fit(X)
        return self
    
    def transform(self, X):
        """Transform data using the fitted pipeline."""
        if self.pipeline is None:
            raise ValueError("Pipeline not fitted yet. Call fit() first.")
        return self.pipeline.transform(X)
    
    def fit_transform(self, X):
        """Fit and transform in one step."""
        if self.pipeline is None:
            self.create_pipeline()
        return self.pipeline.fit_transform(X)

def prepare_data(df, test_size=0.2, random_state=42):
    """
    Prepare data for model training.
    
    Args:
        df: Input DataFrame
        test_size: Proportion of data to use for testing
        random_state: Random state for reproducibility
        
    Returns:
        Tuple of (X_train, X_test, y_train, y_test, preprocessor)
    """
    # Separate features and target
    target_column = 'Attrition'
    
    # Encode target variable
    y = (df[target_column] == 'Yes').astype(int)  # 1 for Yes, 0 for No
    
    # Select feature columns (exclude target and identifiers)
    exclude_cols = [target_column, 'EmployeeNumber', 'Over18', 'EmployeeCount', 'StandardHours']
    X = df.drop(columns=exclude_cols, errors='ignore')
    
    # Create and fit preprocessor
    preprocessor = PreprocessingPipeline()
    preprocessor.fit(X)
    
    # Transform data
    X_processed = preprocessor.transform(X)
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X_processed, y,
        test_size=test_size,
        random_state=random_state,
        stratify=y  # Maintain class distribution
    )
    
    return X_train, X_test, y_train, y_test, preprocessor

def save_preprocessor(preprocessor, save_path='models/preprocessor.pkl'):
    """Save the fitted preprocessor."""
    Path(save_path).parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(preprocessor, save_path)
    print(f"Preprocessor saved to {save_path}")

def load_preprocessor(save_path='models/preprocessor.pkl'):
    """Load a saved preprocessor."""
    return joblib.load(save_path)

if __name__ == '__main__':
    # Test the preprocessing pipeline
    print("\nTesting preprocessing pipeline...")
    
    # Create sample data
    sample_data = pd.DataFrame({
        'EmployeeNumber': [1001, 1002],
        'Age': [35, 45],
        'DistanceFromHome': [5, 10],
        'Education': [3, 4],
        'EnvironmentSatisfaction': [2, 3],
        'HourlyRate': [50, 60],
        'JobInvolvement': [2, 3],
        'JobLevel': [2, 3],
        'JobRole': ['Sales Executive', 'Manager'],
        'JobSatisfaction': [3, 4],
        'Department': ['Sales', 'Research & Development'],
        'MaritalStatus': ['Married', 'Single'],
        'MonthlyIncome': [5000, 6000],
        'MonthlyRate': [5000, 6000],
        'NumCompaniesWorked': [2, 3],
        'Over18': ['Y', 'Y'],
        'OverTime': ['No', 'Yes'],
        'PercentSalaryHike': [15, 12],
        'PerformanceRating': [4, 3],
        'RelationshipSatisfaction': [2, 3],
        'StandardHours': [8, 8],
        'StockOptionLevel': [1, 2],
        'TotalWorkingYears': [10, 15],
        'TrainingTimesLastYear': [3, 4],
        'WorkLifeBalance': [3, 2],
        'YearsAtCompany': [5, 8],
        'YearsInCurrentRole': [3, 5],
        'YearsSinceLastPromotion': [2, 3],
        'YearsWithCurrManager': [2, 4],
        'Gender': ['Female', 'Male'],
        'EducationField': ['Life Sciences', 'Medical'],
        'Attrition': ['No', 'Yes']
    })
    
    # Create preprocessor
    preprocessor = PreprocessingPipeline()
    
    # Fit on sample data
    X_sample = sample_data.drop(columns=['EmployeeNumber', 'Over18', 'EmployeeCount', 
                                         'StandardHours', 'Attrition'], errors='ignore')
    preprocessor.fit(X_sample)
    
    # Transform
    X_transformed = preprocessor.transform(X_sample)
    
    print(f"Original shape: {X_sample.shape}")
    print(f"Transformed shape: {X_transformed.shape}")
    print("Pipeline test successful!")
