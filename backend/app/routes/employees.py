"""
Employee management endpoints.
"""

from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models import Employee, Prediction
from app.schemas import EmployeeCreate, EmployeeResponse, EmployeeUpdate, EmployeeWithPredictions

router = APIRouter()

@router.post("/employees", response_model=EmployeeResponse)
def create_employee(employee: EmployeeCreate, db: Session = Depends(get_db)):
    """
    Create a new employee record.
    """
    db_employee = Employee(**employee.model_dump())
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)
    return db_employee

@router.get("/employees", response_model=List[EmployeeResponse])
def list_employees(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    department: str = Query(None),
    db: Session = Depends(get_db)
):
    """
    List all employee records with optional filtering.
    """
    query = db.query(Employee)
    
    if department:
        query = query.filter(Employee.department == department)
    
    employees = query.offset(skip).limit(limit).all()
    return employees

@router.get("/employees/{employee_id}", response_model=EmployeeWithPredictions)
def get_employee(employee_id: int, db: Session = Depends(get_db)):
    """
    Get a specific employee record with latest prediction.
    """
    db_employee = db.query(Employee).filter(Employee.id == employee_id).first()
    
    if not db_employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    # Get latest prediction
    latest_prediction = db.query(Prediction).filter(
        Prediction.employee_id == employee_id
    ).order_by(Prediction.created_at.desc()).first()
    
    response = EmployeeWithPredictions(**{
        **db_employee.__dict__,
        'latest_prediction': latest_prediction
    })
    
    return response

@router.put("/employees/{employee_id}", response_model=EmployeeResponse)
def update_employee(
    employee_id: int,
    employee_update: EmployeeUpdate,
    db: Session = Depends(get_db)
):
    """
    Update an employee record.
    """
    db_employee = db.query(Employee).filter(Employee.id == employee_id).first()
    
    if not db_employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    # Update only provided fields
    update_data = employee_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_employee, field, value)
    
    db.commit()
    db.refresh(db_employee)
    return db_employee

@router.delete("/employees/{employee_id}")
def delete_employee(employee_id: int, db: Session = Depends(get_db)):
    """
    Delete an employee record.
    """
    db_employee = db.query(Employee).filter(Employee.id == employee_id).first()
    
    if not db_employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    db.delete(db_employee)
    db.commit()
    
    return {"detail": f"Employee {employee_id} deleted successfully"}

@router.get("/employees/department/{department}/stats")
def get_department_stats(department: str, db: Session = Depends(get_db)):
    """
    Get statistics for a specific department.
    """
    employees = db.query(Employee).filter(Employee.department == department).all()
    
    if not employees:
        raise HTTPException(status_code=404, detail="No employees in this department")
    
    # Calculate statistics
    at_risk_count = 0
    for emp in employees:
        latest_pred = db.query(Prediction).filter(
            Prediction.employee_id == emp.id
        ).order_by(Prediction.created_at.desc()).first()
        
        if latest_pred and latest_pred.attrition_risk:
            at_risk_count += 1
    
    avg_income = sum(e.monthly_income for e in employees) / len(employees)
    avg_tenure = sum(e.years_at_company for e in employees) / len(employees)
    
    return {
        'department': department,
        'total_employees': len(employees),
        'at_risk_count': at_risk_count,
        'at_risk_percentage': (at_risk_count / len(employees) * 100) if employees else 0,
        'average_income': avg_income,
        'average_tenure': avg_tenure
    }
