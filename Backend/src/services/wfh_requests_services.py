from src.models.employees import Employees
from src.models.wfh_requests import WFH_Requests
from src.models.withdrawal_requests import Withdrawal_Requests

# Import all email notification functions
from src.utils.email_functions import *

from sqlalchemy import and_
from datetime import datetime

class WFH_Requests_Service:
    def __init__(self, db):
        self.db = db
    
    # Get team strength by given date
    def get_team_strength_by_date(self, reporting_manager_id, date):
        approved_requests_list = self.db.session.query(WFH_Requests).filter(
                                    and_(
                                        WFH_Requests.reporting_manager == reporting_manager_id,
                                        WFH_Requests.status == "Approved",
                                        WFH_Requests.chosen_date == date
                                    )
                                ).all()
                                
        # Initialise dictionary to store strength count
        strength_dict = {"AM":0, "PM":0}

        for req in approved_requests_list:
            if  req.arrangement_type == "Full Day":
                strength_dict["AM"] += 1
                strength_dict["PM"] += 1
            elif req.arrangement_type == "AM":
                strength_dict["AM"] += 1
            elif req.arrangement_type == "PM":
                strength_dict["PM"] += 1

        return strength_dict

    # Get all wfh_requests of team by list of employees
    def find_by_employees(self, employees_list, status):
        requests_list = []

        for employee in employees_list:
            wfh_requests = self.find_by_staff_id(employee.staff_id, status)
            requests_list.extend(wfh_requests)

        return requests_list

    # Get all wfh_requests of staff by staff_id_num from wfh_requests table
    def find_by_staff_id(self, staff_id_num, status):
        if status != "All":
            staff_requests_list = self.db.session.query(WFH_Requests).filter(
                and_(
                    WFH_Requests.staff_id == staff_id_num,
                    WFH_Requests.status == status
                )
            ).all()
            
        else:
            staff_requests_list = self.db.session.scalars(
                    self.db.select(WFH_Requests).filter_by(staff_id=staff_id_num)
                ).all()
        
        return staff_requests_list

    # Service to apply for WFH arrangement (For Users)
    def apply_wfh(self, staff_id, reporting_manager, dept, chosen_date, arrangement_type, request_datetime, status, remarks, recurring_id):
        try:
            # Insert the new WFH request
            new_request = WFH_Requests(staff_id, reporting_manager, dept, chosen_date, arrangement_type, request_datetime, status, remarks, recurring_id, reason_for_status=None)
            self.db.session.add(new_request)
            self.db.session.commit()
            
            # Retrieve the generated request_id
            request_id = new_request.request_id

            # Send email notification of the new WFH Request to Reporting Manager
            wfh_request = self.db.session.query(WFH_Requests).filter_by(request_id=request_id).first()
            reporting_manager = self.db.session.query(Employees).filter_by(staff_id=wfh_request.reporting_manager).first()
            employee = self.db.session.query(Employees).filter_by(staff_id=wfh_request.staff_id).first()

            # Send the email notification using mailersend
            newWFHRequestEmailNotif(reporting_manager, employee, wfh_request)

            return {"message": "WFH request submitted successfully!"}, 200

        except Exception as e:
            return {"error": str(e)}, 500
        
    def can_apply_wfh(self, staff_id, chosen_date, arrangement_type):
        # Convert chosen_date to date object for consistent comparison
        chosen_date = datetime.strptime(chosen_date, "%Y-%m-%d").date() if isinstance(chosen_date, str) else chosen_date

        # Retrieve all WFH requests for the given staff member on the chosen date
        staff_requests_list = self.db.session.query(WFH_Requests).filter(
            WFH_Requests.staff_id == staff_id,
            WFH_Requests.chosen_date == chosen_date.strftime("%Y-%m-%d")
        ).all()

        for request in staff_requests_list:
            # Check if arrangement type conflicts with any existing request
            if arrangement_type == "Full Day" or request.arrangement_type == "Full Day" or request.arrangement_type == arrangement_type:
                # Conflict found, return False
                return False

        # No conflicts found, return True
        return True

    def get_max_recurring_id(self):
        max_id = self.db.session.query(self.db.func.max(WFH_Requests.recurring_id)).scalar()
        return max_id

    # Service for Manager to approve WFH requests
    def approve_wfh_request(self, request_id, manager_id, reason_for_status):
        try:
            # Fetch the WFH request by ID
            wfh_request = self.db.session.query(WFH_Requests).filter_by(request_id=request_id, status='Pending').first()
            if not wfh_request:
                return {"error": "No such pending WFH request found"}, 404
            
            # Check the manager's team size
            team_size = self.db.session.query(Employees).filter_by(reporting_manager=manager_id).count()

            # Example business logic: enforce 50% team limit
            wfh_count = self.db.session.query(WFH_Requests).filter_by(status='Approved').count()
            if wfh_count / team_size > 0.5:
                return {"error": "More than 50 percent of the team is already working from home"}, 400

            # Approve the request if within limits
            wfh_request.status = 'Approved'
            wfh_request.reason_for_status = reason_for_status
            self.db.session.commit()

            # Retrieve information needed to populate email content
            reporting_manager = self.db.session.query(Employees).filter_by(staff_id=wfh_request.reporting_manager).first()
            employee = self.db.session.query(Employees).filter_by(staff_id=wfh_request.staff_id).first()

            # Send the email notification using mailersend
            approvalOrRejectionWFHRequestEmailNotif(reporting_manager, employee, wfh_request)

            return {"message": "WFH request approved successfully!"}, 200
        except Exception as e:
            return {"error": str(e)}, 500
        
    # Service for Manager to reject WFH requests
    def reject_wfh_request(self, request_id, rejection_reason):
        try:

            # Retrieve the WFH request by ID
            wfh_request = self.db.session.query(WFH_Requests).filter_by(request_id=request_id, status='Pending').first()
            if not wfh_request:
                return {"error": "No such pending WFH request found"}, 404

            # Reject the WFH request
            wfh_request.status = 'Rejected'
            wfh_request.reason_for_status = rejection_reason
            self.db.session.commit()

            # Retrieve information needed to populate email content
            reporting_manager = self.db.session.query(Employees).filter_by(staff_id=wfh_request.reporting_manager).first()
            employee = self.db.session.query(Employees).filter_by(staff_id=wfh_request.staff_id).first()

            # Send the email notification using mailersend
            approvalOrRejectionWFHRequestEmailNotif(reporting_manager, employee, wfh_request)

            return {"message": "WFH request withdrawn successfully!"}, 200

        except Exception as e:
            return {"error": str(e)}, 500
        
    # Service for Manager to withdraw approved WFH requests or staff to withdraw pending request
    def withdraw_wfh_request(self, request_id, withdrawal_reason):
        try:

            # Retrieve the WFH request by ID
            wfh_request = self.db.session.query(WFH_Requests).filter(
                WFH_Requests.request_id == request_id,
                WFH_Requests.status.in_(['Approved', 'Pending'])
            ).first()

            # Check if manager or staff
            flag = False
            if wfh_request.status == "Approved":
                flag = True

            if not wfh_request:
                return {"error": "No such approved/pending WFH request found"}, 404

            # Withdraw the WFH request
            wfh_request.status = 'Withdrawn'
            wfh_request.reason_for_status = withdrawal_reason
            self.db.session.commit()

            # Retrieve information needed to populate email content
            reporting_manager = self.db.session.query(Employees).filter_by(staff_id=wfh_request.reporting_manager).first()
            employee = self.db.session.query(Employees).filter_by(staff_id=wfh_request.staff_id).first()

            # Send the email notification if manager withdraw approved req
            if flag:
                withdrawWFHRequestEmailNotif(reporting_manager, employee, wfh_request)

            return {"message": "WFH request withdrawn successfully!"}, 200

        except Exception as e:
            return {"error": str(e)}, 500

    # Approve recurring requests
    def approve_recurring_wfh_requests(self, recurring_id, reason_for_status):
        try:
            # Update all requests with the same recurring_id to "Approved"
            self.db.session.query(WFH_Requests).filter(WFH_Requests.recurring_id == recurring_id).update({"status": "Approved", "reason_for_status": reason_for_status})
            self.db.session.commit()

            # Get all requests that were updated
            requests_list = self.db.session.query(WFH_Requests).filter(WFH_Requests.recurring_id == recurring_id).all()

            # Retrieve information needed to populate email content
            reporting_manager = self.db.session.query(Employees).filter_by(staff_id=requests_list[0].reporting_manager).first()
            employee = self.db.session.query(Employees).filter_by(staff_id=requests_list[0].staff_id).first()
            for req in requests_list:
                # Send the email notification
                approvalOrRejectionWFHRequestEmailNotif(reporting_manager, employee, req)

            return {"message": "All recurring requests approved successfully"}, 200
        except Exception as e:
            self.db.session.rollback()
            return {"error": str(e)}, 500

    # Reject recurring requests
    def reject_recurring_wfh_requests(self, recurring_id, reason_for_status):
        try:
            # Update all requests with the same recurring_id to "Rejected"
            self.db.session.query(WFH_Requests).filter(WFH_Requests.recurring_id == recurring_id).update({"status": "Rejected", "reason_for_status": reason_for_status})
            self.db.session.commit()

            # Get all requests that were updated
            requests_list = self.db.session.query(WFH_Requests).filter(WFH_Requests.recurring_id == recurring_id).all()

            # Retrieve information needed to populate email content
            reporting_manager = self.db.session.query(Employees).filter_by(staff_id=requests_list[0].reporting_manager).first()
            employee = self.db.session.query(Employees).filter_by(staff_id=requests_list[0].staff_id).first()
            for req in requests_list:
                # Send the email notification using mailersend
                approvalOrRejectionWFHRequestEmailNotif(reporting_manager, employee, req)

            return {"message": "All recurring requests rejected successfully"}, 200
        except Exception as e:
            self.db.session.rollback()
            return {"error": str(e)}, 500

