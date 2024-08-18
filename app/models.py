from sqlalchemy import Column, Integer, String, ForeignKey, Float, Date
from sqlalchemy.orm import relationship
from .db import Base

class Employee(Base):
    __tablename__ = 'employees'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    age = Column(Integer)
    department_id = Column(Integer, ForeignKey('departments.id'))
    salary = Column(Float)
    date_joined = Column(Date)
    
    department = relationship("Department", back_populates="employees")
    performances = relationship("EmployeePerformance", back_populates="employee")

class Department(Base):
    __tablename__ = 'departments'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    location = Column(String)
    
    employees = relationship("Employee", back_populates="department")
    projects = relationship("Project", back_populates="department")

class Project(Base):
    __tablename__ = 'projects'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    start_date = Column(Date)
    end_date = Column(Date)
    department_id = Column(Integer, ForeignKey('departments.id'))
    
    department = relationship("Department", back_populates="projects")
    performances = relationship("EmployeePerformance", back_populates="project")

class EmployeePerformance(Base):
    __tablename__ = 'employee_performance'
    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey('employees.id'))
    project_id = Column(Integer, ForeignKey('projects.id'))
    performance_score = Column(Float)
    review_date = Column(Date)
    
    employee = relationship("Employee", back_populates="performances")
    project = relationship("Project", back_populates="performances")
