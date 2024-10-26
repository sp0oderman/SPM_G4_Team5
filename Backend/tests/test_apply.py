import sys
import os

# Add the root directory (where the `src` directory is located) to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

import unittest
from flask_testing import TestCase
from src.models.employees import Employees
from src.models.wfh_requests import WFH_Requests
from src.__init__ import db, create_app
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

        # Add a manager and two team members
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
        
        team_member_1 = Employees(
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
        
        team_member_2 = Employees(
            staff_id=140003, 
            staff_fname="Mark", 
            staff_lname="Brown", 
            dept="Sales", 
            position="Sales Associate", 
            country="USA", 
            email="mark.brown@example.com", 
            reporting_manager=140001,  # Reports to John Doe
            role=2
        )

        db.session.add(manager)
        db.session.add(team_member_1)
        db.session.add(team_member_2)
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
            'staff_id': 140002,
            'reporting_manager': 140001,
            'dept': 'Sales',
            'chosen_date': '2024-10-10',
            'arrangement_type': 'Full Day',
            'request_datetime': '2024-08-08',
            'status': 'Pending',
            'remarks': 'Doctor appointment'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"WFH request submitted successfully!", response.data)

    def test_apply_wfh_50_percent_rule(self):
        """Test applying for WFH fails if 50% of team already approved for WFH."""
        # Set an existing WFH request to be approved
        approved_request = WFH_Requests(
            staff_id=140002, 
            reporting_manager=140001,
            dept='Sales',
            chosen_date='2024-10-10', 
            arrangement_type='Full Day', 
            request_datetime='2024-08-08',
            status='Approved',
            remarks='Family event'
        )
        db.session.add(approved_request)
        db.session.commit()

        # Try to apply for WFH for another team member on the same date
        response = self.client.post('/wfh_requests/apply_wfh', json={
            'staff_id': 140003,
            'reporting_manager': 140001,
            'dept': 'Sales',
            'chosen_date': '2024-10-10',
            'arrangement_type': 'Full Day',
            'request_datetime': '2024-08-09',
            'status': 'Pending',
            'remarks': 'Personal reason'
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn(b"More than 50 percent of the team is already working from home on this date", response.data)

    def test_approve_wfh_50_percent_rule(self):
        """Test approving a WFH request fails if 50% of team already has approved WFH."""
        # Set an existing WFH request to be approved
        approved_request = WFH_Requests(
            staff_id=140002, 
            reporting_manager=140001,
            dept='Sales',
            chosen_date='2024-10-10', 
            arrangement_type='Full Day', 
            request_datetime='2024-08-08',
            status='Approved',
            remarks='Family event'
        )
        db.session.add(approved_request)
        
        # Create a new pending WFH request
        pending_request = WFH_Requests(
            staff_id=140003, 
            reporting_manager=140001,
            dept='Sales',
            chosen_date='2024-10-10', 
            arrangement_type='Full Day', 
            request_datetime='2024-08-09',
            status='Pending',
            remarks='Personal reason'
        )
        db.session.add(pending_request)
        db.session.commit()

        # Attempt to approve the pending request
        response = self.client.post('/wfh_requests/approve_wfh_request', json={
            'request_id': pending_request.request_id,
            'manager_id': 140001
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn(b"More than 50 percent of the team is already working from home on this date", response.data)

    def test_reject_wfh(self):
        """Test rejecting a WFH request."""
        # Create a WFH request
        wfh_request = WFH_Requests(
            staff_id=140002, 
            reporting_manager=140001,
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