#####################################################################################################################
#                                                                                                                   #
#                                                UNUSED SERVICES                                                    #
#                                                                                                                   #
#####################################################################################################################

    # Get wfh_requests by status
    def get_by_status(self, status):
        if status == "All":
            wfh_requests_list = self.db.session.scalars(self.db.select(WFH_Requests)).all()
            return wfh_requests_list

        wfh_requests_list = self.db.session.scalars(self.db.select(WFH_Requests).filter_by(status=status)).all()
        return wfh_requests_list

    # Get wfh_requests with specific request_id_num from wfh_requests table
    def find_by_request_id(self, request_id_num):
        wfh_request = self.db.session.scalars(
            self.db.select(WFH_Requests).filter_by(request_id=request_id_num)
            ).first()
        
        return wfh_request


    # # DEPRECATED - Delete a wfh_request by request_id_num from wfh_requests table
    # def delete_wfh_request(self, request_id_num):    
    #     try:    
    #         # Find the work-from-home request by request_id
    #         wfh_request = self.db.session.query(WFH_Requests).get(request_id_num)

    #         if not wfh_request:
    #             return 404, None

    #         # Delete the request from the database
    #         self.db.session.delete(wfh_request)
    #         self.db.session.commit()

    #         # Retrieve information needed to populate email content
    #         reporting_manager = self.db.session.query(Employees).filter_by(staff_id=wfh_request.reporting_manager).first()
    #         employee = self.db.session.query(Employees).filter_by(staff_id=wfh_request.staff_id).first()
            
    #         # Send the email notification using mailersend
    #         withdrawRequestEmailNotif(reporting_manager, employee, wfh_request)

    #         return 200, None

    #     except Exception as e:
    #         self.db.session.rollback()  # Rollback in case of an error
    #         return 500, e
        
    # # DEPRECATED - Service for Manager to view employees reporting to them
    # def get_manager_team(self, manager_id):
    #     try:
    #         team = self.db.session.query(Employees).filter_by(Reporting_Manager=manager_id).all()
    #         team_data = [{
    #             'Staff_ID': employee.Staff_ID,
    #             'Staff_FName': employee.Staff_FName,
    #             'Staff_LName': employee.Staff_LName,
    #             'Position': employee.Position
    #         } for employee in team]
    #         return team_data
    #     except Exception as e:
    #         return {"error": str(e)}, 500

    # # DEPRECATED - Service to apply for WFH arrangement (For Users)
    # def apply_wfh(self, staff_id, reporting_manager, dept, chosen_date, arrangement_type, request_datetime, status, remarks):
    #     try:
    #         # Insert the new WFH request
    #         new_request = WFH_Requests(staff_id, reporting_manager, dept, chosen_date, arrangement_type, request_datetime, status, remarks)
    #         self.db.session.add(new_request)
    #         self.db.session.commit()
            
    #         # Retrieve the generated request_id
    #         request_id = new_request.request_id

    #         # Send email notification of the new WFH Request to Reporting Manager
    #         wfh_request = self.db.session.query(WFH_Requests).filter_by(request_id=request_id).first()
    #         reporting_manager = self.db.session.query(Employees).filter_by(staff_id=wfh_request.reporting_manager).first()
    #         employee = self.db.session.query(Employees).filter_by(staff_id=wfh_request.staff_id).first()

    #         # Send the email notification using mailersend
    #         newRequestEmailNotif(reporting_manager, employee, wfh_request)

    #         return {"message": "WFH request submitted successfully!"}, 200

    #     except Exception as e:
    #         return {"error": str(e)}, 500

    # # DEPRECATED - Service for Manager to view pending WFH requests
    # def view_pending_wfh_requests(self, manager_id):
    #     # Fetch the manager's team and their pending requests
    #     team = self.db.session.query(Employees).filter_by(reporting_manager=manager_id).all()
    #     team_ids = [emp.staff_id for emp in team]
    #     pending_requests = self.db.session.query(WFH_Requests).filter(WFH_Requests.staff_id.in_(team_ids), WFH_Requests.status == 'Pending').all()

    #     requests_data = [
    #         {
    #             "id": req.request_id,
    #             "staff_id": req.staff_id,
    #             "requested_dates": req.chosen_date,
    #             "time_of_day": req.arrangement_type,
    #             "reason": req.remarks,
    #             "status": req.status
    #         } for req in pending_requests
    #     ]
    #     return requests_data, 200
