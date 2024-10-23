from src.models.employees import Employees
from src.__init__ import db

# Get all employees from Employees table
def get_all():
    employee_list = db.session.scalars(db.select(Employees)).all()
    return employee_list

# Get all departments from Employees table
def get_departments_list():
    departments_list = db.session.scalars(
        db.select(Employees.dept).distinct()
    ).all()
    return departments_list

# Get staff member from Employees table
def find_by_staff_id(staff_id_num):
    employee = db.session.scalars(
        db.select(Employees).filter_by(staff_id=staff_id_num).
        limit(1)
    ).first()

    return employee

# Get all employees in a specific team from Employee table
def find_by_team(reporting_manager_id_num):

    team_manager = db.session.scalars(
        db.select(Employees).filter_by(staff_id=reporting_manager_id_num).
        limit(1)
    ).first()

    if not team_manager:
        return None, []

    team_list = db.session.scalars(
        db.select(Employees).filter_by(reporting_manager=reporting_manager_id_num)).all()
    
    return team_manager, team_list

# Get all employees in a specific department from Employees table
def find_by_dept(dept_name):
    dept_list = db.session.scalars(
        db.select(Employees).filter_by(dept=dept_name)).all()
    
    return dept_list

# Get all employees with a specific role from Employees table
def find_by_role(role_num):
    role_list = db.session.scalars(
        db.select(Employees).filter_by(role=role_num)).all()
    
    return role_list

# Get specific employee from given email from Employees table
def find_by_email(email):
    employee = db.session.scalars(
    	db.select(Employees).filter_by(email=email).
    	limit(1)
        ).first()
    
    return employee