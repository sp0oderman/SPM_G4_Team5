import sys 
import os 
 
# Add the root directory (where the src directory is located) to the system path 
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

import unittest
from unittest.mock import MagicMock, patch
from datetime import datetime
from src.services.wfh_requests_services import WFH_Requests_Service  # Adjust import path as needed
from src.models.wfh_requests import WFH_Requests
from src.models.employees import Employees

class TestWFHRequestsService(unittest.TestCase):
    def setUp(self):
        # Initialize mock database and service
        self.db = MagicMock()
        self.service = WFH_Requests_Service(self.db)

    def test_get_team_strength_by_date(self):
        # Mock data and query result
        mock_request1 = MagicMock(arrangement_type="Full Day")
        mock_request2 = MagicMock(arrangement_type="AM")
        mock_request3 = MagicMock(arrangement_type="PM")
        self.db.session.query.return_value.filter.return_value.all.return_value = [mock_request1, mock_request2, mock_request3]
        
        # Call the method
        result = self.service.get_team_strength_by_date(reporting_manager_id=1, date="2023-12-01")

        # Assertions
        self.assertEqual(result["AM"], 2)
        self.assertEqual(result["PM"], 2)

    def test_find_by_employees(self):
        # Mock data
        mock_employee = MagicMock(staff_id=1)
        mock_request = MagicMock()
        mock_request.json.return_value = {"request_id": 1, "status": "Approved"}
        
        # Mock method responses
        self.service.find_by_staff_id = MagicMock(return_value=[mock_request])

        # Call the method
        result = self.service.find_by_employees([mock_employee], status="Approved")

        # Assertions
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], mock_request)

    def test_apply_wfh_success(self):
        # Mock data
        mock_employee = MagicMock(staff_id=1)
        mock_reporting_manager = MagicMock(staff_id=2)
        
        # Mock database actions
        self.db.session.add = MagicMock()
        self.db.session.commit = MagicMock()
        self.db.session.query.return_value.filter_by.return_value.first.side_effect = [mock_employee, mock_reporting_manager]

        # Call the method
        response, status_code = self.service.apply_wfh(
            staff_id=1,
            reporting_manager=2,
            dept="Engineering",
            chosen_date="2023-12-01",
            arrangement_type="Full Day",
            request_datetime=datetime.now(),
            status="Pending",
            remarks="WFH request",
            recurring_id=-1
        )

        # Assertions
        self.assertEqual(status_code, 200)
        self.assertEqual(response["message"], "WFH request submitted successfully!")

    def test_apply_wfh_failure(self):
        # Mock exception
        self.db.session.add.side_effect = Exception("Database error")

        # Call the method
        response, status_code = self.service.apply_wfh(
            staff_id=1,
            reporting_manager=2,
            dept="Engineering",
            chosen_date="2023-12-01",
            arrangement_type="Full Day",
            request_datetime=datetime.now(),
            status="Pending",
            remarks="WFH request",
            recurring_id=-1
        )

        # Assertions
        self.assertEqual(status_code, 500)
        self.assertIn("Database error", response["error"])

    def test_can_apply_wfh_no_conflict(self):
        # Mock no conflicting requests
        self.db.session.query.return_value.filter.return_value.all.return_value = []

        # Call the method
        result = self.service.can_apply_wfh(staff_id=1, chosen_date="2023-12-01", arrangement_type="Full Day")

        # Assertions
        self.assertTrue(result)

    def test_can_apply_wfh_conflict(self):
        # Mock conflicting request
        mock_request = MagicMock(arrangement_type="AM")
        self.db.session.query.return_value.filter.return_value.all.return_value = [mock_request]

        # Call the method
        result = self.service.can_apply_wfh(staff_id=1, chosen_date="2023-12-01", arrangement_type="AM")

        # Assertions
        self.assertFalse(result)

    def test_approve_wfh_request(self):
        # Mock data
        mock_request = MagicMock(status="Pending")
        self.db.session.query.return_value.filter_by.return_value.first.return_value = mock_request

        # Call the method
        response, status_code = self.service.approve_wfh_request(request_id=1, manager_id=2, reason_for_status="Approved")

        # Assertions
        self.assertEqual(status_code, 200)
        self.assertEqual(response["message"], "WFH request approved successfully!")
        self.assertEqual(mock_request.status, "Approved")

    def test_reject_wfh_request(self):
        # Mock data
        mock_request = MagicMock(status="Pending")
        self.db.session.query.return_value.filter_by.return_value.first.return_value = mock_request

        # Call the method
        response, status_code = self.service.reject_wfh_request(request_id=1, rejection_reason="Not needed")

        # Assertions
        self.assertEqual(status_code, 200)
        self.assertEqual(response["message"], "WFH request withdrawn successfully!")
        self.assertEqual(mock_request.status, "Rejected")

    def test_withdraw_wfh_request(self):
        # Mock data
        mock_request = MagicMock(status="Pending")
        self.db.session.query.return_value.filter.return_value.first.return_value = mock_request

        # Call the method
        response, status_code = self.service.withdraw_wfh_request(request_id=1, withdrawal_reason="Changed plans")

        # Assertions
        self.assertEqual(status_code, 200)
        self.assertEqual(response["message"], "WFH request withdrawn successfully!")
        self.assertEqual(mock_request.status, "Withdrawn")

    def test_approve_recurring_wfh_requests(self):
        # Call the method and mock db update
        self.db.session.query.return_value.filter.return_value.update.return_value = 3  # Assume 3 requests updated
        response, status_code = self.service.approve_recurring_wfh_requests(recurring_id=1, reason_for_status="Approved")

        # Assertions
        self.assertEqual(status_code, 200)
        self.assertEqual(response["message"], "All recurring requests approved successfully")

    def test_reject_recurring_wfh_requests(self):
        # Call the method and mock db update
        self.db.session.query.return_value.filter.return_value.update.return_value = 3  # Assume 3 requests updated
        response, status_code = self.service.reject_recurring_wfh_requests(recurring_id=1, reason_for_status="Not approved")

        # Assertions
        self.assertEqual(status_code, 200)
        self.assertEqual(response["message"], "All recurring requests rejected successfully")

if __name__ == "__main__":
    unittest.main()
