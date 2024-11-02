import pytest
from flask import Flask
from unittest.mock import MagicMock
from src.routes.employees_routes import create_employees_blueprint  # Adjust import to match your structure


@pytest.fixture
def client():
    # Create a Flask app and register the blueprint for testing
    app = Flask(__name__)
    employees_service = MagicMock()  # Mock the employees_service
    employees_blueprint = create_employees_blueprint(employees_service)
    app.register_blueprint(employees_blueprint, url_prefix='/employees')
    client = app.test_client()

    yield client, employees_service


def test_get_all_employees(client):
    client, employees_service = client
    # Mock the return value of employees_service.get_all()
    employees_service.get_all.return_value = [MagicMock(json=lambda: {"name": "John Doe", "role": 2})]

    response = client.get('/employees/')
    assert response.status_code == 200
    assert response.json['code'] == 200
    assert len(response.json['data']['employees']) == 1
    assert response.json['data']['employees'][0]['name'] == 'John Doe'

    # Test case when no employees are found
    employees_service.get_all.return_value = []
    response = client.get('/employees/')
    assert response.status_code == 404
    assert response.json['message'] == "There are no employees."


def test_get_list_of_departments(client):
    client, employees_service = client
    # Mock the return value of employees_service.get_departments_list()
    employees_service.get_departments_list.return_value = ["HR", "Engineering", "Marketing"]

    response = client.get('/employees/dept_list')
    assert response.status_code == 200
    assert response.json['code'] == 200
    assert response.json['data']['departments'] == ["HR", "Engineering", "Marketing"]

    # Test case when no departments are found
    employees_service.get_departments_list.return_value = []
    response = client.get('/employees/dept_list')
    assert response.status_code == 404
    assert response.json['message'] == "No departments found."


def test_get_staff_by_id(client):
    client, employees_service = client
    # Mock the return value of employees_service.find_by_staff_id()
    employees_service.find_by_staff_id.return_value = MagicMock(json=lambda: {"staff_id": 1, "name": "Jane Doe"})

    response = client.get('/employees/staff/1')
    assert response.status_code == 200
    assert response.json['code'] == 200
    assert response.json['data']['employee']['name'] == "Jane Doe"

    # Test case when the employee is not found
    employees_service.find_by_staff_id.return_value = None
    response = client.get('/employees/staff/999')
    assert response.status_code == 404
    assert response.json['message'] == "Employee not found."


def test_get_team_by_reporting_manager(client):
    client, employees_service = client
    # Mock the return value of employees_service.find_by_team()
    team_manager_mock = MagicMock(json=lambda: {"staff_id": 1, "name": "John Manager"})
    team_list_mock = [MagicMock(json=lambda: {"name": "Employee 1"}), MagicMock(json=lambda: {"name": "Employee 2"})]
    employees_service.find_by_team.return_value = (team_manager_mock, team_list_mock)

    response = client.get('/employees/team/1')
    assert response.status_code == 200
    assert response.json['code'] == 200
    assert response.json['data']['team_manager']['name'] == "John Manager"
    assert len(response.json['data']['team_list']) == 2

    # Test case when the team manager is not found
    employees_service.find_by_team.return_value = (None, [])
    response = client.get('/employees/team/999')
    assert response.status_code == 404
    assert response.json['message'] == "Team manager not found."


def test_get_staff_by_dept(client):
    client, employees_service = client
    # Mock the return value of employees_service.find_by_dept()
    employees_service.find_by_dept.return_value = [MagicMock(json=lambda: {"name": "Employee 1"}), MagicMock(json=lambda: {"name": "Employee 2"})]

    response = client.get('/employees/staff/dept/HR')
    assert response.status_code == 200
    assert response.json['code'] == 200
    assert len(response.json['data']['employees']) == 2

    # Test case when department is not found
    employees_service.find_by_dept.return_value = []
    response = client.get('/employees/staff/dept/UnknownDept')
    assert response.status_code == 404
    assert response.json['message'] == "Department not found."


def test_get_staff_by_role(client):
    client, employees_service = client
    # Mock the return value of employees_service.find_by_role()
    employees_service.find_by_role.return_value = [MagicMock(json=lambda: {"name": "Employee 1"}), MagicMock(json=lambda: {"name": "Employee 2"})]

    response = client.get('/employees/staff/role/1')
    assert response.status_code == 200
    assert response.json['code'] == 200
    assert len(response.json['data']['employees']) == 2

    # Test case when role is not found
    employees_service.find_by_role.return_value = []
    response = client.get('/employees/staff/role/999')
    assert response.status_code == 404
    assert response.json['message'] == "Role not found."


def test_get_staff_by_email(client):
    client, employees_service = client
    # Mock the return value of employees_service.find_by_email()
    employees_service.find_by_email.return_value = MagicMock(json=lambda: {"name": "Jane Doe", "email": "jane@example.com"})

    response = client.get('/employees/staff/email/jane@example.com')
    assert response.status_code == 200
    assert response.json['code'] == 200
    assert response.json['data']['name'] == "Jane Doe"

    # Test case when employee email is not found
    employees_service.find_by_email.return_value = None
    response = client.get('/employees/staff/email/unknown@example.com')
    assert response.status_code == 404
    assert response.json['message'] == "Employee not found."
