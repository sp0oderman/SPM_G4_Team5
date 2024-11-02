import unittest
from unittest.mock import MagicMock
from src.models.user_accounts import User_Accounts
from src.models.employees import Employees
from src.services.user_accounts_services import User_Accounts_Service


class TestUserAccountsService(unittest.TestCase):
    def setUp(self):
        # Create a mock database session
        self.mock_db = MagicMock()
        self.user_service = User_Accounts_Service(self.mock_db)
        
        # Sample User_Accounts and Employees instances for tests

        self.mock_user = User_Accounts(
            login_id=1,
            last_login=None,
            role=2,
            username="johndoe", 
            password_hash="hashed_password", 
            staff_id=1
        )
        self.mock_employee = Employees(
            staff_id=1,
            staff_fname="John",
            staff_lname="Doe",
            dept="IT",
            position="staff",
            country="Singapore",
            role=2,
            email="john.doe@example.com",
            reporting_manager=3
        )

    def test_login_successful(self):
        # Mock return values for successful login
        self.mock_db.session.query().filter_by().first.side_effect = [self.mock_user, self.mock_employee]

        response, status_code = self.user_service.login("johndoe", "hashed_password")
        
        # Check response details and status code
        self.assertEqual(status_code, 200)
        self.assertTrue(response["success"])
        self.assertEqual(response["user"]["staff_id"], self.mock_employee.staff_id)
        self.assertEqual(response["user"]["staff_fname"], self.mock_employee.staff_fname)
        self.assertEqual(response["user"]["role"], self.mock_employee.role)
        self.mock_db.session.query().filter_by.assert_called()

    def test_login_invalid_credentials(self):
        # Mock return value for invalid credentials (user not found)
        self.mock_db.session.query().filter_by().first.return_value = None
        
        response, status_code = self.user_service.login("johndoe", "wrong_password")
        
        # Check response details and status code
        self.assertEqual(status_code, 401)
        self.assertFalse(response["success"])
        self.assertEqual(response["message"], "Invalid credentials")
        self.mock_db.session.query().filter_by.call_count == 2

    def test_login_employee_not_found(self):
        # Mock return value for user found, but employee not found
        self.mock_db.session.query().filter_by().first.side_effect = [self.mock_user, None]
        
        response, status_code = self.user_service.login("johndoe", "hashed_password")
        
        # Check response details and status code
        self.assertEqual(status_code, 404)
        self.assertFalse(response["success"])
        self.assertEqual(response["message"], "Employee details not found")
        self.mock_db.session.query().filter_by.assert_called()

    def test_login_wrong_password(self):
        # Mock return value for wrong password (user found but password does not match)
        self.mock_db.session.query().filter_by().first.return_value = self.mock_user
        
        response, status_code = self.user_service.login("johndoe", "wrong_password")
        
        # Check response details and status code
        self.assertEqual(status_code, 401)
        self.assertFalse(response["success"])
        self.assertEqual(response["message"], "Invalid credentials")
        self.mock_db.session.query().filter_by.call_count == 2


if __name__ == "__main__":
    unittest.main()
