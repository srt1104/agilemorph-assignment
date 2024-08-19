from sqlalchemy import Column, Integer, String, ForeignKey, Float, Date, UniqueConstraint
from sqlalchemy.orm import relationship
from .db import Base


class Employee(Base):
    """
    Represents an employee in the company.

    Attributes:
        id (int): Unique identifier for the employee.
        name (str): Full name of the employee.
        age (int): Age of the employee.
        department_id (int): Foreign key to the department the employee belongs to.
        salary (float): Salary of the employee.
        date_joined (date): The date when the employee joined the company.
    """
    __tablename__ = 'employees'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    age = Column(Integer)
    department_id = Column(Integer, ForeignKey('departments.id'), index=True)
    salary = Column(Float)
    date_joined = Column(Date)

    department = relationship("Department", back_populates="employees")
    performances = relationship(
        "EmployeePerformance", back_populates="employee")


class Department(Base):
    """
    Represents a department within the company.

    Attributes:
        id (int): Unique identifier for the department.
        name (str): The name of the department.
        location (str): The location of the department.
    """
    __tablename__ = 'departments'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    location = Column(String)

    employees = relationship("Employee", back_populates="department")
    projects = relationship("Project", back_populates="department")


class Project(Base):
    """
    Represents a project within the company.

    Attributes:
        id (int): Unique identifier for the project.
        name (str): The name of the project.
        start_date (date): The start date of the project.
        end_date (date): The end date of the project.
        department_id (int): Foreign key to the department that owns the project.
    """
    __tablename__ = 'projects'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    start_date = Column(Date)
    end_date = Column(Date)
    department_id = Column(Integer, ForeignKey('departments.id'))

    department = relationship("Department", back_populates="projects")
    performances = relationship(
        "EmployeePerformance", back_populates="project")


class EmployeePerformance(Base):
    """
    Represents an employee's performance on a specific project.

    Attributes:
        id (int): Unique identifier for the performance record.
        employee_id (int): Foreign key to the employee.
        project_id (int): Foreign key to the project.
        performance_score (float): The performance score of the employee on the project.
        review_date (date): The date when the performance was reviewed.
    """
    __tablename__ = 'employee_performance'
    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey('employees.id'), index=True)
    project_id = Column(Integer, ForeignKey('projects.id'), index=True)
    performance_score = Column(Float)
    review_date = Column(Date, index=True)

    __table_args__ = (UniqueConstraint(
        'employee_id', 'project_id', name='_employee_project_uc'),)

    employee = relationship("Employee", back_populates="performances")
    project = relationship("Project", back_populates="performances")
