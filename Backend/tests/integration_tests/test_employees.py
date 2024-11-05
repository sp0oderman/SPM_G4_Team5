import sys
import os

# Add the root directory (where the `src` directory is located) to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

import unittest
from flask_testing import TestCase

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

        # Add a CEO-level manager
        ceo = Employees(
            staff_id=100001,
            staff_fname="ceo_fname",
            staff_lname="ceo_lname",
            dept="Executive",
            position="CEO",
            country="Singapore",
            email="ceo@example.com",
            reporting_manager=None,  # No reporting manager for CEO
            role=5  # Highest level role
        )

        # Add a reporting manager under the CEO
        manager = Employees(
            staff_id=100002,
            staff_fname="manager_fname",
            staff_lname="manager_lname",
            dept="Sales",
            position="Sales Manager",
            country="Singapore",
            email="manager@example.com",
            reporting_manager=100001,  # Reports to CEO
            role=3
        )

        # Add an employee reporting to the manager
        employee = Employees(
            staff_id=100003,
            staff_fname="employee_fname",
            staff_lname="employee_lname",
            dept="Sales",
            position="Account Manager",
            country="Singapore",
            email="employee@example.com",
            reporting_manager=100002,  # Reports to Sales Manager
            role=2
        )

        db.session.add(ceo)
        db.session.add(manager)
        db.session.add(employee)
        db.session.commit()

    def tearDown(self):
        """Destroy the database after each test."""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()


class TestEmployeesRoutes(BaseTestCase):

    def test_get_all_reporting_managers_success(self):
        """Test retrieving a list of all reporting managers."""
        response = self.client.get('/employees/reporting_managers_list')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"reporting_managers", response.data)
        self.assertIn(b"manager_fname", response.data)

    def test_get_all_reporting_managers_no_managers(self):
        """Test retrieving a list of all reporting managers when none exist."""
        with self.app.app_context():
            db.session.query(Employees).delete()  # Remove all employees
            db.session.commit()
        
        response = self.client.get('/employees/reporting_managers_list')
        self.assertEqual(response.status_code, 404)
        self.assertIn(b"There are no employees.", response.data)

    def test_get_reporting_managers_under_me_success(self):
        """Test retrieving reporting managers who report to a specific manager."""
        response = self.client.get('/employees/reporting_managers_under_me_list/100001')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"reporting_managers", response.data)
        self.assertIn(b"manager_fname", response.data)

    def test_get_reporting_managers_under_me_no_subordinates(self):
        """Test retrieving reporting managers under a specific manager when none exist."""
        response = self.client.get('/employees/reporting_managers_under_me_list/100002')
        self.assertEqual(response.status_code, 404)
        self.assertIn(b"There are no subordinates who are also managers.", response.data)

    def test_get_team_size_success(self):
        """Test retrieving the size of a team for a specific reporting manager."""
        response = self.client.get('/employees/team/size/100002')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"team_size", response.data)
        self.assertIn(b'1', response.data)  # Asserts that team size is 1

    def test_get_team_size_no_team(self):
        """Test retrieving team size for a manager with no team members."""
        response = self.client.get('/employees/team/size/100003')  # Employee with no subordinates
        self.assertEqual(response.status_code, 404)
        self.assertIn(b"There is no team with this manager.", response.data)


if __name__ == '__main__':
    unittest.main()
