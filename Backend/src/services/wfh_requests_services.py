from src.models.wfh_requests import WFH_Requests
from src.models.employees import Employees

# Import all email notification functions
from src.utils.email_functions import *

class WFH_Requests_Service:
    def __init__(self, db):
        self.db = db

    # WUHAO'S FUNCTIONS

    # Service for Manager to view employees reporting to them
    def get_manager_team(self, manager_id):
        try:
            team = self.db.session.query(Employees).filter_by(Reporting_Manager=manager_id).all()
            team_data = [{
                'Staff_ID': employee.Staff_ID,
                'Staff_FName': employee.Staff_FName,
                'Staff_LName': employee.Staff_LName,
                'Position': employee.Position
            } for employee in team]
            return team_data
        except Exception as e:
            return {"error": str(e)}, 500
        
    # Service to apply for WFH arrangement (For Users)
    def apply_wfh(self, staff_id, reporting_manager, dept, chosen_date, arrangement_type, request_datetime, status, remarks):
        try:
            # Insert the new WFH request
            new_request = WFH_Requests(staff_id, reporting_manager, dept, chosen_date, arrangement_type, request_datetime, status, remarks)
            self.db.session.add(new_request)
            self.db.session.commit()
            
            # Retrieve the generated request_id
            request_id = new_request.request_id

            # Send email notification of the new WFH Request to Reporting Manager
            wfh_request = self.db.session.query(WFH_Requests).filter_by(request_id=request_id).first()
            reporting_manager = self.db.session.query(Employees).filter_by(staff_id=wfh_request.reporting_manager).first()
            employee = self.db.session.query(Employees).filter_by(staff_id=wfh_request.staff_id).first()

            # Send the email notification using mailersend
            newRequestEmailNotif(reporting_manager, employee, wfh_request)

            return {"message": "WFH request submitted successfully!"}, 200

        except Exception as e:
            return {"error": str(e)}, 500
        
    # Helper Service to check if user can apply for WFH
    def can_apply_wfh(self, staff_id, requested_dates):
        # # Retrieve all WFH requests for the staff in the current month
        # current_month = datetime.now().month
        # user_requests = WFHRequest.query.filter_by(staff_id=staff_id).all()

        # # Check for conflicts in requested dates
        # for req in user_requests:
        #     existing_dates = req.requested_dates.split(',')
        #     for date in requested_dates:
        #         if date in existing_dates:
        #             return False
        return True
        
    # Service for Manager to view pending WFH requests
    def view_pending_wfh_requests(self, manager_id):
        # Fetch the manager's team and their pending requests
        team = self.db.session.query(Employees).filter_by(reporting_manager=manager_id).all()
        team_ids = [emp.staff_id for emp in team]
        pending_requests = self.db.session.query(WFH_Requests).filter(WFH_Requests.staff_id.in_(team_ids), WFH_Requests.status == 'Pending').all()

        requests_data = [
            {
                "id": req.request_id,
                "staff_id": req.staff_id,
                "requested_dates": req.chosen_date,
                "time_of_day": req.arrangement_type,
                "reason": req.remarks,
                "status": req.status
            } for req in pending_requests
        ]
        return requests_data, 200

    # Service for Manager to approve WFH requests
    def approve_wfh_request(self, request_id, manager_id):

        # Fetch the WFH request by ID
        wfh_request = self.db.session.query(WFH_Requests).filter_by(request_id=request_id, status='Pending').first()
        if not wfh_request:
            return {"error": "No pending WFH request found"}, 404
        
        # Check the manager's team size
        team_size = self.db.session.query(Employees).filter_by(reporting_manager=manager_id).count()

        # Example business logic: enforce 50% team limit
        wfh_count = self.db.session.query(WFH_Requests).filter_by(status='Approved').count()
        if wfh_count / team_size > 0.5:
            return {"error": "More than 50 percent of the team is already working from home"}, 400

        # Approve the request if within limits
        wfh_request.status = 'Approved'
        self.db.session.commit()

        # Retrieve information needed to populate email content
        reporting_manager = self.db.session.query(Employees).filter_by(staff_id=wfh_request.reporting_manager).first()
        employee = self.db.session.query(Employees).filter_by(staff_id=wfh_request.staff_id).first()

        # Send the email notification using mailersend
        approvalOrRejectionEmailNotif(reporting_manager, employee, wfh_request)

        return {"message": "WFH request approved successfully!"}, 200
        
    # Service for Manager to reject WFH requests
    def reject_wfh_request(self, request_id, rejection_reason):
        try:

            # Retrieve the WFH request by ID
            wfh_request = self.db.session.query(WFH_Requests).filter_by(request_id=request_id, status='Pending').first()
            if not wfh_request:
                return {"error": "No pending WFH request found"}, 404

            # Reject the WFH request
            wfh_request.status = 'Rejected'
            wfh_request.reason = rejection_reason
            self.db.session.commit()

            # Retrieve information needed to populate email content
            reporting_manager = self.db.session.query(Employees).filter_by(staff_id=wfh_request.reporting_manager).first()
            employee = self.db.session.query(Employees).filter_by(staff_id=wfh_request.staff_id).first()

            # Send the email notification using mailersend
            approvalOrRejectionEmailNotif(reporting_manager, employee, wfh_request)

            return {"message": "WFH request rejected successfully!"}, 200

        except Exception as e:
            return {"error": str(e)}, 500


    # JAKOB'S FUNCTIONS

    # Get all wfh_requests from wfh_requests table
    def get_all(self):
        wfh_requests_list = self.db.session.scalars(self.db.select(WFH_Requests)).all()

        return wfh_requests_list

    # Get wfh_requests with specific request_id_num from wfh_requests table
    def find_by_request_id(self, request_id_num):
        wfh_request = self.db.session.scalars(
            self.db.select(WFH_Requests).filter_by(request_id=request_id_num)
            ).first()
        
        return wfh_request

    # Get all wfh_requests of staff by staff_id_num from wfh_requests table
    def find_by_staff_id(self, staff_id_num):
        staff_requests_list = self.db.session.scalars(
            self.db.select(WFH_Requests).filter_by(staff_id=staff_id_num)
            ).all()
        
        return staff_requests_list

    # Get all wfh_requests of team by reporting_manager_id_num from wfh_requests table
    def find_by_team(self, reporting_manager_id_num):

        # Get all requests for the given team (department and reporting manager)
        team_requests_list = self.db.session.scalars(
            self.db.select(WFH_Requests).filter_by(reporting_manager=reporting_manager_id_num)
        ).all()

        return team_requests_list

    # Delete a wfh_request by request_id_num from wfh_requests table
    def delete_wfh_request(self, request_id_num):    
        try:    
            # Find the work-from-home request by request_id
            wfh_request = self.db.session.query(WFH_Requests).get(request_id_num)

            if not wfh_request:
                return 404, None

            # Delete the request from the database
            self.db.session.delete(wfh_request)
            self.db.session.commit()

            # Retrieve information needed to populate email content
            reporting_manager = self.db.session.query(Employees).filter_by(staff_id=wfh_request.reporting_manager).first()
            employee = self.db.session.query(Employees).filter_by(staff_id=wfh_request.staff_id).first()
            
            # Send the email notification using mailersend
            withdrawRequestEmailNotif(reporting_manager, employee, wfh_request)

            return 200, None

        except Exception as e:
            self.db.session.rollback()  # Rollback in case of an error
            return 500, e
