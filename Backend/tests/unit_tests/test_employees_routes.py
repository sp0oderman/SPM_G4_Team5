import unittest
from unittest.mock import MagicMock
from flask import Flask
from src.routes.employees_routes import create_employees_blueprint  # Replace with the correct import path

class TestEmployeesBlueprint(unittest.TestCase):
    def setUp(self):
        # Create a Flask app and register the blueprint
        self.app = Flask(__name__)
        self.employees_service = MagicMock()
        self.wfh_requests_service = MagicMock()
        self.user_accounts_service = MagicMock()

        employees_blueprint = create_employees_blueprint(
            self.employees_service, 
            self.wfh_requests_service, 
            self.user_accounts_service
        )
        self.app.register_blueprint(employees_blueprint, url_prefix="/employees")

        self.client = self.app.test_client()

    def test_get_all_employees_with_data(self):
        # Mock the response from employees_service.get_all()
        mock_employee = MagicMock()
        mock_employee.json.return_value = {"id": 1, "name": "John Doe"}
        self.employees_service.get_all.return_value = [mock_employee]

        response = self.client.get("/employees/")
        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertIn("employees", data["data"])
        self.assertEqual(data["data"]["employees"][0]["name"], "John Doe")

    def test_get_all_employees_no_data(self):
        self.employees_service.get_all.return_value = []
        response = self.client.get("/employees/")
        data = response.get_json()

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data["message"], "There are no employees.")

    def test_get_list_of_departments_with_data(self):
        self.employees_service.get_departments_list.return_value = ["HR", "Engineering"]
        response = self.client.get("/employees/dept_list")
        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertIn("departments", data["data"])
        self.assertIn("HR", data["data"]["departments"])

    def test_get_list_of_departments_no_data(self):
        self.employees_service.get_departments_list.return_value = []
        response = self.client.get("/employees/dept_list")
        data = response.get_json()

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data["message"], "No departments found.")

    def test_get_staff_by_id_found(self):
        mock_employee = MagicMock()
        mock_employee.json.return_value = {"id": 1, "name": "John Doe"}
        self.employees_service.find_by_staff_id.return_value = mock_employee

        response = self.client.get("/employees/staff/1")
        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["data"]["staff_id"], 1)
        self.assertEqual(data["data"]["employee"]["name"], "John Doe")

    def test_get_staff_by_id_not_found(self):
        self.employees_service.find_by_staff_id.return_value = None
        response = self.client.get("/employees/staff/1")
        data = response.get_json()

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data["message"], "Employee not found.")

    def test_get_team_by_reporting_manager_found(self):
        mock_manager = MagicMock()
        mock_manager.json.return_value = {"id": 1, "name": "Manager Name"}
        mock_team_member = MagicMock()
        mock_team_member.json.return_value = {"id": 2, "name": "Team Member"}
        self.employees_service.find_by_team.return_value = (mock_manager, [mock_team_member])

        response = self.client.get("/employees/team/1")
        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["data"]["team_manager"]["name"], "Manager Name")
        self.assertEqual(data["data"]["team_list"][0]["name"], "Team Member")

    def test_get_team_by_reporting_manager_not_found(self):
        self.employees_service.find_by_team.return_value = (None, [])
        response = self.client.get("/employees/team/1")
        data = response.get_json()

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data["message"], "Team manager not found.")

    def test_get_staff_by_dept_found(self):
        mock_employee = MagicMock()
        mock_employee.json.return_value = {"id": 1, "name": "John Doe"}
        self.employees_service.find_by_dept.return_value = [mock_employee]

        response = self.client.get("/employees/staff/dept/HR")
        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["data"]["dept"], "HR")
        self.assertEqual(data["data"]["employees"][0]["name"], "John Doe")

    def test_get_staff_by_dept_not_found(self):
        self.employees_service.find_by_dept.return_value = []
        response = self.client.get("/employees/staff/dept/HR")
        data = response.get_json()

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data["message"], "Department not found.")

    def test_get_staff_by_email_found(self):
        mock_employee = MagicMock()
        mock_employee.json.return_value = {"id": 1, "name": "John Doe", "email": "john@example.com"}
        self.employees_service.find_by_email.return_value = mock_employee

        response = self.client.get("/employees/staff/email/john@example.com")
        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["data"]["name"], "John Doe")

    def test_get_staff_by_email_not_found(self):
        self.employees_service.find_by_email.return_value = None
        response = self.client.get("/employees/staff/email/john@example.com")
        data = response.get_json()

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data["message"], "Employee not found.")

if __name__ == "__main__":
    unittest.main()
