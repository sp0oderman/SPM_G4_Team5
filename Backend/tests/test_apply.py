import sys
import os

# Add the root directory (where the `src` directory is located) to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

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

        # Add a manager (John Doe) and a team member reporting to the manager
        manager = Employees(
            staff_id=140001, 
            staff_fname="John", 
            staff_lname="Doe", 
            dept="Sales", 
            position="Manager", 
            country="USA", 
            email="john.doe@example.com", 
            reporting_manager=None,
            role=3
        )
        
        team_member = Employees(
            staff_id=140002, 
            staff_fname="Jane", 
            staff_lname="Smith", 
            dept="Sales", 
            position="Sales Associate", 
            country="USA", 
            email="jane.smith@example.com", 
            reporting_manager=140001,  # Reports to John Doe
            role=2
        )

        db.session.add(manager)
        db.session.add(team_member)
        db.session.commit()

    def tearDown(self):
        """Destroy the database after each test."""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()


# Unit Test Cases
class TestApplyWFH(BaseTestCase):

    def test_apply_wfh_success(self):
        """Test applying for WFH successfully."""
        response = self.client.post('/wfh_requests/apply_wfh', json={
            'staff_id': 140001,
            'reporting_manager': 130002,
            'dept': 'Sales',
            'chosen_date': '2024-10-10',
            'arrangement_type': 'Full Day',
            'request_datetime': '2024-08-08',
            'status': 'Pending',
            'remarks': 'Doctor appointment'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"WFH request submitted successfully!", response.data)

    def test_apply_wfh_missing_fields(self):
        """Test WFH application with missing required fields."""
        response = self.client.post('/wfh_requests/apply_wfh', json={
            'staff_id': 140001,
            'requested_dates': '',  # Missing required requested dates
            'time_of_day': 'Full Day'
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn(b"Missing required fields", response.data)

    def test_approve_wfh(self):
        """Test approving a WFH request."""
        # Create a WFH request
        wfh_request = WFH_Requests(
            staff_id=140001, 
            reporting_manager=130002,
            dept='Sales',
            chosen_date='2024-10-10', 
            arrangement_type='Full Day', 
            request_datetime='2024-08-08',
            status='Pending',
            remarks='Doctor appointment'
        )
        db.session.add(wfh_request)
        db.session.commit()

        # Approve the WFH request
        response = self.client.post('/wfh_requests/approve_wfh_request', json={
            'request_id': wfh_request.request_id,
            'manager_id': 140001
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"WFH request approved successfully!", response.data)

    def test_reject_wfh(self):
        """Test rejecting a WFH request."""
        # Create a WFH request
        wfh_request = WFH_Requests(
            staff_id=140001, 
            reporting_manager=130002,
            dept='Sales',
            chosen_date='2024-10-10', 
            arrangement_type='Full Day', 
            request_datetime='2024-08-08',
            status='Pending',
            remarks='Doctor appointment'
        )
        db.session.add(wfh_request)
        db.session.commit()

        # Reject the WFH request
        response = self.client.post('/wfh_requests/reject_wfh_request', json={
            'request_id': wfh_request.request_id,
            'rejection_reason': 'Not enough coverage'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"WFH request rejected successfully!", response.data)

if __name__ == '__main__':
    unittest.main()