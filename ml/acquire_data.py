"""
Dataset acquisition and initial exploration for Employee Attrition Prediction

The IBM HR Analytics Employee Attrition & Performance dataset is a publicly available
dataset with ~1,470 employee records and 34 features including the target variable.

If the dataset cannot be downloaded from Kaggle, this script can generate a 
synthetic dataset with the same schema.
"""

import os
import pandas as pd
import numpy as np
import json
from pathlib import Path

# Set random seed for reproducibility
np.random.seed(42)

def generate_synthetic_data(n_records=1470):
    """
    Generate synthetic employee attrition dataset if real data unavailable.
    This matches the schema of the IBM HR Analytics dataset.
    """
    print(f"Generating synthetic dataset with {n_records} records...")
    
    # Define departments and job roles
    departments = ['Sales', 'Research & Development', 'Human Resources']
    job_roles = [
        'Sales Executive', 'Research Scientist', 'Laboratory Technician',
        'Manufacturing Director', 'Healthcare Representative', 'Manager',
        'Reseach Director', 'Sales Representative', 'Human Resources'
    ]
    education_field = ['Life Sciences', 'Medical', 'Other', 'Technical Degree', 'Human Resources']
    job_satisfaction_levels = [1, 2, 3, 4]  # Low to High
    work_life_balance_levels = [1, 2, 3, 4]  # Bad to Best
    
    data = {
        'EmployeeNumber': np.arange(1001, 1001 + n_records),
        'Age': np.random.randint(18, 66, n_records),
        'Attrition': np.random.choice(['Yes', 'No'], n_records, p=[0.16, 0.84]),  # ~16% attrition rate
        'Department': np.random.choice(departments, n_records),
        'DistanceFromHome': np.random.randint(1, 30, n_records),
        'Education': np.random.randint(1, 5, n_records),
        'EducationField': np.random.choice(education_field, n_records),
        'EmployeeCount': np.full(n_records, 1),  # Always 1 in this dataset
        'EnvironmentSatisfaction': np.random.randint(1, 5, n_records),
        'Gender': np.random.choice(['Female', 'Male'], n_records),
        'HourlyRate': np.random.randint(30, 100, n_records),
        'JobInvolvement': np.random.randint(1, 4, n_records),
        'JobLevel': np.random.randint(1, 5, n_records),
        'JobRole': np.random.choice(job_roles, n_records),
        'JobSatisfaction': np.random.choice(job_satisfaction_levels, n_records),
        'MaritalStatus': np.random.choice(['Single', 'Married', 'Divorced'], n_records),
        'MonthlyIncome': np.random.randint(1009, 19999, n_records),
        'MonthlyRate': np.random.randint(2092, 26997, n_records),
        'NumCompaniesWorked': np.random.randint(0, 9, n_records),
        'Over18': np.full(n_records, 'Y'),
        'OverTime': np.random.choice(['Yes', 'No'], n_records),
        'PercentSalaryHike': np.random.randint(11, 26, n_records),
        'PerformanceRating': np.random.randint(3, 5, n_records),
        'RelationshipSatisfaction': np.random.randint(1, 4, n_records),
        'StandardHours': np.full(n_records, 8),
        'StockOptionLevel': np.random.randint(0, 4, n_records),
        'TotalWorkingYears': np.random.randint(0, 41, n_records),
        'TrainingTimesLastYear': np.random.randint(0, 7, n_records),
        'WorkLifeBalance': np.random.choice(work_life_balance_levels, n_records),
        'YearsAtCompany': np.random.randint(0, 41, n_records),
        'YearsInCurrentRole': np.random.randint(0, 19, n_records),
        'YearsSinceLastPromotion': np.random.randint(0, 16, n_records),
        'YearsWithCurrManager': np.random.randint(0, 18, n_records),
    }
    
    df = pd.DataFrame(data)
    
    # Add some correlation to make it more realistic
    # Higher attrition for those with more distance from home, lower satisfaction, etc.
    for idx in df[df['Attrition'] == 'Yes'].index:
        if np.random.random() > 0.5:
            df.loc[idx, 'DistanceFromHome'] = np.random.randint(15, 30)
        if np.random.random() > 0.5:
            df.loc[idx, 'JobSatisfaction'] = np.random.choice([1, 2])
        if np.random.random() > 0.5:
            df.loc[idx, 'WorkLifeBalance'] = np.random.choice([1, 2])
    
    return df

