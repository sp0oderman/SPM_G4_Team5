import sys 
import os 
 
# Add the root directory (where the src directory is located) to the system path 
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

import unittest
from unittest.mock import MagicMock, patch
from datetime import datetime
from src.services.withdrawal_requests_services import Withdrawal_Requests_Service
from src.models.withdrawal_requests import Withdrawal_Requests
from src.models.wfh_requests import WFH_Requests
from src.models.employees import Employees

class TestWithdrawalRequestsService(unittest.TestCase):
    def setUp(self):
        # Set up a mock database session and initialize the service
        self.db = MagicMock()
        self.service = Withdrawal_Requests_Service(self.db)

    def test_find_by_employees(self):
        # Mock the response for find_by_staff_id
        mock_request1 = Withdrawal_Requests(
            staff_id=1, reporting_manager=2, wfh_request_id=10, request_datetime="2024-01-01",
            status="Pending", remarks="Pending request", reason_for_status=None
        )
        mock_request2 = Withdrawal_Requests(
            staff_id=2, reporting_manager=2, wfh_request_id=11, request_datetime="2024-01-02",
            status="Pending", remarks="Pending request", reason_for_status=None
        )
        self.service.find_by_staff_id = MagicMock(side_effect=[[mock_request1], [mock_request2]])

        # Call the method
        employees_list = [Employees(
            staff_id=1, staff_fname="Team", staff_lname="Member1",
            dept="Sales", position="Sales Rep", country="Singapore",
            email="member.one@example.com", reporting_manager=1, role=2
        ), Employees(
            staff_id=2, staff_fname="Team", staff_lname="Member2",
            dept="Sales", position="Sales Rep", country="Singapore",
            email="member.two@example.com", reporting_manager=1, role=2
        )]
        status = "Pending"
        result = self.service.find_by_employees(employees_list, status)

        # Assertions
        self.assertEqual(len(result), 2)
        self.service.find_by_staff_id.assert_any_call(1, status)
        self.service.find_by_staff_id.assert_any_call(2, status)

    def test_find_by_staff_id(self):
        # Mock database response
        mock_request = Withdrawal_Requests(
            staff_id=1, reporting_manager=2, wfh_request_id=10, request_datetime="2024-01-01",
            status="Pending", remarks="Pending request", reason_for_status=None
        )
        self.db.session.query.return_value.filter.return_value.all.return_value = [mock_request]

        result = self.service.find_by_staff_id(1, "Pending")

        # Assertions
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].staff_id, 1)
        self.assertEqual(result[0].status, "Pending")

    @patch("src.utils.email_functions.newWithdrawalRequestEmailNotif")
    def test_apply_withdrawal(self, mock_email_notif):
        # Mock new request and email notification
        self.db.session.add = MagicMock()
        self.db.session.commit = MagicMock()

        # Create mock request with a request_id
        mock_request = Withdrawal_Requests(
            staff_id=1, reporting_manager=2, wfh_request_id=10, request_datetime="2024-01-01",
            status="Pending", remarks="Request to withdraw WFH", reason_for_status=None
        )
        mock_request.request_id = 123  # Set a mock request_id

        self.db.session.query.return_value.filter_by.return_value.first.return_value = mock_request

        # Mock employee data if needed
        mock_reporting_manager = MagicMock()
        mock_employee = MagicMock()
        self.db.session.query.side_effect = [
            MagicMock(return_value=mock_request),
            MagicMock(return_value=mock_reporting_manager),
            MagicMock(return_value=mock_employee)
        ]

        # Call the method
        response, status_code = self.service.apply_withdrawal(
            staff_id=1,
            reporting_manager=2,
            wfh_request_id=10,
            request_datetime="2024-01-01",
            status="Approved",
            remarks="Request to withdraw WFH"
        )

        # Assertions
        self.assertEqual(status_code, 200)
        self.assertEqual(response["message"], "Withdrawal request submitted successfully!")
        #mock_email_notif.assert_called_once()


    def test_can_apply_withdrawal_no_conflict(self):
        # Mock no conflicting requests
        self.db.session.query.return_value.filter.return_value.all.return_value = []

        # Call the method
        result = self.service.can_apply_withdrawal(staff_id=1, wfh_request_id=10)

        # Assertions
        self.assertTrue(result)

    def test_can_apply_withdrawal_with_conflict(self):
        # Mock conflicting request
        mock_request = Withdrawal_Requests(
            staff_id=1, reporting_manager=2, wfh_request_id=10, request_datetime="2024-01-01",
            status="Pending", remarks="Pending request", reason_for_status=None
        )
        self.db.session.query.return_value.filter.return_value.all.return_value = [mock_request]

        # Call the method
        result = self.service.can_apply_withdrawal(staff_id=1, wfh_request_id=10)

        # Assertions
        self.assertFalse(result)

    @patch("src.utils.email_functions.approvalOrRejectionWithdrawalRequestEmailNotif")
    def test_approve_withdrawal_request(self, mock_email_notif):
        # Mock withdrawal request, WFH request, and associated employee data
        mock_withdrawal_request = Withdrawal_Requests(
            staff_id=1, reporting_manager=2, wfh_request_id=1, request_datetime="2024-01-01",
            status="Pending", remarks="Request to withdraw WFH", reason_for_status=None
        )
        mock_wfh_request = WFH_Requests(
            staff_id=1, 
            reporting_manager=2,
            dept='Sales',
            chosen_date='2024-10-10', 
            arrangement_type='Full Day', 
            request_datetime='2024-08-08',
            status='Approved',  # This should be "Approved" to match the service query
            remarks='Doctor appointment',
            recurring_id=-1,
            reason_for_status=None
        )
        mock_reporting_manager = Employees(
            staff_id=2, staff_fname="Manager", staff_lname="One",
            dept="Sales", position="Manager", country="Singapore",
            email="manager.one@example.com", reporting_manager=None, role=3
        )
        mock_employee = Employees(
            staff_id=1, staff_fname="Team", staff_lname="Member1",
            dept="Sales", position="Sales Rep", country="Singapore",
            email="member.one@example.com", reporting_manager=2, role=2
        )

        # Set up the side effects for filter_by().first() in sequence
        self.db.session.query.return_value.filter_by.return_value.first.side_effect = [
            mock_withdrawal_request,  # For fetching the withdrawal request
            mock_wfh_request,         # For fetching the WFH request
            mock_reporting_manager,    # For fetching the reporting manager
            mock_employee              # For fetching the employee
        ]

        # Call the method
        response, status_code = self.service.approve_withdrawal_request(withdrawal_request_id=1, reason_for_status="Approved for work")

        # Assertions
        self.assertEqual(status_code, 200)
        self.assertEqual(response["message"], "Withdrawal request approved and WFH requests withdrawn successfully!")
        self.assertEqual(mock_withdrawal_request.status, "Approved")
        self.assertEqual(mock_withdrawal_request.reason_for_status, "Approved for work")
        self.assertEqual(mock_wfh_request.status, "Withdrawn")
    
        # Check if the notification function was called
        # mock_email_notif.assert_called_once_with(mock_reporting_manager, mock_employee, mock_withdrawal_request)

    @patch("src.utils.email_functions.approvalOrRejectionWithdrawalRequestEmailNotif")
    def test_reject_withdrawal_request(self, mock_email_notif):
        # Mock the withdrawal request and associated employee data
        mock_withdrawal_request = Withdrawal_Requests(
            staff_id=1, reporting_manager=2, wfh_request_id=10, request_datetime="2024-01-01",
            status="Pending", remarks="Request to withdraw WFH", reason_for_status=None
        )
        mock_employee = Employees(
            staff_id=2, staff_fname="Team", staff_lname="Member1",
            dept="Sales", position="Sales Rep", country="Singapore",
            email="member.one@example.com", reporting_manager=3, role=2
        )
        mock_reporting_manager = Employees(
            staff_id=3, staff_fname="Team", staff_lname="Member2",
            dept="Sales", position="Sales Rep", country="Singapore",
            email="member.two@example.com", reporting_manager=1, role=3
        )

        # Set up query return values for withdrawal request and employee
        self.db.session.query.return_value.filter_by.return_value.first.side_effect = [
            mock_withdrawal_request,  # First call returns the withdrawal request
            mock_reporting_manager,   # Second call returns reporting manager
            mock_employee             # Third call returns employee
        ]

        # Mock the commit method
        self.db.session.commit = MagicMock()

        # Call the method
        response, status_code = self.service.reject_withdrawal_request(
            withdrawal_request_id=1, rejection_reason="Not eligible"
        )

        # Assertions
        self.assertEqual(status_code, 200)
        self.assertEqual(response["message"], "Withdrawal request rejected successfully!")
        self.assertEqual(mock_withdrawal_request.status, "Rejected")
        self.assertEqual(mock_withdrawal_request.reason_for_status, "Not eligible")
        # mock_email_notif.assert_called_once()
        
if __name__ == "__main__":
    unittest.main()
