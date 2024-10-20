# import sys
# # Get system path to apply.py microservice
# sys.path.append('../apply_wfh')

import os
# Set FLASK_ENV to testing so that apply.py app uses sqlite URI instead of postgres URI
os.environ['FLASK_ENV'] = 'testing'  # Set the environment to testing

import unittest
from flask_testing import TestCase
from apply import app, db, Employee, WFHRequest


app.config['TESTING'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # In-memory database for testing
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

class BaseTestCase(TestCase):
    """Base test case to set up the Flask test client and the database."""
    
    def create_app(self):
        """Configure the app for testing with an in-memory SQLite database."""
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # In-memory database for testing
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        return app

    def setUp(self):
        """Set up the database and create the tables before each test."""
        # Ensure the correct database URI is applied early
        with app.app_context():
            db.create_all()

        # Add a manager (John Doe) and a team member reporting to the manager
        manager = Employee(
            Staff_ID=140001, 
            Staff_FName="John", 
            Staff_LName="Doe", 
            Dept="Sales", 
            Position="Manager", 
            Country="USA", 
            Email="john.doe@example.com", 
            Role=3
        )
        
        team_member = Employee(
            Staff_ID=140002, 
            Staff_FName="Jane", 
            Staff_LName="Smith", 
            Dept="Sales", 
            Position="Sales Associate", 
            Country="USA", 
            Email="jane.smith@example.com", 
            Reporting_Manager=140001,  # Reports to John Doe
            Role=2
        )

        db.session.add(manager)
        db.session.add(team_member)
        db.session.commit()

    def tearDown(self):
        """Destroy the database after each test."""
        with app.app_context():
            db.session.remove()
            db.drop_all()


# Unit Test Cases
class TestApplyWFH(BaseTestCase):

    def test_apply_wfh_success(self):
        """Test applying for WFH successfully."""
        response = self.client.post('/apply_wfh', json={
            'staff_id': 140001,
            'requested_dates': ['2024-10-10'],
            'time_of_day': 'Full Day',
            'reason': 'Doctor appointment'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"WFH request submitted successfully!", response.data)

    def test_apply_wfh_missing_fields(self):
        """Test WFH application with missing required fields."""
        response = self.client.post('/apply_wfh', json={
            'staff_id': 140001,
            'requested_dates': [],  # Missing required requested dates
            'time_of_day': 'Full Day'
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn(b"Missing required fields", response.data)

    def test_approve_wfh(self):
        """Test approving a WFH request."""
        # Create a WFH request
        wfh_request = WFHRequest(
            staff_id=140001, 
            requested_dates='2024-10-10', 
            time_of_day='Full Day', 
            reason='Doctor appointment'
        )
        db.session.add(wfh_request)
        db.session.commit()

        # Approve the WFH request
        response = self.client.post('/approve_wfh_request', json={
            'request_id': wfh_request.id,
            'manager_id': 140001
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"WFH request approved successfully!", response.data)

    def test_reject_wfh(self):
        """Test rejecting a WFH request."""
        # Create a WFH request
        wfh_request = WFHRequest(
            staff_id=140001, 
            requested_dates='2024-10-10', 
            time_of_day='Full Day', 
            reason='Doctor appointment'
        )
        db.session.add(wfh_request)
        db.session.commit()

        # Reject the WFH request
        response = self.client.post('/reject_wfh_request', json={
            'request_id': wfh_request.id,
            'rejection_reason': 'Not enough coverage'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"WFH request rejected successfully!", response.data)

if __name__ == '__main__':
    unittest.main()