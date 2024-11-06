import sys
import os

# Add the root directory (where the `src` directory is located) to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

import unittest
from flask_testing import TestCase
from datetime import datetime

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
            staff_id=140894,
            staff_fname="managerfname",
            staff_lname="managerlname",
            dept="Sales",
            position="Sales Manager",
            country="Singapore",
            email="manager@example.com",
            reporting_manager=140001,
            role=3
        )

        # Add an employee who reports to the manager
        employee = Employees(
            staff_id=140002,
            staff_fname="empfname",
            staff_lname="emplname",
            dept="Sales",
            position="Account Manager",
            country="Singapore",
            email="employee@example.com",
            reporting_manager=140894,
            role=2
        )

        # Add WFH requests with different statuses
        pendingRequest = WFH_Requests(
            staff_id=140002,
            reporting_manager=140894,
            dept="Sales",
            chosen_date="2024-04-10",
            arrangement_type="am",
            request_datetime="2024-01-01",
            status="Pending",
            remarks="Pending request",
            recurring_id=-1,
            reason_for_status=None
        )
        
        approvedRequest = WFH_Requests(
            staff_id=140002,
            reporting_manager=140894,
            dept="Sales",
            chosen_date="2024-04-11",
            arrangement_type="pm",
            request_datetime="2024-01-02",
            status="Approved",
            remarks="Approved request",
            recurring_id=-1,
            reason_for_status=None
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

class TestWFHRoutes(BaseTestCase):

    def test_get_strength_by_team_and_date_range_success(self):
        """Test retrieving team strength by date range."""
        response = self.client.get('/wfh_requests/team/strength/140894/2024-04-01/2024-04-30')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"dates", response.data)  # Checks that the data structure is correct

    def test_get_strength_by_team_and_date_range_no_requests(self):
        """Test retrieving team strength by date range when no requests are found."""
        response = self.client.get('/wfh_requests/team/strength/140894/2025-04-01/2025-04-30')
        self.assertEqual(response.status_code, 404)
        self.assertIn(b"No requests from this team for this date is not found.", response.data)

    def test_get_wfh_requests_by_team_success(self):
        """Test retrieving WFH requests for a specific team manager."""
        response = self.client.get('/wfh_requests/team/140894/Pending')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"team_requests", response.data)  # Checks that the data structure is correct

    def test_get_wfh_requests_by_team_no_requests(self):
        """Test retrieving WFH requests for a team manager when no requests exist."""
        response = self.client.get('/wfh_requests/team/140894/Rejected')
        self.assertEqual(response.status_code, 404)
        self.assertIn(b"No requests from this team is not found.", response.data)

    def test_get_wfh_requests_by_staff_id_success(self):
        """Test retrieving WFH requests by a specific staff ID."""
        response = self.client.get('/wfh_requests/staff_id/140002/Pending')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"requests", response.data)  # Checks that the data structure is correct

    def test_get_wfh_requests_by_staff_id_no_requests(self):
        """Test retrieving WFH requests by a non-existent staff ID."""
        response = self.client.get('/wfh_requests/staff_id/999999/Pending')
        self.assertEqual(response.status_code, 404)
        self.assertIn(b"Employee with that ID number is not found.", response.data)

if __name__ == '__main__':
    unittest.main()
