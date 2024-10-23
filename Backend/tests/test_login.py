import unittest
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import sys
import os

# Import employee
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'employee')))
from employee import app, db, employees

class LoginTestCase(unittest.TestCase):
    def setUp(self):
        """Set up test client and initialize database."""
        self.app = app
        self.client = self.app.test_client()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

        with self.app.app_context():
            db.create_all()
            # Add test employee to the database
            test_employee = employees(
                staff_id=1,
                staff_fname='John',
                staff_lname='Doe',
                dept='IT',
                position='Developer',
                country='USA',
                email='john.doe@example.com',
                reporting_manager=None,
                role='2'
            )
            db.session.add(test_employee)
            db.session.commit()

    def tearDown(self):
        """Tear down database."""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_login_success(self):
        """Test login functionality for existing employee."""
        response = self.client.get('/employees/auth/john.doe@example.com')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['code'], 200)
        self.assertEqual(data['data']['email'], 'john.doe@example.com')

    def test_login_failure(self):
        """Test login functionality for non-existing employee."""
        response = self.client.get('/employees/auth/nonexistent@example.com')
        self.assertEqual(response.status_code, 404)
        data = response.get_json()
        self.assertEqual(data['code'], 404)
        self.assertEqual(data['message'], 'Employee not found.')

if __name__ == '__main__':
    unittest.main()
