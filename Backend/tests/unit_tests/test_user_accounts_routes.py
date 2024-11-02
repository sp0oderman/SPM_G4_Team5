import pytest
from flask import Flask, session
from unittest.mock import MagicMock
from src.routes.user_accounts_routes import create_user_accounts_blueprint  # Adjust the import to your file structure


@pytest.fixture
def client():
    # Create a Flask app and register the blueprint for testing
    app = Flask(__name__, template_folder="../../src/templates")
    app.secret_key = 'test_secret_key'  # Needed for session management

    user_accounts_service = MagicMock()
    employees_service = MagicMock()

    user_accounts_blueprint = create_user_accounts_blueprint(user_accounts_service, employees_service)
    app.register_blueprint(user_accounts_blueprint, url_prefix='/accounts')

    client = app.test_client()

    yield client, user_accounts_service, employees_service


def test_login_successful(client):
    client, user_accounts_service, _ = client

    # Mock login response
    user_accounts_service.login.return_value = ({'user': {'staff_id': 1, 'username': 'test_user'}}, 200)

    response = client.post('/accounts/login', data={'username': 'test_user', 'password': 'test_pass'})

    # Check if the response redirects to the index page
    assert response.status_code == 302
    assert response.location.endswith('/accounts/index')

    # Check if the user is stored in session
    with client.session_transaction() as sess:
        assert 'user' in sess
        assert sess['user']['username'] == 'test_user'


def test_login_invalid_credentials(client):
    client, user_accounts_service, _ = client

    # Mock invalid login credentials response
    user_accounts_service.login.return_value = ({'message': 'Invalid credentials'}, 401)

    response = client.post('/accounts/login', data={'username': 'test_user', 'password': 'wrong_pass'})
    assert response.status_code == 200
    assert b'Invalid credentials' in response.data


def test_login_user_not_found(client):
    client, user_accounts_service, _ = client

    # Mock user not found scenario
    user_accounts_service.login.return_value = ({'message': 'User not found'}, 404)

    response = client.post('/accounts/login', data={'username': 'nonexistent_user', 'password': 'password'})
    assert response.status_code == 200
    assert b'User not found' in response.data


def test_logout(client):
    client, _, _ = client

    # Simulate a logged-in user
    with client.session_transaction() as sess:
        sess['user'] = {'staff_id': 1, 'username': 'test_user', 'role': 2}

    # Call logout route
    response = client.get('/accounts/logout')

    # Check if the session was cleared and the user is redirected to login
    with client.session_transaction() as sess:
        assert 'user' not in sess
    assert response.status_code == 302
    assert response.location.endswith('/accounts/login')


def test_display_index_page_logged_in(client):
    client, _, employees_service = client

    # Simulate a logged-in user in session
    with client.session_transaction() as sess:
        sess['user'] = {
        'staff_id': 1,
        'username': 'test_user',
        'role': 2,
        'staff_fname': 'Test',
        'staff_lname': 'User'
    }

    # Mock employee data from employees_service
    mock_employee = MagicMock()
    mock_employee.reporting_manager = 'Manager Name'
    mock_employee.dept = 'HR'
    employees_service.find_by_staff_id.return_value = mock_employee

    response = client.get('/accounts/index')

    # Check if the employee's details are added to session
    with client.session_transaction() as sess:
        assert sess['user']['reporting_manager'] == 'Manager Name'
        assert sess['user']['dept'] == 'HR'

    assert response.status_code == 200


def test_display_index_page_redirect_when_not_logged_in(client):
    client, _, _ = client

    # No user in session, the index page should redirect to login
    response = client.get('/accounts/index')

    assert response.status_code == 302
    assert response.location.endswith('/accounts/login')


def test_display_index_page_employee_not_found(client):
    client, _, employees_service = client

    # Simulate a logged-in user
    with client.session_transaction() as sess:
        sess['user'] = {
            'staff_id': 1,
            'username': 'test_user',
            'role': 2,
            'staff_fname': 'Test',
            'staff_lname': 'User'
        }

    # Mock case where employee is not found
    employees_service.find_by_staff_id.return_value = None

    response = client.get('/accounts/index')

    # Check that 'reporting_manager' and 'dept' are None in the session
    with client.session_transaction() as sess:
        assert sess['user']['reporting_manager'] is None
        assert sess['user']['dept'] is None

    assert response.status_code == 200
