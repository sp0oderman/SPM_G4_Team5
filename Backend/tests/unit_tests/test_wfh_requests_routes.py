import pytest
from unittest.mock import MagicMock
from flask import Flask
from src.routes.wfh_requests_routes import create_wfh_requests_blueprint

# Fixture to set up the Flask app and mock service
@pytest.fixture
def app():
    # Create a MagicMock for the wfh_requests_service
    mock_wfh_requests_service = MagicMock()

    # Create a Flask app and register the blueprint
    app = Flask(__name__)
    blueprint = create_wfh_requests_blueprint(mock_wfh_requests_service)
    app.register_blueprint(blueprint)

    return app, mock_wfh_requests_service

@pytest.fixture
def client(app):
    app, _ = app
    with app.test_client() as client:
        yield client

def test_get_team_by_reporting_manager(client, app):
    _, mock_service = app
    mock_service.get_manager_team.return_value = ({"team": []}, 200)

    response = client.get("/get_manager_team/1")

    assert response.status_code == 200
    assert response.json == {
        "code": 200,
        "data": {"team": []}
    }

def test_apply_for_wfh_request(client, app):
    _, mock_service = app

    mock_service.can_apply_wfh.return_value = True
    mock_service.apply_wfh.return_value = ({"message": "Request submitted"}, 201)

    response = client.post("/apply_wfh", json={
        "staff_id": 1,
        "reporting_manager": 2,
        "dept": "Engineering",
        "chosen_date": "2023-12-01",
        "arrangement_type": "WFH",
        "request_datetime": "2023-11-01T10:00:00Z",
        "status": "Pending",
        "remarks": "Need to attend a personal matter"
    })

    assert response.status_code == 201
    assert response.json == {"message": "Request submitted"}

def test_get_pending_wfh_requests_of_own_team(client, app):
    _, mock_service = app

    mock_service.view_pending_wfh_requests.return_value = ({"requests": []}, 200)

    response = client.get("/pending_wfh_requests?manager_id=1")

    assert response.status_code == 200
    assert response.json == {"requests": []}

def test_approve_pending_wfh_request(client, app):
    _, mock_service = app

    mock_service.approve_wfh_request.return_value = ({"message": "Request approved"}, 200)

    response = client.post("/approve_wfh_request", json={"request_id": 1, "manager_id": 2})

    assert response.status_code == 200
    assert response.json == {"message": "Request approved"}

def test_reject_pending_wfh_request(client, app):
    _, mock_service = app

    mock_service.reject_wfh_request.return_value = ({"message": "Request rejected"}, 200)

    response = client.post("/reject_wfh_request", json={"request_id": 1, "rejection_reason": "Not enough justification"})

    assert response.status_code == 200
    assert response.json == {"message": "Request rejected"}

def test_get_all_wfh_requests(client, app):
    _, mock_service = app

    mock_service.get_all.return_value = []

    response = client.get("/pending")

    assert response.status_code == 404
    assert response.json == {"code": 404, "message": "There are no work-from-home requests."}

def test_get_wfh_request_by_request_id(client, app):
    _, mock_service = app

    mock_service.find_by_request_id.return_value = None

    response = client.get("/request_id/1")

    assert response.status_code == 404
    assert response.json == {"code": 404, "message": "Work-from-home request with that ID number is not found."}

def test_withdraw_request_by_id(client, app):
    _, mock_service = app

    mock_service.delete_wfh_request.return_value = (404, "Request not found")

    response = client.delete("/withdraw/request_id/1")

    assert response.status_code == 404
    assert response.json == {
        "code": 404,
        "message": "Work-from-home request with ID number:1 not found."
    }

# Additional Tests for Other Routes
def test_get_wfh_requests_by_staff_id(client, app):
    _, mock_service = app

    mock_service.find_by_staff_id.return_value = []

    response = client.get("/staff_id/1")

    assert response.status_code == 404
    assert response.json == {"code": 404, "message": "Employee with that ID number is not found."}

def test_get_wfh_requests_by_team(client, app):
    _, mock_service = app

    mock_service.find_by_team.return_value = []

    response = client.get("/team/1")

    assert response.status_code == 404
    assert response.json == {"code": 404, "message": "No requests from this team is not found."}
