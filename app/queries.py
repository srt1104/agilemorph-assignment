from datetime import datetime, timedelta
from sqlalchemy import extract, func, case
from sqlalchemy.orm import Session

from app.models import Department, Employee, EmployeePerformance, Project


def get_top_performers(db: Session):
    """
    Retrieves the top 10 performers based on the average performance score over the last year.

    Parameters:
        db (Session): SQLAlchemy database session.

    Returns:
        list: A list of dictionaries containing the top performers' details.
    """
    last_year = datetime.now() - timedelta(days=365)

    subquery = db.query(
        EmployeePerformance.employee_id,
        func.avg(EmployeePerformance.performance_score).label('average_score')
    ).filter(EmployeePerformance.review_date >= last_year).group_by(EmployeePerformance.employee_id).subquery()

    results = db.query(
        Employee.id,
        Employee.name,
        Department.name.label('department_name'),
        subquery.c.average_score
    ).join(Employee.department).join(subquery, Employee.id == subquery.c.employee_id).order_by(
        subquery.c.average_score.desc()
    ).limit(10).all()

    return [{
        'id': item.id,
        'name': item.name,
        'department_name': item.department_name,
        'average_score': item.average_score
    } for item in results]


def get_project_success_rate(db: Session, department_id: int):
    """
    Calculates the success rate of projects within a department over the last two years.

    Parameters:
        db (Session): SQLAlchemy database session.
        department_id (int): The ID of the department.

    Returns:
        dict: A dictionary containing the total number of projects and the number of successful projects.
    """
    two_years_ago = datetime.now() - timedelta(days=365*2)

    subquery = db.query(
        Project.id.label('project_id'),
        func.avg(EmployeePerformance.performance_score).label('average_score')
    ).join(EmployeePerformance, Project.id == EmployeePerformance.project_id).filter(
        Project.end_date >= two_years_ago,
        Project.department_id == department_id
    ).group_by(Project.id).subquery()

    result = db.query(
        func.count(subquery.c.project_id).label('total_projects'),
        func.sum(case((subquery.c.average_score > 70, 1), else_=0)
                 ).label('successful_projects')
    ).first()

    if result:
        return {
            "total_projects": result.total_projects,
            "successful_projects": result.successful_projects
        }
    else:
        return None


def get_employee_mobility(db: Session):
    """
    Retrieves employees who have worked in more than one department and their average performance score.

    Parameters:
        db (Session): SQLAlchemy database session.

    Returns:
        list: A list of dictionaries containing employee mobility details.
    """
    results = db.query(
        Employee.id,
        Employee.name,
        func.count(func.distinct(Project.department_id)
                   ).label('departments_count'),
        func.avg(EmployeePerformance.performance_score).label('average_score')
    ).join(Employee.performances).join(EmployeePerformance.project).group_by(Employee.id).having(
        func.count(func.distinct(Project.department_id)) > 1
    ).all()

    return [{
        "id": emp.id,
        "name": emp.name,
        "departments_count": emp.departments_count,
        "average_score": emp.average_score
    } for emp in results]


def get_departmental_performance_trends(db: Session):
    """
    Analyzes the performance trends of departments over the last three years, grouped by quarter.

    Parameters:
        db (Session): SQLAlchemy database session.

    Returns:
        list: A list of dictionaries containing departmental performance trends.
    """
    three_years_ago = datetime.now() - timedelta(days=365*3)

    quarter_expr = case(
        (extract('month', EmployeePerformance.review_date).between(1, 3), 1),
        (extract('month', EmployeePerformance.review_date).between(4, 6), 2),
        (extract('month', EmployeePerformance.review_date).between(7, 9), 3),
        (extract('month', EmployeePerformance.review_date).between(10, 12), 4)
    )

    results = db.query(
        Department.name.label('department_name'),
        extract('year', EmployeePerformance.review_date).label('year'),
        quarter_expr.label('quarter'),
        func.avg(EmployeePerformance.performance_score).label('average_score')
    ).join(Employee, Employee.department_id == Department.id).join(Employee.performances).filter(
        EmployeePerformance.review_date >= three_years_ago
    ).group_by(
        Department.name,
        extract('year', EmployeePerformance.review_date),
        quarter_expr
    ).order_by(
        Department.name,
        extract('year', EmployeePerformance.review_date),
        quarter_expr
    ).all()

    return [{
        'department_name': item.department_name,
        'year': item.year,
        'quarter': item.quarter,
        'average_score': item.average_score
    } for item in results]
