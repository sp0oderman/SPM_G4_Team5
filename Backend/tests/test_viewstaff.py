import unittest
from flask_testing import TestCase
from ..view_schedule.view_staff_schedule import app, db, get_staff_schedule
from ..wfh_request import wfh_requests
import json

class TestStaffSchedule(TestCase):
    # Setup and teardown methods to prepare the test environment
    def create_app(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://test_user:test_password@localhost/test_db'
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        return app

    def setUp(self):
        db.create_all()

        # Create sample WFH requests for testing
        wfh1 = wfh_requests(staff_id=2, reporting_manager=3, dept="IT", chosen_date="2024-10-10",
                            arrangement_type="WFH", request_datetime="2024-10-08 10:00:00",
                            status="Pending", remarks="Testing")
        wfh2 = wfh_requests(staff_id=2, reporting_manager=3, dept="IT", chosen_date="2024-10-11",
                            arrangement_type="WFH", request_datetime="2024-10-08 12:00:00",
                            status="Approved", remarks="Testing Approved")
        db.session.add_all([wfh1, wfh2])
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    # Test HR can view any schedule
    def test_hr_can_view_any_schedule(self):
        response = self.client.get('/staff_schedule/2', headers={'X-User-Role': '1', 'X-User-ID': '1'})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(len(data['data']['schedule']), 2)  # HR should see all requests

    # Test staff can view their own schedule
    def test_staff_can_view_own_schedule(self):
        response = self.client.get('/staff_schedule/2', headers={'X-User-Role': '2', 'X-User-ID': '2'})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['data']['staff_id'], 2)  # Ensure correct staff ID

    # Test staff cannot view other staff's schedule
    def test_staff_cannot_view_other_schedule(self):
        response = self.client.get('/staff_schedule/3', headers={'X-User-Role': '2', 'X-User-ID': '2'})
        self.assertEqual(response.status_code, 403)
        data = json.loads(response.data)
        self.assertIn("Forbidden", data['message'])  # Staff should not view others

    # Test missing user info in headers (Unauthorized)
    def test_unauthorized_access(self):
        response = self.client.get('/staff_schedule/2')
        self.assertEqual(response.status_code, 401)
        data = json.loads(response.data)
        self.assertIn("Unauthorized", data['message'])

    # Test schedule not found for staff
    def test_no_schedule_found(self):
        response = self.client.get('/staff_schedule/999', headers={'X-User-Role': '1', 'X-User-ID': '1'})  # HR role
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data)
        self.assertIn("No schedule found", data['message'])

if __name__ == '__main__':
    unittest.main()
