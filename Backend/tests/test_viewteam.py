import unittest
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from ..view_schedule.view_team_schedule import app, db, get_team_schedule
from ..wfh_request import wfh_requests
from ..employee import employees
from unittest.mock import patch

class TeamScheduleTestCase(unittest.TestCase):
    
    def setUp(self):
        """Set up test database and app"""
        self.app = app.test_client()
        self.app.testing = True

        # Setup in-memory database for testing
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

        db.create_all()  # Create tables
        self.setup_sample_employees()

    def tearDown(self):
        """Teardown test database"""
        db.session.remove()
        db.drop_all()  # Drop tables after each test

    def setup_sample_employees(self):
        """Helper method to add sample employees to the DB"""
        # Create mock employees
        employee1 = employees(
            staff_id=1, staff_fname="John", staff_lname="Doe", dept="HR", position="Manager",
            country="USA", email="john.doe@example.com", reporting_manager=None, role="1"
        )
        employee2 = employees(
            staff_id=2, staff_fname="Jane", staff_lname="Doe", dept="IT", position="Developer",
            country="USA", email="jane.doe@example.com", reporting_manager=1, role="2"
        )
        employee3 = employees(
            staff_id=3, staff_fname="Jack", staff_lname="Smith", dept="IT", position="Manager",
            country="USA", email="jack.smith@example.com", reporting_manager=None, role="3"
        )
        db.session.add(employee1)
        db.session.add(employee2)
        db.session.add(employee3)
        
        # Add sample WFH requests
        wfh_request1 = wfh_requests(
            staff_id=2, start_date="2024-10-01", end_date="2024-10-01", reason="Working from home",
            status="Approved"
        )
        wfh_request2 = wfh_requests(
            staff_id=2, start_date="2024-10-02", end_date="2024-10-02", reason="Working from home",
            status="Pending"
        )
        db.session.add(wfh_request1)
        db.session.add(wfh_request2)
        db.session.commit()

    def test_get_team_schedule_hr(self):
        """Test the '/team_schedule/<manager_id>' endpoint for HR role"""
        with self.app as client:
            response = client.get("/team_schedule/3?department=IT", 
                                  headers={"X-User-Role": "1", "X-User-ID": "1"})
            self.assertEqual(response.status_code, 200)
            data = response.get_json()
            self.assertIn("team_schedule", data["data"])
            self.assertEqual(len(data["data"]["team_schedule"]), 2)

    def test_get_team_schedule_manager(self):
        """Test the '/team_schedule/<manager_id>' endpoint for a Manager role"""
        with self.app as client:
            response = client.get("/team_schedule/3?department=IT", 
                                  headers={"X-User-Role": "3", "X-User-ID": "3"})
            self.assertEqual(response.status_code, 200)
            data = response.get_json()
            self.assertIn("team_schedule", data["data"])
            self.assertEqual(len(data["data"]["team_schedule"]), 2)

    def test_get_team_schedule_staff(self):
        """Test the '/team_schedule/<manager_id>' endpoint for Staff role"""
        with self.app as client:
            response = client.get("/team_schedule/3?department=IT", 
                                  headers={"X-User-Role": "2", "X-User-ID": "2"})
            self.assertEqual(response.status_code, 200)
            data = response.get_json()
            self.assertIn("team_schedule", data["data"])
            self.assertEqual(len(data["data"]["team_schedule"]), 2)

    def test_get_team_schedule_invalid_role(self):
        """Test the '/team_schedule/<manager_id>' endpoint for invalid role (not HR, Manager, or Staff)"""
        with self.app as client:
            response = client.get("/team_schedule/3?department=IT", 
                                  headers={"X-User-Role": "4", "X-User-ID": "4"})
            self.assertEqual(response.status_code, 401)
            data = response.get_json()
            self.assertEqual(data["message"], "Unauthorized: Missing user information")

    def test_unauthorized_access(self):
        """Test access control for unauthorized users (wrong role, missing role, etc.)"""
        with self.app as client:
            response = client.get("/team_schedule/3?department=IT", headers={"X-User-ID": "2"})
            self.assertEqual(response.status_code, 401)
            data = response.get_json()
            self.assertEqual(data["message"], "Unauthorized: Missing user information")

    def test_manager_access_to_other_team(self):
        """Test manager trying to access another team's schedule"""
        with self.app as client:
            response = client.get("/team_schedule/2?department=IT", 
                                  headers={"X-User-Role": "3", "X-User-ID": "3"})
            self.assertEqual(response.status_code, 403)
            data = response.get_json()
            self.assertEqual(data["message"], "Managers can only view their own team's schedule")

    def test_staff_access_to_other_manager(self):
        """Test staff trying to access a schedule not belonging to their reporting manager"""
        with self.app as client:
            response = client.get("/team_schedule/1?department=IT", 
                                  headers={"X-User-Role": "2", "X-User-ID": "2"})
            self.assertEqual(response.status_code, 403)
            data = response.get_json()
            self.assertEqual(data["message"], "Staff can only view their own reporting manager's schedule")

    def test_no_schedule_found(self):
        """Test when no team schedule is found for the reporting manager"""
        with self.app as client:
            response = client.get("/team_schedule/999?department=IT", 
                                  headers={"X-User-Role": "3", "X-User-ID": "3"})
            self.assertEqual(response.status_code, 404)
            data = response.get_json()
            self.assertEqual(data["message"], "No schedule found for team under reporting manager: 999 in department: IT")

if __name__ == '__main__':
    unittest.main()
