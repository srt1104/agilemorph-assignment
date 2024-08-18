from fastapi import Depends, FastAPI
from fastapi_cache.decorator import cache
from sqlalchemy.orm import Session

from app.cache import init_cache
from app.db import get_db
from app.queries import get_departmental_performance_trends, get_employee_mobility, get_project_success_rate, get_top_performers

app = FastAPI()


# Initialize cache
@app.on_event("startup")
async def startup():
    init_cache()


@app.get("/performance/top-performers")
@cache(expire=60)
async def read_top_performers(db: Session = Depends(get_db)):
    return get_top_performers(db)


@app.get("/departments/{id}/success-rate")
@cache(expire=60)
def read_department_success_rate(id: int, db: Session = Depends(get_db)):
    return get_project_success_rate(db, id)


@app.get("/employees/mobility")
@cache(expire=60)
def read_employee_mobility(db: Session = Depends(get_db)):
    return get_employee_mobility(db)


@app.get("/departments/performance-trends")
@cache(expire=60)
def read_departmental_performance_trends(db: Session = Depends(get_db)):
    return get_departmental_performance_trends(db)
