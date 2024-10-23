from src.models.employees import Employees


class Employees_Service:
    def __init__(self, db):
        self.db = db

    # Get all employees from Employees table
    def get_all(self):
        employee_list = self.db.session.scalars(self.db.select(Employees)).all()
        return employee_list

    # Get all departments from Employees table
    def get_departments_list(self):
        departments_list = self.db.session.scalars(
            self.db.select(Employees.dept).distinct()
        ).all()
        return departments_list

    # Get staff member from Employees table
    def find_by_staff_id(self, staff_id_num):
        employee = self.db.session.scalars(
            self.db.select(Employees).filter_by(staff_id=staff_id_num).
            limit(1)
        ).first()

        return employee

    # Get all employees in a specific team from Employee table
    def find_by_team(self, reporting_manager_id_num):

        team_manager = self.db.session.scalars(
            self.db.select(Employees).filter_by(staff_id=reporting_manager_id_num).
            limit(1)
        ).first()

        if not team_manager:
            return None, []

        team_list = self.db.session.scalars(
            self.db.select(Employees).filter_by(reporting_manager=reporting_manager_id_num)).all()
        
        return team_manager, team_list

    # Get all employees in a specific department from Employees table
    def find_by_dept(self, dept_name):
        dept_list = self.db.session.scalars(
            self.db.select(Employees).filter_by(dept=dept_name)).all()
        
        return dept_list

    # Get all employees with a specific role from Employees table
    def find_by_role(self, role_num):
        role_list = self.db.session.scalars(
            self.db.select(Employees).filter_by(role=role_num)).all()
        
        return role_list

    # Get specific employee from given email from Employees table
    def find_by_email(self, email):
        employee = self.db.session.scalars(
            self.db.select(Employees).filter_by(email=email).
            limit(1)
            ).first()
        
        return employee