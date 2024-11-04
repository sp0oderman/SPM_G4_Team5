import unittest
from unittest.mock import MagicMock
from flask import Flask, jsonify
from src.routes.wfh_requests_routes import create_wfh_requests_blueprint  # Replace with the correct import path

class TestWFHRequestsBlueprint(unittest.TestCase):
    def setUp(self):
        # Create a Flask app and register the blueprint
        self.app = Flask(__name__)
        self.app.config['TESTING'] = True
        self.employees_service = MagicMock()
        self.wfh_requests_service = MagicMock()
        self.user_accounts_service = MagicMock()

        wfh_requests_blueprint = create_wfh_requests_blueprint(
            self.employees_service,
            self.wfh_requests_service,
            self.user_accounts_service
        )
        self.app.register_blueprint(wfh_requests_blueprint, url_prefix="/wfh")
        self.client = self.app.test_client()

    def test_get_team_by_reporting_manager_success(self):
        # Mock the service response
        self.wfh_requests_service.get_manager_team.return_value = ({"team": []}, 200)
        
        response = self.client.get("/wfh/get_manager_team/1")
        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertIn("data", data)
        self.assertIn("team", data["data"])

    def test_get_team_by_reporting_manager_error(self):
        self.wfh_requests_service.get_manager_team.return_value = ({"error": "Database error"}, 500)
        
        response = self.client.get("/wfh/get_manager_team/1")
        data = response.get_json()

        self.assertEqual(response.status_code, 500)
        self.assertEqual(data["message"], "An error occurred while retrieving the team data.")
        self.assertEqual(data["error"], "Database error")

    def test_apply_for_wfh_request_successful(self):
        # Mock successful WFH application
        self.wfh_requests_service.can_apply_wfh.return_value = True
        self.wfh_requests_service.apply_wfh.return_value = ({"message": "Request applied"}, 200)

        response = self.client.post("/wfh/apply_wfh", json={
            "staff_id": 1,
            "reporting_manager": 2,
            "dept": "Engineering",
            "chosen_date": "2024-11-04",
            "arrangement_type": "Remote",
            "request_datetime": "2024-11-01T08:00:00",
            "status": "Pending",
            "remarks": "WFH request"
        })

        self.assertEqual(response.status_code, 200)
        self.assertIn("message", response.get_json())
        self.assertEqual(response.get_json()["message"], "Request applied")

    def test_apply_for_wfh_request_missing_fields(self):
        response = self.client.post("/wfh/apply_wfh", json={})
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.get_json())
        self.assertEqual(response.get_json()["error"], "Missing required fields")

    def test_get_pending_wfh_requests_success(self):
        self.wfh_requests_service.view_pending_wfh_requests.return_value = ({"requests": []}, 200)
        
        response = self.client.get("/wfh/pending_wfh_requests?manager_id=1")
        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertIn("requests", data)

    def test_get_pending_wfh_requests_missing_manager_id(self):
        response = self.client.get("/wfh/pending_wfh_requests")
        data = response.get_json()

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data["error"], "Manager ID is required")

    def test_approve_pending_wfh_request(self):
        self.wfh_requests_service.approve_wfh_request.return_value = ({"message": "Request approved"}, 200)
        
        response = self.client.put("/wfh/approve_wfh_request", json={"request_id": 1, "manager_id": 2})
        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["message"], "Request approved")

    def test_reject_pending_wfh_request_missing_fields(self):
        response = self.client.put("/wfh/reject_wfh_request", json={"request_id": 1})
        data = response.get_json()

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data["error"], "Request ID and rejection reason are required")

    def test_get_all_wfh_requests_with_data(self):
        mock_request = MagicMock()
        mock_request.json.return_value = {"id": 1, "status": "Pending"}
        self.wfh_requests_service.get_all.return_value = [mock_request]

        response = self.client.get("/wfh/Pending")
        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertIn("wfh_requests", data["data"])

    def test_get_all_wfh_requests_no_data(self):
        self.wfh_requests_service.get_all.return_value = []

        response = self.client.get("/wfh/Pending")
        data = response.get_json()

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data["message"], "There are no work-from-home requests.")

    def test_withdraw_request_by_id_success(self):
        self.wfh_requests_service.delete_wfh_request.return_value = (200, None)

        response = self.client.delete("/wfh/withdraw/request_id/1")
        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["message"], "Work-from-home request with ID number:1 successfully deleted.")

    def test_withdraw_request_by_id_not_found(self):
        self.wfh_requests_service.delete_wfh_request.return_value = (404, None)

        response = self.client.delete("/wfh/withdraw/request_id/1")
        data = response.get_json()

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data["message"], "Work-from-home request with ID number:1 not found.")

    def test_withdraw_request_by_id_error(self):
        self.wfh_requests_service.delete_wfh_request.return_value = (500, "Database error")

        response = self.client.delete("/wfh/withdraw/request_id/1")
        data = response.get_json()

        self.assertEqual(response.status_code, 500)
        self.assertEqual(data["message"], "An error occurred while deleting the work-from-home request.")
        self.assertEqual(data["error"], "Database error")

if __name__ == "__main__":
    unittest.main()
