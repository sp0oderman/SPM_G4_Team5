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
            email="jakob.lie.2022@smu.edu.sg",
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
            email="sthauheed.2022@smu.edu.sg",
            reporting_manager=140894,
            role=2
        )

        # Add a WFH request to be withdrawn
        approved_request = WFH_Requests(
            staff_id=140002,
            reporting_manager=140894,
            dept="Sales",
            chosen_date="2024-04-10",
            arrangement_type="am",
            request_datetime="2024-01-01",
            status="Approved",
            remarks="Approved request for withdrawal",
            recurring_id=-1,
            reason_for_status=None
        )

        db.session.add(reportingManager)
        db.session.add(employee)
        db.session.add(approved_request)
        db.session.commit()

    def tearDown(self):
        """Destroy the database after each test."""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()


class TestWithdrawalRequests(BaseTestCase):

    def test_apply_withdrawal_request_success(self):
        """Test applying to withdraw an approved WFH request successfully."""
        response = self.client.post('/withdrawal_requests/apply_withdrawal_request', json={
            'staff_id': 140002,
            'reporting_manager': 140894,
            'wfh_request_id': 1,
            'remarks': 'Need to cancel due to schedule change'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Withdrawal request submitted successfully!", response.data)

    def test_apply_withdrawal_request_missing_fields(self):
        """Test applying to withdraw a WFH request with missing required fields."""
        response = self.client.post('/withdrawal_requests/apply_withdrawal_request', json={
            'staff_id': 140002,
            'reporting_manager': 140894
            # Missing wfh_request_id and remarks
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn(b"Missing required fields", response.data)

    def test_approve_withdrawal_request_success(self):
        """Test approving a pending withdrawal request."""
        # Create a withdrawal request
        withdrawal_request = Withdrawal_Requests(
            staff_id=140002,
            reporting_manager=140894,
            wfh_request_id=1,
            request_datetime="2024-01-01",
            status="Pending",
            remarks="Request to cancel WFH",
            reason_for_status=None
        )
        db.session.add(withdrawal_request)
        db.session.commit()

        # Approve the withdrawal request
        response = self.client.put('/withdrawal_requests/approve_withdrawal_request', json={
            'request_id': withdrawal_request.request_id,
            'reason_for_status': 'Approved'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Withdrawal request approved and WFH requests withdrawn successfully!", response.data)

    def test_approve_withdrawal_request_not_found(self):
        """Test approving a withdrawal request that does not exist."""
        response = self.client.put('/withdrawal_requests/approve_withdrawal_request', json={
            'request_id': 999,
            'reason_for_status': 'Approved'
        })
        self.assertEqual(response.status_code, 404)
        self.assertIn(b"No pending withdrawal request found", response.data)

    def test_reject_withdrawal_request_success(self):
        """Test rejecting a pending withdrawal request."""
        # Create a withdrawal request
        withdrawal_request = Withdrawal_Requests(
            staff_id=140002,
            reporting_manager=140894,
            wfh_request_id=1,
            request_datetime="2024-01-01",
            status="Pending",
            remarks="Request to cancel WFH",
            reason_for_status=None
        )
        db.session.add(withdrawal_request)
        db.session.commit()

        # Reject the withdrawal request
        response = self.client.put('/withdrawal_requests/reject_withdrawal_request', json={
            'request_id': withdrawal_request.request_id,
            'reason_for_status': 'Insufficient coverage'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"rejected successfully", response.data)

    def test_reject_withdrawal_request_missing_fields(self):
        """Test rejecting a withdrawal request with missing required fields."""
        response = self.client.put('/withdrawal_requests/reject_withdrawal_request', json={
            'request_id': 1  # Missing reason_for_status
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn(b"Request ID and rejection reason are required", response.data)


if __name__ == '__main__':
    unittest.main()
