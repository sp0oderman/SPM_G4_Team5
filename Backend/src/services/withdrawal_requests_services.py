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
        if status != "All":
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

    # Apply withdrawal_request
    def apply_withdrawal(self, staff_id, reporting_manager, wfh_request_id, request_datetime, status, remarks):
        try:
            # Insert the new Withdrawal request
            new_request = Withdrawal_Requests(staff_id, reporting_manager, wfh_request_id, request_datetime, status, remarks, reason_for_status=None)
            self.db.session.add(new_request)
            self.db.session.commit()
            
            # Retrieve the generated request_id
            request_id = new_request.request_id

            # Send email notification of the new WFH Request to Reporting Manager
            withdrawal_request = self.db.session.query(Withdrawal_Requests).filter_by(request_id=request_id).first()
            reporting_manager = self.db.session.query(Employees).filter_by(staff_id=withdrawal_request.reporting_manager).first()
            employee = self.db.session.query(Employees).filter_by(staff_id=withdrawal_request.staff_id).first()

            # Send the email notification using mailersend
            newRequestEmailNotif(reporting_manager, employee, withdrawal_request)

            return {"message": "WFH request submitted successfully!"}, 200

        except Exception as e:
            return {"error": str(e)}, 500

    # Helper function to see if can apply for withdrawal
    def can_apply_withdrawal(self, staff_id, wfh_request_id):
        # Retrieve all WFH requests for the given staff member on the chosen date
        staff_requests_list = self.db.session.query(Withdrawal_Requests).filter(
            Withdrawal_Requests.staff_id == staff_id,
            Withdrawal_Requests.wfh_request_id == wfh_request_id,
            Withdrawal_Requests.status.in_(["Pending", "Approved"])
        ).all()

        # If any results are found, then there are conflcits
        if staff_requests_list != None:
            return False
        # No conflicts found, return True
        return True
    
    # Approve withdrawal_requests
    def approve_withdrawal_request(self, request_id, reason_for_status):

        # Fetch the withdrawal request by ID
        withdrawal_request = self.db.session.query(Withdrawal_Requests).filter_by(request_id=request_id, status='Pending').first()
        if not withdrawal_request:
            return {"error": "No pending withdrawal request found"}, 404
        
        # Fetch the corresponding wfh_request
        wfh_request = self.db.session.query(WFH_Requests).filter_by(wfh_request_id=withdrawal_request.wfh_request_id, status='Pending').first()
        if not wfh_request:
            return {"error": "No approved wfh request found"}, 404

        # Approve the request if within limits
        withdrawal_request.status = 'Approved'
        withdrawal_request.reason_for_status = reason_for_status

        # Adjust the corresponding wfh request
        wfh_request.status = 'Withdrawn'
        wfh_request.reason_for_status = reason_for_status

        self.db.session.commit()

        # Retrieve information needed to populate email content
        reporting_manager = self.db.session.query(Employees).filter_by(staff_id=withdrawal_request.reporting_manager).first()
        employee = self.db.session.query(Employees).filter_by(staff_id=withdrawal_request.staff_id).first()

        # Send the email notification
        approvalOrRejectionEmailNotif(reporting_manager, employee, withdrawal_request)

        return {"message": "Withdrawal request approved and WFH requests withdrawn successfully!"}, 200
    
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
        
