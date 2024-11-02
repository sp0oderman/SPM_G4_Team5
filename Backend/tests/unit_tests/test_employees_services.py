import unittest
from unittest.mock import MagicMock
from src.models.employees import Employees
from src.services.employees_services import Employees_Service


class TestEmployeesService(unittest.TestCase):
    def setUp(self):
        # Create a mock database session
        self.mock_db = MagicMock()
        self.employee_service = Employees_Service(self.mock_db)
       
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

    def test_get_all(self):
        # Mock the return value of the database query
        self.mock_db.session.scalars.return_value.all.return_value = [self.mock_employee]
        
        result = self.employee_service.get_all()
        
        # Assert that the mock employee is in the result
        self.assertEqual(result, [self.mock_employee])
        self.mock_db.session.scalars.assert_called_once()

    def test_get_departments_list(self):
        # Mock the return value for department list query
        self.mock_db.session.scalars.return_value.all.return_value = ["IT", "HR"]
        
        result = self.employee_service.get_departments_list()
        
        self.assertEqual(result, ["IT", "HR"])
        self.mock_db.session.scalars.assert_called_once()

    def test_find_by_staff_id(self):
        # Mock the return value of a single employee by staff_id
        self.mock_db.session.scalars.return_value.first.return_value = self.mock_employee
        
        result = self.employee_service.find_by_staff_id(1)
        
        self.assertEqual(result, self.mock_employee)
        self.mock_db.session.scalars.assert_called_once()

    def test_find_by_team(self):
        # Mock the return values of a team manager and team list
        self.mock_db.session.scalars.side_effect = [
            MagicMock(first=MagicMock(return_value=self.mock_employee)),  # Manager
            MagicMock(all=MagicMock(return_value=[self.mock_employee]))    # Team list
        ]
        
        manager, team = self.employee_service.find_by_team(3)
        
        self.assertEqual(manager, self.mock_employee)
        self.assertEqual(team, [self.mock_employee])
        self.mock_db.session.scalars.assert_called()

    def test_find_by_dept(self):
        # Mock the return value for employees in a department
        self.mock_db.session.scalars.return_value.all.return_value = [self.mock_employee]
        
        result = self.employee_service.find_by_dept("IT")
        
        self.assertEqual(result, [self.mock_employee])
        self.mock_db.session.scalars.assert_called_once()

    def test_find_by_role(self):
        # Mock the return value for employees with a specific role
        self.mock_db.session.scalars.return_value.all.return_value = [self.mock_employee]
        
        result = self.employee_service.find_by_role(2)
        
        self.assertEqual(result, [self.mock_employee])
        self.mock_db.session.scalars.assert_called_once()

    def test_find_by_email(self):
        # Mock the return value for an employee found by email
        self.mock_db.session.scalars.return_value.first.return_value = self.mock_employee
        
        result = self.employee_service.find_by_email("john.doe@example.com")
        
        self.assertEqual(result, self.mock_employee)
        self.mock_db.session.scalars.assert_called_once()


if __name__ == "__main__":
    unittest.main()