def load_or_create_dataset(data_dir='data'):
    """
    Load the dataset from disk or generate synthetic data if not found.
    """
    data_path = Path(data_dir)
    data_path.mkdir(exist_ok=True)
    
    csv_file = data_path / 'attrition.csv'
    
    if csv_file.exists():
        print(f"Loading existing dataset from {csv_file}")
        df = pd.read_csv(csv_file)
    else:
        print(f"Dataset not found at {csv_file}")
        print("Creating synthetic dataset instead...")
        df = generate_synthetic_data()
        df.to_csv(csv_file, index=False)
        print(f"Dataset saved to {csv_file}")
    
    return df, data_path

def explore_data(df):
    """
    Perform exploratory data analysis on the dataset.
    """
    print("\n" + "="*60)
    print("EXPLORATORY DATA ANALYSIS")
    print("="*60 + "\n")
    
    # Basic info
    print("Dataset Shape:")
    print(f"  Rows: {df.shape[0]}")
    print(f"  Columns: {df.shape[1]}\n")
    
    # Data types
    print("Data Types:")
    print(df.dtypes.value_counts().to_string())
    print()
    
    # Missing values
    print("Missing Values:")
    missing = df.isnull().sum()
    if missing.sum() == 0:
        print("  No missing values found")
    else:
        print(missing[missing > 0].to_string())
    print()
    
    # Target variable distribution
    print("Target Variable Distribution (Attrition):")
    attrition_counts = df['Attrition'].value_counts()
    attrition_pct = df['Attrition'].value_counts(normalize=True) * 100
    for val in ['No', 'Yes']:
        if val in attrition_counts.index:
            count = attrition_counts[val]
            pct = attrition_pct[val]
            print(f"  {val}: {count} ({pct:.2f}%)")
    print()
    
    # Numeric columns summary
    print("Numeric Columns Summary:")
    print(df.describe().to_string())
    print()
    
    # Categorical columns
    categorical_cols = df.select_dtypes(include=['object']).columns
    print(f"Categorical Columns: {', '.join(categorical_cols)}")
    for col in categorical_cols:
        if col != 'Attrition':  # Skip target variable
            print(f"\n  {col}:")
            print(f"    Unique values: {df[col].nunique()}")
            print(f"    Values: {df[col].unique().tolist()}")
    print()
    
    return {
        'shape': df.shape,
        'dtypes': df.dtypes.to_dict(),
        'missing_values': df.isnull().sum().to_dict(),
        'attrition_distribution': df['Attrition'].value_counts().to_dict(),
        'numeric_summary': df.describe().to_dict(),
        'categorical_columns': categorical_cols.tolist()
    }

def save_eda_report(eda_results, data_dir='data'):
    """
    Save EDA results to a JSON file for reference.
    """
    report_path = Path(data_dir) / 'eda_report.json'
    
    # Convert numpy types to JSON-serializable types
    report = {}
    for key, value in eda_results.items():
        if isinstance(value, dict):
            report[key] = {k: (int(v) if isinstance(v, (np.integer, np.int64)) else v) 
                          for k, v in value.items()}
        elif isinstance(value, list):
            report[key] = value
        else:
            report[key] = value
    
    with open(report_path, 'w') as f:
        json.dump(report, f, indent=2, default=str)
    
    print(f"EDA report saved to {report_path}")

def main():
    """
    Main execution function.
    """
    print("\n" + "="*60)
    print("EMPLOYEE ATTRITION DATASET ACQUISITION & EDA")
    print("="*60 + "\n")
    
    # Load or create dataset
    df, data_dir = load_or_create_dataset('data')
    
    # Explore data
    eda_results = explore_data(df)
    
    # Save EDA report
    save_eda_report(eda_results, 'data')
    
    print("="*60)
    print("EDA Complete! Dataset is ready for preprocessing.")
    print("="*60 + "\n")
    
    return df

if __name__ == '__main__':
    df = main()
