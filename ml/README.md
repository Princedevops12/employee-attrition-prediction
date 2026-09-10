# ML Module - Employee Attrition Prediction Model

This module contains the machine learning pipeline for employee attrition prediction.

## Directory Structure

```
ml/
├── venv/                  # Python virtual environment
├── requirements.txt       # Python dependencies
├── data/
│   └── attrition.csv     # IBM HR Analytics dataset
├── notebooks/
│   └── eda.ipynb         # Exploratory Data Analysis
├── src/
│   ├── preprocessing.py  # Data preprocessing pipeline
│   ├── train.py          # Model training script
│   └── evaluate.py       # Model evaluation
└── models/
    ├── model.pkl         # Trained model
    ├── preprocessor.pkl  # Data preprocessor
    └── metrics.json      # Performance metrics
```

## Dataset

The project uses the IBM HR Analytics Employee Attrition & Performance dataset:
- **Source**: Kaggle (publicly available)
- **Rows**: ~1,470 employees
- **Columns**: 34 (features + target)
- **Target Variable**: Attrition (Yes/No)

## Setup

1. Create and activate virtual environment:
   ```bash
   python -m venv venv
   ./venv/Scripts/activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run exploratory analysis:
   ```bash
   jupyter notebook notebooks/eda.ipynb
   ```

## Model Development

### Preprocessing Pipeline

The preprocessing pipeline handles:
- Missing value imputation
- Categorical encoding (OneHotEncoder, LabelEncoder)
- Feature scaling (StandardScaler)
- Train/test split (80/20 with stratification)
- Class imbalance handling (if needed)

### Model Training

Two models are tested:
1. **RandomForestClassifier** - Ensemble method with good interpretability
2. **XGBoost** - Gradient boosting for potentially better performance

The model with better validation metrics (F1-score, ROC-AUC) is selected.

### Model Evaluation

Metrics tracked:
- **Accuracy**: Overall correctness
- **Precision**: Positive prediction accuracy
- **Recall**: Coverage of actual positives
- **F1-Score**: Harmonic mean of precision/recall
- **ROC-AUC**: Area under the receiver operating characteristic curve
- **Confusion Matrix**: Breakdown of predictions

### Running the Pipeline

```bash
# Full pipeline: preprocessing -> training -> evaluation
python src/train.py

# View evaluation results
cat models/metrics.json
```

## Model Serialization

Models are saved using joblib:

```python
import joblib

# Save
joblib.dump(model, 'models/model.pkl')
joblib.dump(preprocessor, 'models/preprocessor.pkl')

# Load
model = joblib.load('models/model.pkl')
preprocessor = joblib.load('models/preprocessor.pkl')
```

## Making Predictions

Example workflow:

```python
import joblib
import pandas as pd

# Load model and preprocessor
model = joblib.load('models/model.pkl')
preprocessor = joblib.load('models/preprocessor.pkl')

# Prepare employee data
employee_data = pd.DataFrame({
    'Age': [45],
    'YearsAtCompany': [10],
    'Department': ['Sales'],
    'MonthlyIncome': [5000],
    # ... other features
})

# Preprocess
X_processed = preprocessor.transform(employee_data)

# Predict
prediction = model.predict(X_processed)
probability = model.predict_proba(X_processed)[0][1]

print(f"Attrition Risk: {probability:.2%}")
```

## Feature Importance

Top features influencing attrition:
(To be populated after training)

## Performance Baseline

Target metrics:
- **Accuracy**: > 85%
- **ROC-AUC**: > 0.80
- **F1-Score**: > 0.75

## Dependencies

See `requirements.txt` for the complete list:
- pandas: Data manipulation
- numpy: Numerical computing
- scikit-learn: Machine learning algorithms
- xgboost: Gradient boosting
- joblib: Model serialization
- matplotlib/seaborn: Visualization
- jupyter: Interactive notebooks

## Development Notes

- All data preprocessing is encapsulated in a scikit-learn Pipeline for reproducibility
- Random state is fixed for reproducible results
- Model and preprocessor are saved together as artifacts
- The preprocessor is used by the backend API for inference
