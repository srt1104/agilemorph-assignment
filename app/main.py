from fastapi import Depends, FastAPI
from fastapi_cache.decorator import cache
from sqlalchemy.orm import Session

from app.cache import init_cache
from app.db import get_db
from app.queries import get_departmental_performance_trends, get_employee_mobility, get_project_success_rate, get_top_performers

app = FastAPI()


@app.on_event("startup")
async def startup():
    """
    Event handler for FastAPI startup. Initializes the cache.
    """
    init_cache()


@app.get("/performance/top-performers")
@cache(expire=60)
async def read_top_performers(db: Session = Depends(get_db)):
    """
    API endpoint to retrieve the top 10 performers based on the average performance score over the last year.

    Parameters:
        db (Session): SQLAlchemy database session dependency.

    Returns:
        list: A list of top performers.
    """
    return get_top_performers(db)


@app.get("/departments/{id}/success-rate")
@cache(expire=60)
def read_department_success_rate(id: int, db: Session = Depends(get_db)):
    """
    API endpoint to calculate the success rate of projects within a department over the last two years.

    Parameters:
        department_id (int): The ID of the department.
        db (Session): SQLAlchemy database session dependency.

    Returns:
        dict: A dictionary containing the total and successful projects.
    """
    return get_project_success_rate(db, id)


@app.get("/employees/mobility")
@cache(expire=60)
def read_employee_mobility(db: Session = Depends(get_db)):
    """
    API endpoint to retrieve employees who have worked in more than one department and their average performance score.

    Parameters:
        db (Session): SQLAlchemy database session dependency.

    Returns:
        list: A list of employees with mobility details.
    """
    return get_employee_mobility(db)


@app.get("/departments/performance-trends")
@cache(expire=60)
def read_departmental_performance_trends(db: Session = Depends(get_db)):
    """
    API endpoint to analyze the performance trends of departments over the last three years, grouped by quarter.

    Parameters:
        db (Session): SQLAlchemy database session dependency.

    Returns:
        list: A list of departmental performance trends.
    """
    return get_departmental_performance_trends(db)
