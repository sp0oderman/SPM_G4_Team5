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

        db.session.add(manager)
        db.session.commit()

    def tearDown(self):
        """Destroy the database after each test."""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

# Unit Test Cases         
class LoginTestCase(BaseTestCase):

    def test_login_success(self):
        """Test login functionality for existing employee."""
        response = self.client.get('/employees/staff/email/john.doe@example.com')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['code'], 200)
        self.assertEqual(data['data']['email'], 'john.doe@example.com')

    def test_login_failure(self):
        """Test login functionality for nonexistent employee."""
        response = self.client.get('/employees/staff/email/nonexistent@example.com')
        self.assertEqual(response.status_code, 404)
        data = response.get_json()
        self.assertEqual(data['code'], 404)
        self.assertEqual(data['message'], 'Employee not found.')

if __name__ == '__main__':
    unittest.main()
