"""
Model training and evaluation for Employee Attrition Prediction

This module trains multiple models and selects the best one based on validation metrics.
"""

import numpy as np
import pandas as pd
import json
from pathlib import Path
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, confusion_matrix, classification_report
)
import joblib
import warnings

# Try to import XGBoost; it's optional
try:
    import xgboost as xgb
    XGBOOST_AVAILABLE = True
except ImportError:
    XGBOOST_AVAILABLE = False
    warnings.warn("XGBoost not available. Only RandomForest will be trained.")

from preprocessing import prepare_data, save_preprocessor, PreprocessingPipeline

class ModelTrainer:
    """
    Train and evaluate multiple attrition prediction models.
    """
    
    def __init__(self, random_state=42):
        self.random_state = random_state
        self.models = {}
        self.metrics = {}
        self.best_model = None
        self.best_model_name = None
        
    def train_random_forest(self, X_train, y_train):
        """Train a RandomForest model."""
        print("\nTraining RandomForest model...")
        
        model = RandomForestClassifier(
            n_estimators=100,
            max_depth=15,
            min_samples_split=10,
            min_samples_leaf=4,
            random_state=self.random_state,
            n_jobs=-1,
            class_weight='balanced'  # Handle class imbalance
        )
        
        model.fit(X_train, y_train)
        print("RandomForest training complete!")
        
        return model
    
    def train_xgboost(self, X_train, y_train):
        """Train an XGBoost model."""
        if not XGBOOST_AVAILABLE:
            print("\nXGBoost not available. Skipping XGBoost model.")
            return None
        
        print("\nTraining XGBoost model...")
        
        model = xgb.XGBClassifier(
            n_estimators=100,
            max_depth=5,
            learning_rate=0.1,
            subsample=0.8,
            colsample_bytree=0.8,
            random_state=self.random_state,
            eval_metric='logloss',
            use_label_encoder=False,
            scale_pos_weight=(y_train == 0).sum() / (y_train == 1).sum()  # Handle imbalance
        )
        
        model.fit(X_train, y_train)
        print("XGBoost training complete!")
        
        return model
    
    def evaluate_model(self, model, X_test, y_test, model_name):
        """Evaluate a trained model."""
        print(f"\nEvaluating {model_name}...")
        
        # Predictions
        y_pred = model.predict(X_test)
        y_pred_proba = model.predict_proba(X_test)[:, 1]
        
        # Metrics
        metrics = {
            'accuracy': accuracy_score(y_test, y_pred),
            'precision': precision_score(y_test, y_pred),
            'recall': recall_score(y_test, y_pred),
            'f1_score': f1_score(y_test, y_pred),
            'roc_auc': roc_auc_score(y_test, y_pred_proba),
            'confusion_matrix': confusion_matrix(y_test, y_pred).tolist()
        }
        
        # Print metrics
        print(f"{model_name} Performance:")
        print(f"  Accuracy:  {metrics['accuracy']:.4f}")
        print(f"  Precision: {metrics['precision']:.4f}")
        print(f"  Recall:    {metrics['recall']:.4f}")
        print(f"  F1-Score:  {metrics['f1_score']:.4f}")
        print(f"  ROC-AUC:   {metrics['roc_auc']:.4f}")
        
        return metrics
    
    def train_and_evaluate(self, X_train, X_test, y_train, y_test):
        """Train all models and select the best one."""
        print("\n" + "="*60)
        print("TRAINING AND EVALUATING MODELS")
        print("="*60)
        
        # Train RandomForest
        rf_model = self.train_random_forest(X_train, y_train)
        rf_metrics = self.evaluate_model(rf_model, X_test, y_test, 'RandomForest')
        self.models['RandomForest'] = rf_model
        self.metrics['RandomForest'] = rf_metrics
        
        # Train XGBoost if available
        xgb_model = self.train_xgboost(X_train, y_train)
        if xgb_model:
            xgb_metrics = self.evaluate_model(xgb_model, X_test, y_test, 'XGBoost')
            self.models['XGBoost'] = xgb_model
            self.metrics['XGBoost'] = xgb_metrics
        
        # Select best model based on F1-score
        print("\n" + "-"*60)
        print("Model Selection")
        print("-"*60)
        
        best_f1 = -1
        for model_name, metrics in self.metrics.items():
            f1 = metrics['f1_score']
            print(f"{model_name} F1-Score: {f1:.4f}")
            if f1 > best_f1:
                best_f1 = f1
                self.best_model = self.models[model_name]
                self.best_model_name = model_name
        
        print(f"\nBest Model Selected: {self.best_model_name} (F1-Score: {best_f1:.4f})")
        
        return self.best_model, self.metrics[self.best_model_name]

def save_model_and_metrics(model, metrics, model_path='models/model.pkl', 
                          metrics_path='models/metrics.json'):
    """Save the trained model and metrics."""
    # Create models directory
    Path(model_path).parent.mkdir(parents=True, exist_ok=True)
    
    # Save model
    joblib.dump(model, model_path)
    print(f"\nModel saved to {model_path}")
    
    # Prepare metrics for JSON (convert numpy types)
    metrics_json = {}
    for key, value in metrics.items():
        if isinstance(value, np.ndarray):
            metrics_json[key] = value.tolist()
        elif isinstance(value, (np.integer, np.floating)):
            metrics_json[key] = float(value)
        else:
            metrics_json[key] = value
    
    # Save metrics
    with open(metrics_path, 'w') as f:
        json.dump(metrics_json, f, indent=2)
    print(f"Metrics saved to {metrics_path}")

def main(data_csv='data/attrition.csv'):
    """
    Main training pipeline.
    """
    print("\n" + "="*60)
    print("EMPLOYEE ATTRITION MODEL TRAINING")
    print("="*60 + "\n")
    
    # Load data
    print(f"Loading data from {data_csv}...")
    df = pd.read_csv(data_csv)
    print(f"Loaded {len(df)} records with {df.shape[1]} columns")
    
    # Prepare data
    print("\nPreparing data (splitting train/test, preprocessing)...")
    X_train, X_test, y_train, y_test, preprocessor = prepare_data(df)
    print(f"Training set: {X_train.shape[0]} samples")
    print(f"Test set: {X_test.shape[0]} samples")
    print(f"Class distribution - No: {(y_train == 0).sum()}, Yes: {(y_train == 1).sum()}")
    
    # Save preprocessor for later use
    save_preprocessor(preprocessor)
    
    # Train models
    trainer = ModelTrainer()
    best_model, best_metrics = trainer.train_and_evaluate(X_train, X_test, y_train, y_test)
    
    # Save best model and metrics
    save_model_and_metrics(best_model, best_metrics)
    
    print("\n" + "="*60)
    print("MODEL TRAINING COMPLETE")
    print("="*60 + "\n")
    
    return best_model, best_metrics

if __name__ == '__main__':
    model, metrics = main()
