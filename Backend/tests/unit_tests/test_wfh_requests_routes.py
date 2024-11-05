import sys 
import os 
 
# Add the root directory (where the src directory is located) to the system path 
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

import unittest
from unittest.mock import MagicMock, patch
from flask import Flask, jsonify
from datetime import datetime
from src.routes.wfh_requests_routes import create_wfh_requests_blueprint

class TestWFHRequestsBlueprint(unittest.TestCase):
    def setUp(self):
        # Set up a Flask test client and mock services
        self.app = Flask(__name__)
        self.employees_service = MagicMock()
        self.wfh_requests_service = MagicMock()
        self.withdrawal_requests_service = MagicMock()

        # Register the blueprint with the test app
        blueprint = create_wfh_requests_blueprint(self.employees_service, self.wfh_requests_service, self.withdrawal_requests_service)
        self.app.register_blueprint(blueprint)
        self.client = self.app.test_client()

    def test_get_strength_by_team_and_date(self):
        # Mock response from wfh_requests_service
        self.wfh_requests_service.get_team_strength_by_date.return_value = {"AM": 3, "PM": 2}

        response = self.client.get("/wfh_requests/team/strength/1/2023-12-01")
        data = response.get_json()

        # Assertions
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["data"]["AM"], 3)
        self.assertEqual(data["data"]["PM"], 2)

    def test_get_strength_by_team_and_date_no_requests(self):
        self.wfh_requests_service.get_team_strength_by_date.return_value = {}

        response = self.client.get("/wfh_requests/team/strength/1/2023-12-01")
        data = response.get_json()

        # Assertions
        self.assertEqual(response.status_code, 404)
        self.assertIn("No requests from this team for this date is not found.", data["message"])

    def test_get_wfh_requests_by_team(self):
        mock_request = MagicMock()
        mock_request.json.return_value = {"request_id": 1, "status": "Pending"}
        self.employees_service.find_by_team.return_value = ("Manager", [mock_request])
        self.wfh_requests_service.find_by_employees.return_value = [mock_request]

        response = self.client.get("/wfh_requests/team/1/Pending")
        data = response.get_json()

        # Assertions
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data["data"]["team_requests"]), 1)
        self.assertEqual(data["data"]["team_requests"][0]["request_id"], 1)

    def test_apply_for_wfh_request_single(self):
        data = {
            "staff_id": 1,
            "reporting_manager": 2,
            "dept": "Engineering",
            "chosen_date": "2023-12-01",
            "arrangement_type": "Full Day",
            "remarks": "WFH request",
            "recurring_id": -1
        }
        self.wfh_requests_service.can_apply_wfh.return_value = True
        self.wfh_requests_service.apply_wfh.return_value = ({"message": "WFH request submitted successfully!"}, 200)

        response = self.client.post("/wfh_requests/apply_wfh_request", json=data)
        data = response.get_json()

        # Assertions
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["message"], "WFH request submitted successfully!")

    def test_apply_for_wfh_request_conflict(self):
        data = {
            "staff_id": 1,
            "reporting_manager": 2,
            "dept": "Engineering",
            "chosen_date": "2023-12-01",
            "arrangement_type": "Full Day",
            "remarks": "WFH request",
            "recurring_id": -1
        }
        self.wfh_requests_service.can_apply_wfh.return_value = False

        response = self.client.post("/wfh_requests/apply_wfh_request", json=data)
        data = response.get_json()

        # Assertions
        self.assertEqual(response.status_code, 400)
        self.assertIn("You have conflicting dates", data["error"])

    def test_approve_pending_wfh_request_single(self):
        data = {
            "request_id": 1,
            "reporting_manager": 2,
            "reason_for_status": "Approved"
        }
        self.wfh_requests_service.approve_wfh_request.return_value = ({"message": "WFH request approved successfully!"}, 200)

        response = self.client.put("/wfh_requests/approve_wfh_request", json=data)
        data = response.get_json()

        # Assertions
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["message"], "WFH request approved successfully!")

    def test_reject_pending_wfh_request_single(self):
        data = {
            "request_id": 1,
            "reason_for_status": "Rejected"
        }
        self.wfh_requests_service.reject_wfh_request.return_value = ({"message": "WFH request rejected successfully!"}, 200)

        response = self.client.put("/wfh_requests/reject_wfh_request", json=data)
        data = response.get_json()

        # Assertions
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["message"], "WFH request rejected successfully!")

    def test_withdraw_wfh_request(self):
        data = {
            "request_id": 1,
            "reason_for_status": "Changed plans"
        }
        self.wfh_requests_service.withdraw_wfh_request.return_value = ({"message": "WFH request withdrawn successfully!"}, 200)

        response = self.client.put("/wfh_requests/withdraw_wfh_request", json=data)
        data = response.get_json()

        # Assertions
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["message"], "WFH request withdrawn successfully!")

if __name__ == "__main__":
    unittest.main()
