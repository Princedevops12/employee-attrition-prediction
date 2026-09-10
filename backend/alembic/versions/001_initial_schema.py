"""Initial database schema creation.

Revision ID: 001_initial_schema
Revises: None
Create Date: 2026-09-10

This migration creates the initial database schema with Employee,
Prediction, and ModelMetrics tables.
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import sqlite

# revision identifiers
revision = '001_initial_schema'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Create initial database schema."""
    # Create Employee table
    op.create_table(
        'employees',
        sa.Column('id', sa.Integer, primary_key=True, index=True),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('department', sa.String(100), nullable=False),
        sa.Column('job_role', sa.String(100), nullable=False),
        sa.Column('age', sa.Integer, nullable=False),
        sa.Column('gender', sa.String(50)),
        sa.Column('monthly_income', sa.Float, nullable=False),
        sa.Column('hourly_rate', sa.Float),
        sa.Column('years_at_company', sa.Integer, nullable=False),
        sa.Column('years_in_current_role', sa.Integer),
        sa.Column('years_with_curr_manager', sa.Integer),
        sa.Column('total_working_years', sa.Integer),
        sa.Column('job_satisfaction', sa.Integer),
        sa.Column('work_life_balance', sa.Integer),
        sa.Column('distance_from_home', sa.Integer),
        sa.Column('over_time', sa.String(10)),
        sa.Column('marital_status', sa.String(50)),
        sa.Column('education_field', sa.String(100)),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime, server_default=sa.func.now(), onupdate=sa.func.now()),
    )
    
    # Create Prediction table
    op.create_table(
        'predictions',
        sa.Column('id', sa.Integer, primary_key=True, index=True),
        sa.Column('employee_id', sa.Integer, sa.ForeignKey('employees.id', ondelete='CASCADE'), nullable=False),
        sa.Column('attrition_risk', sa.Boolean, nullable=False),
        sa.Column('probability', sa.Float, nullable=False),
        sa.Column('risk_level', sa.String(20), nullable=False),
        sa.Column('confidence', sa.Float),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.now()),
    )
    
    # Create ModelMetrics table
    op.create_table(
        'model_metrics',
        sa.Column('id', sa.Integer, primary_key=True, index=True),
        sa.Column('model_version', sa.String(50), nullable=False),
        sa.Column('model_name', sa.String(100), nullable=False),
        sa.Column('training_date', sa.DateTime, nullable=False),
        sa.Column('accuracy', sa.Float),
        sa.Column('precision', sa.Float),
        sa.Column('recall', sa.Float),
        sa.Column('f1_score', sa.Float),
        sa.Column('roc_auc', sa.Float),
        sa.Column('confusion_matrix', sa.JSON),
        sa.Column('training_samples', sa.Integer),
        sa.Column('test_samples', sa.Integer),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.now()),
    )
    
    # Create indices
    op.create_index('idx_employees_department', 'employees', ['department'])
    op.create_index('idx_employees_job_role', 'employees', ['job_role'])
    op.create_index('idx_predictions_employee', 'predictions', ['employee_id'])
    op.create_index('idx_predictions_risk_level', 'predictions', ['risk_level'])
    op.create_index('idx_model_metrics_version', 'model_metrics', ['model_version'])


def downgrade() -> None:
    """Drop all tables created in upgrade."""
    # Drop indices
    op.drop_index('idx_model_metrics_version', 'model_metrics')
    op.drop_index('idx_predictions_risk_level', 'predictions')
    op.drop_index('idx_predictions_employee', 'predictions')
    op.drop_index('idx_employees_job_role', 'employees')
    op.drop_index('idx_employees_department', 'employees')
    
    # Drop tables
    op.drop_table('model_metrics')
    op.drop_table('predictions')
    op.drop_table('employees')
