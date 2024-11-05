import sys
import os

# Add the root directory (where the `src` directory is located) to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

import unittest
from flask_testing import TestCase
from datetime import datetime

from src.models.withdrawal_requests import Withdrawal_Requests
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

        # Add a pending and an approved withdrawal request
        pending_request = Withdrawal_Requests(
            staff_id=140002,
            reporting_manager=140894,
            wfh_request_id=1,
            request_datetime="2024-01-01",
            status="Pending",
            remarks="Pending request to withdraw WFH",
            reason_for_status=None
        )

        approved_request = Withdrawal_Requests(
            staff_id=140002,
            reporting_manager=140894,
            wfh_request_id=2,
            request_datetime="2024-01-02",
            status="Approved",
            remarks="Approved request to withdraw WFH",
            reason_for_status="Approved by manager"
        )

        db.session.add(reportingManager)
        db.session.add(employee)
        db.session.add(pending_request)
        db.session.add(approved_request)
        db.session.commit()

    def tearDown(self):
        """Destroy the database after each test."""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()


class TestWithdrawalRequestsByTeamAndStaff(BaseTestCase):

    def test_get_withdrawal_requests_by_team_success(self):
        """Test retrieving withdrawal requests for a specific team manager with a given status."""
        response = self.client.get('/withdrawal_requests/team/140894/Pending')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"team_requests", response.data)  # Checks that the data structure is correct
        self.assertIn(b"Pending request to withdraw WFH", response.data)  # Checks specific content

    def test_get_withdrawal_requests_by_team_no_requests(self):
        """Test retrieving withdrawal requests for a team manager when no requests of the given status exist."""
        response = self.client.get('/withdrawal_requests/team/140894/Rejected')
        self.assertEqual(response.status_code, 404)
        self.assertIn(b"No requests from this team is not found.", response.data)

    def test_get_withdrawal_requests_by_staff_id_success(self):
        """Test retrieving withdrawal requests by a specific staff ID with a given status."""
        response = self.client.get('/withdrawal_requests/staff_id/140002/Approved')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"requests", response.data)  # Checks that the data structure is correct
        self.assertIn(b"Approved request to withdraw WFH", response.data)  # Checks specific content

    def test_get_withdrawal_requests_by_staff_id_no_requests(self):
        """Test retrieving withdrawal requests by a specific staff ID when no requests with the given status exist."""
        response = self.client.get('/withdrawal_requests/staff_id/140002/Rejected')
        self.assertEqual(response.status_code, 404)
        self.assertIn(b"There are no Withdrawal Requests for staff with that ID number.", response.data)

    def test_get_withdrawal_requests_by_staff_id_nonexistent_staff(self):
        """Test retrieving withdrawal requests for a non-existent staff ID."""
        response = self.client.get('/withdrawal_requests/staff_id/999999/Pending')
        self.assertEqual(response.status_code, 404)
        self.assertIn(b"There are no Withdrawal Requests for staff with that ID number.", response.data)


if __name__ == '__main__':
    unittest.main()