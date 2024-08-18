import random
from datetime import datetime, timedelta
from app.models import Employee, Department, Project, EmployeePerformance
from app.db import SessionLocal


def populate_data():
    db = SessionLocal()

    # Populate Departments
    departments = [Department(name=f"Department {i}",
                              location=f"Location {i}") for i in range(10)]
    db.add_all(departments)
    db.commit()

    # Populate Employees
    employees = [Employee(name=f"Employee {i}", age=random.randint(22, 60), department_id=random.randint(1, 10), salary=random.uniform(
        30000, 70000), date_joined=datetime.now() - timedelta(days=random.randint(0, 365*5))) for i in range(200)]
    db.add_all(employees)
    db.commit()

    # Populate Projects
    projects = [Project(name=f"Project {i}", start_date=datetime.now() - timedelta(days=random.randint(0, 365*2)),
                        end_date=datetime.now() - timedelta(days=random.randint(0, 365)), department_id=random.randint(1, 10)) for i in range(50)]
    db.add_all(projects)
    db.commit()

    # Populate Employee Performance
    existing_combinations = set()
    performances = []

    for _ in range(500):
        employee_id = random.randint(1, 200)
        project_id = random.randint(1, 50)

        # Ensure unique combination of employee_id and project_id
        if (employee_id, project_id) not in existing_combinations:
            performance = EmployeePerformance(
                employee_id=employee_id,
                project_id=project_id,
                performance_score=random.uniform(50, 100),
                review_date=datetime.now() - timedelta(days=random.randint(0, 365))
            )
            performances.append(performance)
            existing_combinations.add((employee_id, project_id))

    db.add_all(performances)
    db.commit()


if __name__ == "__main__":
    populate_data()
    print("Database seeded!")
