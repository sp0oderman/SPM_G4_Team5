import sys
import os

# Add the root directory (where the `src` directory is located) to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

import unittest
from flask_testing import TestCase

from src.models.employees import Employees
from src.models.wfh_requests import WFH_Requests
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

        # Add an employee who reports to RM
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
        # Add an employee who reports to RM
        employee1 = Employees(
            staff_id=140001,
            staff_fname="empfname",
            staff_lname="emplname",
            dept="Sales",
            position="Account Manager",
            country="Singapore",
            email="sthauheed4.2022@smu.edu.sg",
            reporting_manager=140894,
            role=2
        )
        # Add an employee who reports to RM
        employee2 = Employees(
            staff_id=140009,
            staff_fname="empfname",
            staff_lname="emplname",
            dept="Sales",
            position="Account Manager",
            country="Singapore",
            email="sthauheed3.2022@smu.edu.sg",
            reporting_manager=140894,
            role=2
        )
        # Add an employee who reports to RM
        employee3 = Employees(
            staff_id=140008,
            staff_fname="empfname",
            staff_lname="emplname",
            dept="Sales",
            position="Account Manager",
            country="Singapore",
            email="sthauheed2.2022@smu.edu.sg",
            reporting_manager=140894,
            role=2
        )
        # Add an employee who reports to RM
        employee4 = Employees(
            staff_id=140007,
            staff_fname="empfname",
            staff_lname="emplname",
            dept="Sales",
            position="Account Manager",
            country="Singapore",
            email="sthauheed1.2022@smu.edu.sg",
            reporting_manager=140894,
            role=2
        )

        db.session.add(reportingManager)
        db.session.add(employee)
        db.session.add(employee1)
        db.session.add(employee2)
        db.session.add(employee3)
        db.session.add(employee4)
        db.session.commit()

    def tearDown(self):
        """Destroy the database after each test."""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

