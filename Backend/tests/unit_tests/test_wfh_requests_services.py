import unittest
from unittest.mock import MagicMock, patch
from src.models.wfh_requests import WFH_Requests
from src.models.employees import Employees
from src.services.wfh_requests_services import WFH_Requests_Service


class TestWFHRequestsService(unittest.TestCase):
    def setUp(self):
        # Set up mock database and service instance
        self.mock_db = MagicMock()
        self.wfh_service = WFH_Requests_Service(self.mock_db)
        
        # Mock data for Employees and WFH_Requests
        self.mock_employee = Employees(
            staff_id=1,
            staff_fname="John",
            staff_lname="Doe",
            dept="IT",
            position="staff",
            country="Singapore",
            role=2,
            email="john.doe@example.com",
            reporting_manager=3
        )
        
        self.mock_request = WFH_Requests(
            # request_id=101, 
            staff_id=1, 
            reporting_manager=3, 
            dept="IT",
            chosen_date="2024-10-15",
            arrangement_type="Full Day", 
            request_datetime="2024-10-10", 
            status="Pending", 
            remarks="Family commitment"
        )

    @patch("src.utils.email_functions.newRequestEmailNotif")
    def test_apply_wfh_successful(self, mock_email_notif):
        # Mock the database calls
        self.mock_db.session.add.return_value = None
        self.mock_db.session.commit.return_value = None
        self.mock_db.session.query().filter_by().first.side_effect = [self.mock_request, self.mock_employee, self.mock_employee]

        response, status_code = self.wfh_service.apply_wfh(
            staff_id=1, reporting_manager=3, dept="IT", chosen_date="2024-10-15", 
            arrangement_type="Full Day", request_datetime="2024-10-10", status="Pending", remarks="Family commitment"
        )

        # Check results
        self.assertEqual(status_code, 200)
        self.assertEqual(response["message"], "WFH request submitted successfully!")
        # mock_email_notif.assert_called_once()

    def test_get_manager_team(self):
        # Mock the return value for team data
        self.mock_db.session.query().filter_by().all.return_value = [self.mock_employee]

        result = self.wfh_service.get_manager_team(manager_id=3)

        # Assert that the response contains the expected team data
        expected_result = [{
            'Staff_ID': self.mock_employee.staff_id,
            'Staff_FName': self.mock_employee.staff_fname,
            'Staff_LName': self.mock_employee.staff_lname,
            'Position': self.mock_employee.position
        }]
        self.assertEqual(result, expected_result)

    @patch("src.utils.email_functions.approvalOrRejectionEmailNotif")
    @patch("src.utils.email_functions.mailer")
    def test_approve_wfh_request_successful(self, mock_mailer,mock_email_notif):
        self.mock_request = MagicMock()
        self.mock_request.request_id = 101
        self.mock_request.reporting_manager = 3
        self.mock_request.staff_id = 1
        self.mock_request.status = 'Pending'

        # Mock the database interactions
        self.mock_db.session.query().filter_by(request_id=101, status='Pending').first.return_value = self.mock_request
        
        self.mock_db.session.query().filter_by(reporting_manager=3).count.return_value = 10
        
        self.mock_db.session.query().filter_by(status='Approved').count.return_value = 1

        self.mock_db.session.commit.return_value = None

        # Call the method under test
        response, status_code = self.wfh_service.approve_wfh_request(request_id=101, manager_id=3)

        # Check results
        self.assertEqual(status_code, 200)
        self.assertEqual(response["message"], "WFH request approved successfully!")
        mock_mailer.send.assert_called_once()


    @patch("src.utils.email_functions.approvalOrRejectionEmailNotif")
    @patch("src.utils.email_functions.mailer")
    def test_reject_wfh_request_successful(self, mock_mailer, mock_email_notif):
        self.mock_request = MagicMock()
        self.mock_request.request_id = 101
        self.mock_request.reporting_manager = 3
        self.mock_request.staff_id = 1
        self.mock_request.status = 'Pending'

        # Mock the database interactions
        self.mock_db.session.query().filter_by(request_id=101, status='Pending').first.return_value = self.mock_request
        
        self.mock_db.session.query().filter_by(reporting_manager=3).count.return_value = 10
        
        self.mock_db.session.query().filter_by(status='Rejected').count.return_value = 1
        self.mock_db.session.commit.return_value = None

        response, status_code = self.wfh_service.reject_wfh_request(request_id=101, rejection_reason="Workload")

        # Check results
        self.assertEqual(status_code, 200)
        self.assertEqual(response["message"], "WFH request rejected successfully!")
        mock_mailer.send.assert_called_once()

    def test_get_all_requests(self):
        # Mock the return value for all WFH requests
        self.mock_db.session.scalars.return_value.all.return_value = [self.mock_request]

        result = self.wfh_service.get_all(status="All")

        # Assert the returned list matches the expected mock data
        self.assertEqual(result, [self.mock_request])

    def test_find_by_request_id(self):
        # Mock the return value for a single WFH request by request ID
        self.mock_db.session.scalars.return_value.first.return_value = self.mock_request

        result = self.wfh_service.find_by_request_id(request_id_num=101)

        # Check the returned request matches the mock data
        self.assertEqual(result, self.mock_request)

    @patch("src.utils.email_functions.withdrawRequestEmailNotif")
    @patch("src.utils.email_functions.mailer")
    def test_delete_wfh_request_successful(self, mock_mailer, mock_email_notif):
        self.mock_request = MagicMock()
        self.mock_request.request_id = 101
        self.mock_request.reporting_manager = 3
        self.mock_request.staff_id = 1
        self.mock_request.status = 'Pending'

        # Mock the database interactions
        self.mock_db.session.query().filter_by(request_id=101, status='Pending').first.return_value = self.mock_request
        
        self.mock_db.session.query().filter_by(reporting_manager=3).count.return_value = 10
        
        self.mock_db.session.query().filter_by(status='Approved').count.return_value = 1

        self.mock_db.session.commit.return_value = None

        status_code, error = self.wfh_service.delete_wfh_request(request_id_num=101)

        # Check the result and ensure no errors are returned
        self.assertEqual(status_code, 200)
        self.assertIsNone(error)
        mock_mailer.send.assert_called_once()

    def test_view_pending_wfh_requests(self):
        # Mock return values for manager's team and their pending requests
        self.mock_db.session.query().filter_by().all.side_effect = [[self.mock_employee], [self.mock_request]]

        result, status_code = self.wfh_service.view_pending_wfh_requests(manager_id=3)
        
        # Check the response structure and data
        expected_result = []
        self.assertEqual(result, expected_result)
        self.assertEqual(status_code, 200)


if __name__ == "__main__":
    unittest.main()
