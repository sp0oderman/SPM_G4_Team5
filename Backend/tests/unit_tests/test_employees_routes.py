import sys 
import os 
 
# Add the root directory (where the src directory is located) to the system path 
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

import unittest
from unittest.mock import MagicMock
from flask import Flask
from src.routes.employees_routes import create_employees_blueprint  # Update with correct path

class TestEmployeesRoutes(unittest.TestCase):
    def setUp(self):
        # Create a Flask app and register the blueprint
        self.app = Flask(__name__)
        self.employees_service = MagicMock()
        self.wfh_requests_service = MagicMock()
        self.withdrawal_requests_service = MagicMock()

        # Register the blueprint
        employees_blueprint = create_employees_blueprint(
            self.employees_service, self.wfh_requests_service, self.withdrawal_requests_service
        )
        self.app.register_blueprint(employees_blueprint, url_prefix="/employees")

        # Initialize test client
        self.client = self.app.test_client()

    def test_get_all_reporting_managers_success(self):
        # Mock the service response
        mock_employee = MagicMock()
        mock_employee.json.return_value = {"id": 1, "name": "John Doe"}
        self.employees_service.get_all_reporting_managers.return_value = [mock_employee]

        # Call the route
        response = self.client.get("/employees/reporting_managers_list")
        data = response.get_json()

        # Assertions
        self.assertEqual(response.status_code, 200)
        self.assertIn("reporting_managers", data["data"])
        self.assertEqual(data["data"]["reporting_managers"][0]["name"], "John Doe")

    def test_get_all_reporting_managers_not_found(self):
        self.employees_service.get_all_reporting_managers.return_value = []

        response = self.client.get("/employees/reporting_managers_list")
        data = response.get_json()

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data["message"], "There are no employees.")

    def test_get_reporting_managers_under_me_success(self):
        mock_employee = MagicMock()
        mock_employee.json.return_value = {"id": 2, "name": "Jane Doe"}
        self.employees_service.get_reporting_managers_under_me.return_value = [mock_employee]

        response = self.client.get("/employees/reporting_managers_under_me_list/1")
        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertIn("reporting_managers", data["data"])
        self.assertEqual(data["data"]["reporting_managers"][0]["name"], "Jane Doe")

    def test_get_reporting_managers_under_me_not_found(self):
        self.employees_service.get_reporting_managers_under_me.return_value = []

        response = self.client.get("/employees/reporting_managers_under_me_list/1")
        data = response.get_json()

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data["message"], "There are no subordinates who are also managers.")

    def test_get_team_size_success(self):
        self.employees_service.get_team_size.return_value = 5

        response = self.client.get("/employees/team/size/1")
        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["data"]["team_size"], 5)

    def test_get_team_size_not_found(self):
        self.employees_service.get_team_size.return_value = 0

        response = self.client.get("/employees/team/size/1")
        data = response.get_json()

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data["message"], "There is no team with this manager.")

    def test_get_all_employees_success(self):
        mock_employee = MagicMock()
        mock_employee.json.return_value = {"id": 1, "name": "John Doe"}
        self.employees_service.get_all.return_value = [mock_employee]

        response = self.client.get("/employees/")
        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertIn("employees", data["data"])
        self.assertEqual(data["data"]["employees"][0]["name"], "John Doe")

    def test_get_all_employees_not_found(self):
        self.employees_service.get_all.return_value = []

        response = self.client.get("/employees/")
        data = response.get_json()

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data["message"], "There are no employees.")

    def test_get_list_of_departments_success(self):
        self.employees_service.get_departments_list.return_value = ["HR", "Engineering"]

        response = self.client.get("/employees/dept_list")
        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertIn("departments", data["data"])
        self.assertIn("HR", data["data"]["departments"])

    def test_get_list_of_departments_not_found(self):
        self.employees_service.get_departments_list.return_value = []

        response = self.client.get("/employees/dept_list")
        data = response.get_json()

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data["message"], "No departments found.")

    def test_get_staff_by_id_success(self):
        mock_employee = MagicMock()
        mock_employee.json.return_value = {"id": 1, "name": "John Doe"}
        self.employees_service.find_by_staff_id.return_value = mock_employee

        response = self.client.get("/employees/staff/1")
        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["data"]["employee"]["name"], "John Doe")

    def test_get_staff_by_id_not_found(self):
        self.employees_service.find_by_staff_id.return_value = None

        response = self.client.get("/employees/staff/1")
        data = response.get_json()

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data["message"], "Employee not found.")

    # Add similar tests for remaining routes like get_team_by_reporting_manager, get_staff_by_dept, etc.

if __name__ == "__main__":
    unittest.main()
