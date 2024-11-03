from src.models.employees import Employees
from src.models.wfh_requests import WFH_Requests
from src.models.withdrawal_requests import Withdrawal_Requests

# Import all email notification functions
from src.utils.email_functions import *

class Withdrawal_Requests_Service:
    def __init__(self, db):
        self.db = db

    # Get all withdrawal_requests of team by list of employees
    def find_by_employees(self, employees_list):
        requests_list = []

        for employee in employees_list:
            withdrawal_requests = self.find_by_staff_id(employee.staff_id)
            requests_list.extend(withdrawal_requests)

        return requests_list

    # Get all withdrawal_requests of staff by staff_id_num from withdrawal_requests table
    def find_by_staff_id(self, staff_id_num):
        staff_requests_list = self.db.session.scalars(
            self.db.select(Withdrawal_Requests).filter_by(staff_id=staff_id_num)
            ).all()
        
        return staff_requests_list
        
