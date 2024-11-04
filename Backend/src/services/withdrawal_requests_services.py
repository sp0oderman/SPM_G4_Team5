from src.models.employees import Employees
from src.models.wfh_requests import WFH_Requests
from src.models.withdrawal_requests import Withdrawal_Requests

# Import all email notification functions
from src.utils.email_functions import *

from sqlalchemy import and_

class Withdrawal_Requests_Service:
    def __init__(self, db):
        self.db = db

    # Get all withdrawal_requests of team by list of employees
    def find_by_employees(self, employees_list, status):
        requests_list = []

        for employee in employees_list:
            withdrawal_requests = self.find_by_staff_id(employee.staff_id, status)
            requests_list.extend(withdrawal_requests)

        return requests_list

    # Get all withdrawal_requests of staff by staff_id_num from withdrawal_requests table
    def find_by_staff_id(self, staff_id_num, status):
        if status != "all":
            staff_requests_list = self.db.session.query(Withdrawal_Requests).filter(
                and_(
                    Withdrawal_Requests.staff_id == staff_id_num,
                    Withdrawal_Requests.status == status
                )
            ).all()
            
        else:
            staff_requests_list = self.db.session.scalars(
                    self.db.select(Withdrawal_Requests).filter_by(staff_id=staff_id_num)
                ).all()
        
        return staff_requests_list
    
    # Approve withdrawal_requests
    def approve_withdrawal_request(self, request_id, reason_for_status):

        # Fetch the withdrawal request by ID
        withdrawal_request = self.db.session.query(Withdrawal_Requests).filter_by(request_id=request_id, status='Pending').first()
        if not withdrawal_request:
            return {"error": "No pending withdrawal request found"}, 404

        # Approve the request if within limits
        withdrawal_request.status = 'Approved'
        withdrawal_request.reason_for_status = reason_for_status
        self.db.session.commit()

        # Retrieve information needed to populate email content
        reporting_manager = self.db.session.query(Employees).filter_by(staff_id=withdrawal_request.reporting_manager).first()
        employee = self.db.session.query(Employees).filter_by(staff_id=withdrawal_request.staff_id).first()

        # Send the email notification
        approvalOrRejectionEmailNotif(reporting_manager, employee, withdrawal_request)

        return {"message": "Withdrawal request approved successfully!"}, 200
    
    # Reject Withdrawal requests
    def reject_withdrawal_request(self, request_id, rejection_reason):
        try:

            # Retrieve the withdrawal request by ID
            withdrawal_request = self.db.session.query(Withdrawal_Requests).filter_by(request_id=request_id, status='Pending').first()
            if not withdrawal_request:
                return {"error": "No pending WFH request found"}, 404

            # Reject the withdrawal request
            withdrawal_request.status = 'Rejected'
            withdrawal_request.reason_for_status = rejection_reason
            self.db.session.commit()

            # Retrieve information needed to populate email content
            reporting_manager = self.db.session.query(Employees).filter_by(staff_id=withdrawal_request.reporting_manager).first()
            employee = self.db.session.query(Employees).filter_by(staff_id=withdrawal_request.staff_id).first()

            # Send the email notification using mailersend
            approvalOrRejectionEmailNotif(reporting_manager, employee, withdrawal_request)

            return {"message": "Withdrawal request rejected successfully!"}, 200

        except Exception as e:
            return {"error": str(e)}, 500
        
    # Get all withdrawal_requests of staff by staff_id_num
    def find_by_staff_id(self, staff_id_num):
        staff_requests_list = self.db.session.scalars(
            self.db.select(Withdrawal_Requests).filter_by(staff_id=staff_id_num)
            ).all()
        
        return staff_requests_list
        
