from datetime import datetime, timedelta
from sqlalchemy import extract, func, case

from .models import Department, Employee, EmployeePerformance, Project
from .db import SessionLocal

db = SessionLocal()


def get_top_performers():
    last_year = datetime.now() - timedelta(days=365)

    func_avg_performance_score = func.avg(
        EmployeePerformance.performance_score)

    results = db.query(
        Employee.id,
        Employee.name,
        Department.name.label('department_name'),
        func_avg_performance_score.label('average_score')
    ).join(Employee.department).join(Employee.performances).filter(EmployeePerformance.review_date >= last_year).group_by(Employee.id, Department.name).order_by(
        func_avg_performance_score.desc()
    ).limit(10).all()

    return [{
        'id': item.id,
        'name': item.name,
        'department_name': item.department_name,
        'average_score': item.average_score
    } for item in results]


def get_project_success_rate():
    two_years_ago = datetime.now() - timedelta(days=365*2)

    # Subquery to calculate the average performance score per project
    subquery = db.query(
        Project.id.label('project_id'),
        func.avg(EmployeePerformance.performance_score).label('average_score')
    ).join(Project.performances).filter(
        Project.end_date >= two_years_ago
    ).group_by(Project.id).subquery()

    # Main query to calculate the number of successful projects per department
    results = db.query(
        Department.id,
        Department.name,
        func.count(Project.id).label('total_projects'),
        func.sum(
            case(
                (subquery.c.average_score > 70, 1),
                else_=0
            )
        ).label('successful_projects')
    ).join(Department.projects).join(subquery, Project.id == subquery.c.project_id).group_by(
        Department.id, Department.name
    ).all()

    return [{
        "id": dept.id,
        "name": dept.name,
        "total_projects": dept.total_projects,
        "successful_projects": dept.successful_projects
    } for dept in results]


def get_employee_mobility():
    results = db.query(
        Employee.id,
        Employee.name,
        func.count(func.distinct(Project.department_id)
                   ).label('departments_count'),
        func.avg(EmployeePerformance.performance_score).label('average_score')
    ).join(Employee.performances).join(EmployeePerformance.project).join(Project.department).group_by(Employee.id).having(func.count(func.distinct(Project.department_id)) > 1).all()

    return [{
        "id": emp.id,
        "name": emp.name,
        "departments_count": emp.departments_count,
        "average_score": emp.average_score
    } for emp in results]


def get_departmental_performance_trends():
    three_years_ago = datetime.now() - timedelta(days=365*3)

    # Calculate quarter manually
    quarter_expr = case(
        (extract('month', EmployeePerformance.review_date) <= 3, 1),
        (extract('month', EmployeePerformance.review_date) <= 6, 2),
        (extract('month', EmployeePerformance.review_date) <= 9, 3),
        else_=4
    )

    results = db.query(
        Department.name.label('department_name'),
        extract('year', EmployeePerformance.review_date).label('year'),
        quarter_expr.label('quarter'),
        func.avg(EmployeePerformance.performance_score).label('average_score')
    ).join(Employee, Employee.department_id == Department.id).join(Employee.performances).filter(EmployeePerformance.review_date >= three_years_ago).group_by(
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
