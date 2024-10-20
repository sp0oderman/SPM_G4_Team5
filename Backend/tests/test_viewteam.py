import unittest
from flask_testing import TestCase
from wfh_request import app, db, wfh_requests
from employee import employees

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
        db.create_all()

        # Sample employees and WFH requests for testing
        employee1 = employees(staff_id=140002, reporting_manager=140894, dept="IT")
        employee2 = employees(staff_id=140003, reporting_manager=140894, dept="IT")
        employee3 = employees(staff_id=140894, reporting_manager=140001, dept="HR")  # Manager

        wfh_request1 = wfh_requests(
            staff_id=140002,
            reporting_manager=140894,
            dept="IT",
            chosen_date="2024-04-10",
            arrangement_type="WFH",
            request_datetime="2024-01-01 09:00:00",
            status="pending",
            remarks="Pending request"
        )

        wfh_request2 = wfh_requests(
            staff_id=140003,
            reporting_manager=140894,
            dept="IT",
            chosen_date="2024-04-12",
            arrangement_type="WFH",
            request_datetime="2024-01-02 10:00:00",
            status="approved",
            remarks="Approved request"
        )

        # Add them to the session
        db.session.add_all([employee1, employee2, employee3, wfh_request1, wfh_request2])
        db.session.commit()

    def tearDown(self):
        """Destroy the database after each test."""
        db.session.remove()
        db.drop_all()

class TestTeamSchedule(BaseTestCase):
    """Test case for the /team_schedule endpoint."""

    def test_hr_access(self):
        """Test that HR can access any team schedule."""
        headers = {
            'X-User-Role': '1',  # HR role
            'X-User-ID': '140001'
        }
        response = self.client.get('/team_schedule/140894?department=IT', headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertIn('team_schedule', response.json['data'])

    def test_manager_access(self):
        """Test that a manager can access their own team's schedule."""
        headers = {
            'X-User-Role': '3',  # Manager role
            'X-User-ID': '140894'
        }
        response = self.client.get('/team_schedule/140894?department=IT', headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertIn('team_schedule', response.json['data'])

    def test_staff_access_own_team(self):
        """Test that staff can access their own manager's schedule."""
        headers = {
            'X-User-Role': '2',  # Staff role
            'X-User-ID': '140002'
        }
        response = self.client.get('/team_schedule/140894?department=IT', headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertIn('team_schedule', response.json['data'])

    def test_staff_access_forbidden(self):
        """Test that staff cannot access another team's schedule."""
        headers = {
            'X-User-Role': '2',  # Staff role
            'X-User-ID': '140002'
        }
        response = self.client.get('/team_schedule/140001?department=HR', headers=headers)
        self.assertEqual(response.status_code, 403)
        self.assertIn('Forbidden', response.json['message'])

    def test_no_schedule_found(self):
        """Test when no schedule is found for a given manager."""
        headers = {
            'X-User-Role': '3',  # Manager role
            'X-User-ID': '140894'
        }
        response = self.client.get('/team_schedule/999999?department=Nonexistent', headers=headers)
        self.assertEqual(response.status_code, 404)
        self.assertIn('No schedule found', response.json['message'])


if __name__ == '__main__':
    unittest.main()