# Unit Test Cases
class TestWFHRequests(BaseTestCase):

    def test_apply_wfh_success(self):
        """Test applying for WFH successfully with all required fields."""
        response = self.client.post('/wfh_requests/apply_wfh_request', json={
            'staff_id': 140002,
            'reporting_manager': 140894,
            'dept': 'Sales',
            'chosen_date': '2024-10-10',
            'arrangement_type': 'Full Day',
            'request_datetime': '2024-08-08',
            'status': 'Pending',
            'remarks': 'Doctor appointment',
            'recurring_id': -1  # Non-recurring
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"WFH request submitted successfully", response.data)

    def test_apply_wfh_missing_fields(self):
        """Test WFH application with missing required fields."""
        response = self.client.post('/wfh_requests/apply_wfh_request', json={
            'staff_id': 140002,
            'reporting_manager': 140894,
            'dept': 'Sales',
            # Missing chosen_date and arrangement_type
            'remarks': 'Doctor appointment',
            'recurring_id': -1
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn(b"Missing required fields", response.data)

    def test_approve_wfh(self):
        """Test approving a single WFH request."""
        # Create a WFH request
        wfh_request = WFH_Requests(
            staff_id=140002, 
            reporting_manager=140894,
            dept='Sales',
            chosen_date='2024-10-10', 
            arrangement_type='Full Day', 
            request_datetime='2024-08-08',
            status='Pending',
            remarks='Doctor appointment',
            recurring_id=-1,
            reason_for_status=None
        )

        wfh_request2 = WFH_Requests(
            staff_id=140001, 
            reporting_manager=140894,
            dept='Sales',
            chosen_date='2024-10-10', 
            arrangement_type='Full Day', 
            request_datetime='2024-08-08',
            status='Pending',
            remarks='Doctor appointment',
            recurring_id=-1,
            reason_for_status=None
        )

        wfh_request3 = WFH_Requests(
            staff_id=140003, 
            reporting_manager=140894,
            dept='Sales',
            chosen_date='2024-10-10', 
            arrangement_type='Full Day', 
            request_datetime='2024-08-08',
            status='Pending',
            remarks='Doctor appointment',
            recurring_id=-1,
            reason_for_status=None
        )

        wfh_request4 = WFH_Requests(
            staff_id=140004, 
            reporting_manager=140894,
            dept='Sales',
            chosen_date='2024-10-10', 
            arrangement_type='Full Day', 
            request_datetime='2024-08-08',
            status='Pending',
            remarks='Doctor appointment',
            recurring_id=-1,
            reason_for_status=None
        )

        wfh_request5 = WFH_Requests(
            staff_id=140009, 
            reporting_manager=140894,
            dept='Sales',
            chosen_date='2024-10-10', 
            arrangement_type='Full Day', 
            request_datetime='2024-08-08',
            status='Pending',
            remarks='Doctor appointment',
            recurring_id=-1,
            reason_for_status=None
        )
        db.session.add(wfh_request)
        db.session.add(wfh_request2)
        db.session.add(wfh_request3)
        db.session.add(wfh_request4)
        db.session.add(wfh_request5)
        db.session.commit()

        # Approve the WFH request
        response = self.client.put('/wfh_requests/approve_wfh_request', json={
            'request_id': wfh_request.request_id,
            'reporting_manager': 140894,
            'reason_for_status': 'Approved for WFH',
            'recurring_id': -1
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"WFH request approved successfully", response.data)

    def test_reject_wfh(self):
        """Test rejecting a single WFH request."""
        # Create a WFH request
        wfh_request = WFH_Requests(
            staff_id=140002, 
            reporting_manager=140894,
            dept='Sales',
            chosen_date='2024-10-10', 
            arrangement_type='Full Day', 
            request_datetime='2024-08-08',
            status='Pending',
            remarks='Doctor appointment',
            recurring_id=-1,
            reason_for_status=None
        )
        db.session.add(wfh_request)
        db.session.commit()

        # Reject the WFH request
        response = self.client.put('/wfh_requests/reject_wfh_request', json={
            'request_id': wfh_request.request_id,
            'reason_for_status': 'Not enough coverage',
            'recurring_id': -1
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"WFH request rejected successfully", response.data)

    def test_apply_wfh_recurring_conflict(self):
        """Test applying for a recurring WFH request where a conflict exists on one date."""

        # Create a WFH request
        wfh_request = WFH_Requests(
            staff_id=140002, 
            reporting_manager=140894,
            dept='Sales',
            chosen_date='2024-10-10', 
            arrangement_type='Full Day', 
            request_datetime='2024-08-08',
            status='Pending',
            remarks='Doctor appointment',
            recurring_id=-1,
            reason_for_status=None
        )
        db.session.add(wfh_request)
        db.session.commit()

        response = self.client.post('/wfh_requests/apply_wfh_request', json={
            'staff_id': 140002,
            'reporting_manager': 140894,
            'dept': 'Sales',
            'chosen_date': '2024-10-10',
            'end_date': '2024-11-10',
            'arrangement_type': 'Full Day',
            'request_datetime': '2024-08-08',
            'status': 'Pending',
            'remarks': 'Weekly check-up',
            'recurring_id': 1  # Recurring request
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn(b"Conflict detected", response.data)

    def test_withdraw_wfh_request(self):
        """Test withdrawing an existing WFH request."""
        # Create a WFH request
        wfh_request = WFH_Requests(
            staff_id=140002,
            reporting_manager=140894,
            dept='Sales',
            chosen_date='2024-10-10',
            arrangement_type='Full Day',
            request_datetime='2024-08-08',
            status='Pending',
            remarks='Doctor appointment',
            recurring_id=-1,
            reason_for_status=None
        )
        db.session.add(wfh_request)
        db.session.commit()

        # Withdraw the WFH request
        response = self.client.put('/wfh_requests/withdraw_wfh_request', json={
            'request_id': wfh_request.request_id,
            'reason_for_status': 'Plans changed'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"WFH request withdrawn successfully", response.data)

if __name__ == '__main__':
    unittest.main()
