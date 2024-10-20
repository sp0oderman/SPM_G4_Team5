import sys
# Get system path to wfh_request.py microservice
sys.path.append('../wfh_request')

import os
# Set FLASK_ENV to testing so that apply.py app uses sqlite URI instead of postgres URI
os.environ['FLASK_ENV'] = 'testing'  # Set the environment to testing

import unittest
from flask_testing import TestCase
from wfh_request import app, db, wfh_requests


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
        pendingRequest = wfh_requests(
            staff_id = 140002,
            reporting_manager = 140894,
            dept = "",
            chosen_date = "2024-04-10",
            arrangement_type = "am",
            request_datetime = "2024-01-01",
            status = "pending",
            remarks = "I am a pending request"
        )
        
        approvedRequest = wfh_requests(
            staff_id = 140002,
            reporting_manager = 140894,
            dept = "",
            chosen_date = "2024-04-10",
            arrangement_type = "pm",
            request_datetime = "2024-01-01",
            status = "approved",
            remarks = "I am a pending request"
        )

        db.session.add(pendingRequest)
        db.session.add(approvedRequest)
        db.session.commit()

    def tearDown(self):
        """Destroy the database after each test."""
        with app.app_context():
            db.session.remove()
            db.drop_all()


# Test cases
class TestWFHRequests(BaseTestCase):

    def test_homepage(self):
        """Test the homepage route."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Welcome to the homepage of the wfh_request microservice (SPM).", response.data)

    def test_get_all_requests(self):
        """Test retrieving all WFH requests."""
        response = self.client.get('/wfh_requests')
        self.assertEqual(response.status_code, 200)
        # self.assertIn(b"Pending approval", response.data)

    def test_get_all_requests_empty(self):
        """Test retrieving all WFH requests when none exist."""
        # Remove all records from the table instead of dropping the entire table
        with app.app_context():
            db.session.query(wfh_requests).delete()
            db.session.commit()
        response = self.client.get('/wfh_requests')
        self.assertEqual(response.status_code, 404)
        # self.assertIn(b"There are no work-from-home requests.", response.data)

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

    # def test_apply_wfh_application(self):
    #     """Test applying for a new WFH request."""
    #     response = self.client.post('/wfh_requests/apply', json={
    #         'staff_id': 140003,
    #         'reporting_manager': 140895,
    #         'dept': 'IT',
    #         'chosen_date': '2024-10-12',
    #         'arrangement_type': 'Full Day'
    #     })
    #     self.assertEqual(response.status_code, 201)
    #     self.assertIn(b"Work-from-home application successfully inserted.", response.data)

    # def test_apply_wfh_application_invalid_json(self):
    #     """Test applying for a WFH request with invalid JSON format."""
    #     response = self.client.post('/wfh_requests/apply', data="Invalid Data")
    #     self.assertEqual(response.status_code, 400)
    #     # self.assertIn(b"Application details should be in JSON.", response.data)

    def test_delete_wfh_request_success(self):
        """Test deleting a WFH request successfully."""
        response = self.client.delete('/wfh_requests/withdraw/1')
        self.assertEqual(response.status_code, 200)
        # self.assertIn(b"successfully deleted", response.data)

    def test_delete_wfh_request_not_found(self):
        """Test deleting a non-existent WFH request."""
        response = self.client.delete('/wfh_requests/withdraw/999')
        self.assertEqual(response.status_code, 404)
        # self.assertIn(b"Work-from-home request with ID number:999 not found.", response.data)

    # def test_process_application_details_error(self):
    #     """Test error handling in processApplicationDetails with missing fields."""
    #     response = self.client.post('/wfh_requests/apply', json={})
    #     # self.assertEqual(response.status_code, 500)

if __name__ == '__main__':
    unittest.main()