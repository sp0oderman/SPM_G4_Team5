import sys
import os

# Add the root directory (where the src directory is located) to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

import unittest
from unittest.mock import MagicMock, patch
from datetime import datetime
from src.services.wfh_requests_services import WFH_Requests_Service
from src.models.wfh_requests import WFH_Requests
from src.models.employees import Employees

from datetime import datetime, timedelta

class TestWFHRequestsService(unittest.TestCase):
    def setUp(self):
        # Initialize mock database and service
        self.db = MagicMock()
        self.service = WFH_Requests_Service(self.db)

    def test_get_team_strength_by_date_range(self):
        # Mock data for date range
        mock_request1 = MagicMock(arrangement_type="Full Day", chosen_date="2023-12-01")
        mock_request2 = MagicMock(arrangement_type="AM", chosen_date="2023-12-02")
        mock_request3 = MagicMock(arrangement_type="PM", chosen_date="2023-12-02")
        self.db.session.query.return_value.filter.return_value.all.return_value = [mock_request1, mock_request2, mock_request3]
        
        # Call the method with date range
        result = self.service.get_team_strength_by_date_range(reporting_manager_id=1, start_date="2023-12-01", end_date="2023-12-02")

        # Assertions
        self.assertEqual(result["2023-12-01"]["AM"], 1)
        self.assertEqual(result["2023-12-01"]["PM"], 1)
        self.assertEqual(result["2023-12-02"]["AM"], 1)
        self.assertEqual(result["2023-12-02"]["PM"], 1)

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
        
        # Mock the request and set a request_id
        mock_request = MagicMock(request_id=1)
        self.db.session.query.return_value.filter_by.return_value.first.side_effect = [mock_employee, mock_reporting_manager, mock_request]

        # Patch the email notification function
        with patch("src.services.wfh_requests_services.newWFHRequestEmailNotif") as mock_email_notif:
            mock_email_notif.return_value = None  # Mock it to do nothing

            # Call the method
            response, status_code = self.service.apply_wfh(
                staff_id=1,
                reporting_manager=2,
                dept="Engineering",
                chosen_date="2024-12-01",
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
        
        # Mock team size and WFH count queries
        self.db.session.query.return_value.filter_by.return_value.count.side_effect = [10, 4]  # Mock team size as 10 and approved count as 4
        
        # Patch the email notification function
        with patch("src.services.wfh_requests_services.approvalOrRejectionWFHRequestEmailNotif") as mock_email_notif:
            mock_email_notif.return_value = None  # Mock it to do nothing

            # Call the method
            response, status_code = self.service.approve_wfh_request(request_id=1, manager_id=2, reason_for_status="Approved")

            # Assertions
            self.assertEqual(status_code, 200)
            self.assertEqual(response["message"], "WFH request approved successfully!")
            self.assertEqual(mock_request.status, "Approved")
            self.assertEqual(mock_request.reason_for_status, "Approved")

    def test_reject_wfh_request(self):
        # Mock data
        mock_request = MagicMock(status="Pending")
        self.db.session.query.return_value.filter_by.return_value.first.return_value = mock_request

        # Call the method
        response, status_code = self.service.reject_wfh_request(request_id=1, rejection_reason="Not needed")

        # Assertions
        self.assertEqual(status_code, 200)
        self.assertEqual(response["message"], "WFH request rejected successfully!")
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
        # Mock db update for recurring approval
        self.db.session.query.return_value.filter.return_value.update.return_value = 3  # Assume 3 requests updated
        response, status_code = self.service.approve_recurring_wfh_requests(recurring_id=1, reason_for_status="Approved")

        # Assertions
        self.assertEqual(status_code, 200)
        self.assertEqual(response["message"], "All recurring requests approved successfully")

    def test_reject_recurring_wfh_requests(self):
        # Mock db update for recurring rejection
        self.db.session.query.return_value.filter.return_value.update.return_value = 3  # Assume 3 requests updated
        response, status_code = self.service.reject_recurring_wfh_requests(recurring_id=1, reason_for_status="Not approved")

        # Assertions
        self.assertEqual(status_code, 200)
        self.assertEqual(response["message"], "All recurring requests rejected successfully")

    @patch('src.services.wfh_requests_services.datetime')
    def test_reject_old_pending_wfh_requests(self, mock_datetime):
        # Set a fixed date for datetime to ensure consistency
        current_date = datetime(2024, 12, 1)
        mock_datetime.now.return_value = current_date

        # Set up a mock WFH request that is older than 2 months and pending
        old_request = MagicMock(status="Pending", request_datetime=current_date - timedelta(days=61))
        self.db.session.query.return_value.filter.return_value.all.return_value = [old_request]

        # Call the method
        self.service.reject_old_pending_wfh_requests()

        # Assertions
        self.assertEqual(old_request.status, "Rejected")
        self.db.session.commit.assert_called_once()

if __name__ == "__main__":
    unittest.main()
