import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta
from app.db import Base, get_db
from app import models
from app.queries import get_top_performers, get_project_success_rate, get_employee_mobility, get_departmental_performance_trends

# Setup in-memory SQLite database for testing
DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="module")
def db():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    yield db
    db.close()
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="module")
def populate_data(db):
    from app.models import Department, Employee, Project, EmployeePerformance

    # Create two departments
    department1 = Department(name="Engineering", location="Building A")
    department2 = Department(name="Marketing", location="Building B")
    db.add(department1)
    db.add(department2)
    db.commit()

    # Create an employee
    employee = Employee(name="John Doe", age=30, department_id=department1.id,
                        salary=60000, date_joined=datetime.now())
    db.add(employee)
    db.commit()

    # Create projects for the employee in different departments
    project1 = Project(name="Project X", start_date=datetime.now(
    ) - timedelta(days=365), end_date=datetime.now(), department_id=department1.id)
    project2 = Project(name="Project Y", start_date=datetime.now(
    ) - timedelta(days=365), end_date=datetime.now(), department_id=department2.id)
    db.add(project1)
    db.add(project2)
    db.commit()

    # Add performance records
    performance1 = EmployeePerformance(
        employee_id=employee.id, project_id=project1.id, performance_score=85.0, review_date=datetime.now())
    performance2 = EmployeePerformance(
        employee_id=employee.id, project_id=project2.id, performance_score=90.0, review_date=datetime.now())
    db.add(performance1)
    db.add(performance2)
    db.commit()

    return db


def test_get_top_performers(db, populate_data):
    result = get_top_performers(db)
    assert len(result) > 0
    assert 'id' in result[0]
    assert 'name' in result[0]
    assert 'department_name' in result[0]
    assert 'average_score' in result[0]


def test_get_project_success_rate(db, populate_data):
    result = get_project_success_rate(db, 1)
    assert result is not None
    assert 'total_projects' in result
    assert 'successful_projects' in result


def test_get_employee_mobility(db, populate_data):
    result = get_employee_mobility(db)
    assert len(result) > 0
    assert 'id' in result[0]
    assert 'name' in result[0]
    assert 'departments_count' in result[0]
    assert 'average_score' in result[0]


def test_get_departmental_performance_trends(db, populate_data):
    result = get_departmental_performance_trends(db)
    assert len(result) > 0
    assert 'department_name' in result[0]
    assert 'year' in result[0]
    assert 'quarter' in result[0]
    assert 'average_score' in result[0]
