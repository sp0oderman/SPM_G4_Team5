import os
from flask_testing import TestCase
from wfh_request import app, db, wfh_requests

# Set the environment to testing (not necessary but can help)
os.environ['FLASK_ENV'] = 'testing'

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
        with app.app_context():
            db.create_all()

        # Add sample WFH requests for testing
        pendingRequest = wfh_requests(
            staff_id=140002,
            reporting_manager=140894,
            dept="IT",
            chosen_date="2024-04-10",
            arrangement_type="am",
            request_datetime="2024-01-01",
            status="pending",
            remarks="I am a pending request"
        )

        approvedRequest = wfh_requests(
            staff_id=140002,
            reporting_manager=140894,
            dept="IT",
            chosen_date="2024-04-10",
            arrangement_type="pm",
            request_datetime="2024-01-01",
            status="approved",
            remarks="I am an approved request"
        )

        db.session.add(pendingRequest)
        db.session.add(approvedRequest)
        db.session.commit()

    def tearDown(self):
        """Destroy the database after each test."""
        with app.app_context():
            db.session.remove()
            db.drop_all()

# Example test cases
class TestStaffSchedule(BaseTestCase):

    def test_hr_can_view_any_schedule(self):
        response = self.client.get('/staff_schedule/140002', headers={'X-User-Role': '1', 'X-User-ID': '140894'})
        self.assertEqual(response.status_code, 200)
        self.assertIn("schedule", response.json["data"])

    def test_staff_can_view_own_schedule(self):
        response = self.client.get('/staff_schedule/140002', headers={'X-User-Role': '2', 'X-User-ID': '140002'})
        self.assertEqual(response.status_code, 200)

    def test_staff_cannot_view_others_schedule(self):
        response = self.client.get('/staff_schedule/140002', headers={'X-User-Role': '2', 'X-User-ID': '140003'})
        self.assertEqual(response.status_code, 403)
        self.assertIn("Forbidden", response.json["message"])

if __name__ == '__main__':
    import unittest
    unittest.main()
