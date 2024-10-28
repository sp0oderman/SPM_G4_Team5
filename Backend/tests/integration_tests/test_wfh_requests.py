import sys
import os

# Add the root directory (where the `src` directory is located) to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

import unittest
from flask_testing import TestCase

from src.models.wfh_requests import WFH_Requests
from src.models.employees import Employees
from __init__ import db, create_app
from config import TestingConfig

class BaseTestCase(TestCase):
    """Base test case to set up the Flask test client and the database."""
    
    def create_app(self):
        """Configure the app for testing with an in-memory SQLite database."""
        app = create_app(config_class=TestingConfig)
        return app

    def setUp(self):
        """Set up the database and create the tables before each test."""
        with self.app.app_context():
            db.create_all()  # Ensure tables are created before adding data

        # Add a reporting manager
        reportingManager = Employees(
            staff_id = 140894,
            staff_fname = "managerfname",
            staff_lname = "managerlname",
            dept = "Sales",
            position = "Sales Manager",
            country = "Singapore",
            email = "jakob.lie.2022@smu.edu.sg",
            reporting_manager = 140001,
            role = 3
        )

        # Add employee who reports to RM
        employee = Employees(
            staff_id = 140002,
            staff_fname = "empfname",
            staff_lname = "emplname",
            dept = "Sales",
            position = "Account Manager",
            country = "Singapore",
            email = "sthauheed.2022@smu.edu.sg",
            reporting_manager = 140894,
            role = 2
        )

        # Add a pending request 
        pendingRequest = WFH_Requests(
            staff_id = 140002,
            reporting_manager = 140894,
            dept = "",
            chosen_date = "2024-04-10",
            arrangement_type = "am",
            request_datetime = "2024-01-01",
            status = "pending",
            remarks = "I am a pending request"
        )
        
        # Add an approved request
        approvedRequest = WFH_Requests(
            staff_id = 140002,
            reporting_manager = 140894,
            dept = "",
            chosen_date = "2024-04-10",
            arrangement_type = "pm",
            request_datetime = "2024-01-01",
            status = "approved",
            remarks = "I am a pending request"
        )

        db.session.add(reportingManager)
        db.session.add(employee)
        db.session.add(pendingRequest)
        db.session.add(approvedRequest)
        db.session.commit()

    def tearDown(self):
        """Destroy the database after each test."""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()


# Test cases
class TestWFHRequests(BaseTestCase):

    def test_get_all_requests(self):
        """Test retrieving all WFH requests."""
        response = self.client.get('/wfh_requests/All')
        self.assertEqual(response.status_code, 200)

    def test_get_all_requests_empty(self):
        """Test retrieving all WFH requests when none exist."""
        # Remove all records from the table instead of dropping the entire table
        with self.app.app_context():
            db.session.query(WFH_Requests).delete()
            db.session.commit()
        response = self.client.get('/wfh_requests/All')
        self.assertEqual(response.status_code, 404)
        self.assertIn(b"There are no work-from-home requests.", response.data)

    def test_find_by_request_id_success(self):
        """Test finding a WFH request by ID successfully."""
        response = self.client.get('/wfh_requests/request_id/1')
        self.assertEqual(response.status_code, 200)
        # self.assertIn(b"Pending approval", response.data)

    def test_find_by_request_id_not_found(self):
        """Test finding a WFH request by a non-existent ID."""
        response = self.client.get('/wfh_requests/request_id/999')
        self.assertEqual(response.status_code, 404)
        # self.assertIn(b"Work-from-home request with that ID number is not found.", response.data)

    def test_find_by_staff_id_success(self):
        """Test finding WFH requests by staff ID successfully."""
        response = self.client.get('/wfh_requests/staff_id/140002')
        self.assertEqual(response.status_code, 200)
        # self.assertIn(b"Pending approval", response.data)

    def test_find_by_staff_id_not_found(self):
        """Test finding WFH requests by a non-existent staff ID."""
        response = self.client.get('/wfh_requests/staff_id/999999')
        self.assertEqual(response.status_code, 404)
        # self.assertIn(b"Employee with that ID number is not found.", response.data)

    def test_find_by_team_success(self):
        """Test finding WFH requests by team manager only."""
        response = self.client.get('/wfh_requests/team/140894')
        self.assertEqual(response.status_code, 200)
        # self.assertIn(b"Pending approval", response.data)

    def test_find_by_team_not_found(self):
        """Test finding WFH requests by a non-existent department or manager."""
        response = self.client.get('/wfh_requests/team/999999')
        self.assertEqual(response.status_code, 404)
        # self.assertIn(b"Department with name:HR is not found.", response.data)

    def test_delete_wfh_request_success(self):
        """Test deleting a WFH request successfully."""
        response = self.client.delete('/wfh_requests/withdraw/request_id/1')
        self.assertEqual(response.status_code, 200)
        # self.assertIn(b"successfully deleted", response.data)

    def test_delete_wfh_request_not_found(self):
        """Test deleting a non-existent WFH request."""
        response = self.client.delete('/wfh_requests/withdraw/request_id/999')
        self.assertEqual(response.status_code, 404)
        # self.assertIn(b"Work-from-home request with ID number:999 not found.", response.data)

if __name__ == '__main__':
    unittest.main()