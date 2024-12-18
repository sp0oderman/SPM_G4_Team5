from src.models.employees import Employees
from src.models.wfh_requests import WFH_Requests
from src.models.withdrawal_requests import Withdrawal_Requests  

class Employees_Service:
    def __init__(self, db):
        self.db = db

    # Get list of all reporting_managers - CEO/HR
    def get_all_reporting_managers(self):
        # Retrieve all distinct reporting_manager_ids
        reporting_managers_ids = self.db.session.scalars(
            self.db.select(Employees.reporting_manager).distinct()
        ).all()

        # Retrieve all employee objects using the reporting_manager_ids
        reporting_manager_objects = self.db.session.query(Employees).filter(
            Employees.staff_id.in_(reporting_managers_ids)
        ).all()

        return reporting_manager_objects

    # Get list of reporting_managers that report to input manager - Manager
    def get_reporting_managers_under_me(self, reporting_manager_id_num):
        # Retrieve all distinct reporting_manager_ids
        reporting_managers_ids = self.db.session.scalars(
            self.db.select(Employees.reporting_manager).distinct()
        ).all()

        # Retrieve all employee objects using the reporting_manager_ids that have the reporting_manager == reporting_manager_id_num
        reporting_manager_objects = self.db.session.query(Employees).filter(
            Employees.staff_id.in_(reporting_managers_ids),
            Employees.reporting_manager == reporting_manager_id_num
        ).all()

        return reporting_manager_objects

    # Get all employees in a specific team from Employee table
    def find_by_team(self, reporting_manager_id_num):
        team_manager = self.db.session.scalars(
            self.db.select(Employees).filter_by(staff_id=reporting_manager_id_num)
        ).first()

        if not team_manager:
            return None, []

        team_list = self.db.session.scalars(
            self.db.select(Employees).filter_by(reporting_manager=reporting_manager_id_num)).all()
        
        return team_manager, team_list

    # Get staff member from Employees table
    def find_by_staff_id(self, staff_id_num):
        employee = self.db.session.scalars(
            self.db.select(Employees).filter_by(staff_id=staff_id_num).
            limit(1)
        ).first()

        return employee

    # Get Team Size for given reporting_manager
    def get_team_size(self, reporting_manager_id_num):
        team_size = self.db.session.query(Employees).filter(
            Employees.reporting_manager == reporting_manager_id_num
        ).count()

        return team_size

#####################################################################################################################
#                                                                                                                   #
#                                                UNUSED SERVICES                                                    #
#                                                                                                                   #
#####################################################################################################################

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
    
    # Helper function to recursively get all subordinates of inputted staff_id
    def get_all_subordinates(self, staff_id_num, visited):

        # Check for CEO
        if staff_id_num == 130002:
            return self.db.session.scalars(self.db.select(Employees)).all()

        # Initialize the visited set to track managers we've already processed to avoid infinite loops
        if visited is None:
            visited = set()

        # Stop condition: If this reporting manager has already been processed, return an empty list
        if staff_id_num in visited:
            return []

        # Mark this manager as visited
        visited.add(staff_id_num)

        # Get all requests for the given team (department and reporting manager)
        team_list = self.db.session.scalars(
            self.db.select(Employees).filter_by(reporting_manager=staff_id_num)
        ).all()

        # Accumulator for recursively collected team requests
        full_team_list = team_list[:]

        # Recursively get all the team members under this reporting manager
        for member in team_list:
            full_team_list.extend(self.get_all_subordinates(member.staff_id, visited))

        return full_team_list