from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

from app.db import get_db
from app.queries import get_departmental_performance_trends, get_employee_mobility, get_project_success_rate, get_top_performers

app = FastAPI()


@app.get("/performance/top-performers")
def read_top_performers(db: Session = Depends(get_db)):
    return get_top_performers(db)


@app.get("/departments/{id}/success-rate")
def read_department_success_rate(id: int, db: Session = Depends(get_db)):
    return get_project_success_rate(db, id)


@app.get("/employees/mobility")
def read_employee_mobility(db: Session = Depends(get_db)):
    return get_employee_mobility(db)


@app.get("/departments/performance-trends")
def read_departmental_performance_trends(db: Session = Depends(get_db)):
    return get_departmental_performance_trends(db)
