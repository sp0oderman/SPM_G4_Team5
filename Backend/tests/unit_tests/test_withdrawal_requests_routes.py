import sys 
import os 
 
# Add the root directory (where the src directory is located) to the system path 
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

import unittest
from unittest.mock import MagicMock, patch
from flask import Flask, jsonify
from datetime import datetime
from src.routes.withdrawal_requests_routes import create_withdrawal_requests_blueprint

class TestWithdrawalRequestsRoutes(unittest.TestCase):
    def setUp(self):
        # Create a test Flask app and initialize the blueprint
        self.app = Flask(__name__)
        
        # Mock the services
        self.employees_service = MagicMock()
        self.wfh_requests_service = MagicMock()
        self.withdrawal_requests_service = MagicMock()
        
        # Register the blueprint with the app
        blueprint = create_withdrawal_requests_blueprint(
            self.employees_service,
            self.wfh_requests_service,
            self.withdrawal_requests_service
        )
        self.app.register_blueprint(blueprint)
        self.client = self.app.test_client()

    @patch("src.routes.withdrawal_requests_routes.datetime", wraps=datetime)
    def test_get_withdrawal_requests_by_team(self, mock_datetime):
        # Mock services to return expected data
        mock_withdrawal_request = MagicMock()
        mock_withdrawal_request.json.return_value = {"request_id": 1, "status": "Pending"}
        self.employees_service.find_by_team.return_value = (MagicMock(), [MagicMock(staff_id=1), MagicMock(staff_id=2)])
        self.withdrawal_requests_service.find_by_employees.return_value = [mock_withdrawal_request]

        # Perform the GET request
        response = self.client.get("/team/1/Pending")
        data = response.get_json()

        # Assertions
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["code"], 200)
        self.assertEqual(len(data["data"]["team_requests"]), 1)

    def test_get_withdrawal_requests_by_staff_id(self):
        # Mock the service to return a list of requests
        mock_withdrawal_request = MagicMock()
        mock_withdrawal_request.json.return_value = {"request_id": 1, "status": "Pending"}
        self.withdrawal_requests_service.find_by_staff_id.return_value = [mock_withdrawal_request]

        # Perform the GET request
        response = self.client.get("/staff_id/1/Pending")
        data = response.get_json()

        # Assertions
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["code"], 200)
        self.assertEqual(data["data"]["staff_id"], 1)
        self.assertEqual(len(data["data"]["requests"]), 1)

    def test_apply_withdrawal_request_missing_fields(self):
        # Perform the POST request with missing fields
        response = self.client.post("/apply_withdrawal_request", json={})
        data = response.get_json()

        # Assertions
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data["error"], "Missing required fields")

    def test_apply_withdrawal_request_conflicting_request(self):
        # Mock the can_apply_withdrawal method to return False
        self.withdrawal_requests_service.can_apply_withdrawal.return_value = False

        # Perform the POST request
        response = self.client.post("/apply_withdrawal_request", json={
            "staff_id": 1,
            "reporting_manager": 2,
            "wfh_request_id": 10,
            "remarks": "Requesting withdrawal"
        })
        data = response.get_json()

        # Assertions
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data["error"], "You have conflicting requests")

    def test_approve_withdrawal_request(self):
        # Mock the service to return a successful response
        self.withdrawal_requests_service.approve_withdrawal_request.return_value = ({"message": "Approved"}, 200)

        # Perform the PUT request
        response = self.client.put("/approve_withdrawal_request", json={
            "request_id": 1,
            "reason_for_status": "Approved for business reasons"
        })
        data = response.get_json()

        # Assertions
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["message"], "Approved")

    def test_reject_withdrawal_request_missing_fields(self):
        # Perform the PUT request with missing fields
        response = self.client.put("/reject_withdrawal_request", json={})
        data = response.get_json()

        # Assertions
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data["error"], "Request ID and rejection reason are required")

    def test_reject_withdrawal_request(self):
        # Mock the service to return a successful response
        self.withdrawal_requests_service.reject_withdrawal_request.return_value = ({"message": "Rejected"}, 200)

        # Perform the PUT request
        response = self.client.put("/reject_withdrawal_request", json={
            "request_id": 1,
            "reason_for_status": "Does not meet criteria"
        })
        data = response.get_json()

        # Assertions
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["message"], "Rejected")

if __name__ == "__main__":
    unittest.main()
