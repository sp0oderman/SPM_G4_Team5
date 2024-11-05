import sys 
import os 
 
# Add the root directory (where the src directory is located) to the system path 
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

import unittest
from unittest.mock import MagicMock
from src.services.employees_services import Employees_Service  # Update the import path as necessary
from src.models.employees import Employees

class TestEmployeesService(unittest.TestCase):
    def setUp(self):
        # Set up a mock database session
        self.db = MagicMock()
        self.service = Employees_Service(self.db)

    def test_get_all_reporting_managers(self):
        # Mock the response for distinct reporting_manager_ids
        self.db.session.scalars.return_value.all.return_value = [1, 2]
        mock_manager1 = MagicMock(staff_id=1)
        mock_manager2 = MagicMock(staff_id=2)
        self.db.session.query.return_value.filter.return_value.all.return_value = [mock_manager1, mock_manager2]

        result = self.service.get_all_reporting_managers()

        # Assertions
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].staff_id, 1)
        self.assertEqual(result[1].staff_id, 2)

    def test_get_reporting_managers_under_me(self):
        # Mock distinct reporting_manager_ids
        self.db.session.scalars.return_value.all.return_value = [2]
        mock_manager = MagicMock(staff_id=2, reporting_manager=1)
        self.db.session.query.return_value.filter.return_value.all.return_value = [mock_manager]

        result = self.service.get_reporting_managers_under_me(reporting_manager_id_num=1)

        # Assertions
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].staff_id, 2)
        self.assertEqual(result[0].reporting_manager, 1)

    def test_find_by_team(self):
        # Create a mock manager and team members as Employees instances
        mock_manager = Employees(
            staff_id=1, staff_fname="Manager", staff_lname="One",
            dept="Sales", position="Manager", country="Singapore",
            email="manager.one@example.com", reporting_manager=None, role=3
        )
        
        mock_team_member1 = Employees(
            staff_id=2, staff_fname="Team", staff_lname="Member1",
            dept="Sales", position="Sales Rep", country="Singapore",
            email="member.one@example.com", reporting_manager=1, role=2
        )
        
        mock_team_member2 = Employees(
            staff_id=3, staff_fname="Team", staff_lname="Member2",
            dept="Sales", position="Sales Rep", country="Singapore",
            email="member.two@example.com", reporting_manager=1, role=2
        )

        # Mock the query calls for the manager and team members separately
        # Mock for finding the manager by staff_id (returns the manager)
        self.db.session.query.return_value.filter_by.return_value.first.side_effect = lambda: mock_manager

        # Mock for finding all team members under the manager
        self.db.session.query.return_value.filter_by.return_value.all.side_effect = lambda: [mock_team_member1, mock_team_member2]

        # Call the method under test
        team_manager, team_list = self.service.find_by_team(reporting_manager_id_num=1)

        # Assertions
        self.assertEqual(team_manager.staff_id, 1)
        self.assertEqual(len(team_list), 2)
        self.assertEqual(team_list[0].staff_id, 2)
        self.assertEqual(team_list[1].staff_id, 3)

    def test_find_by_team_no_manager(self):
        # Mock no manager found
        self.db.session.query.return_value.filter_by.return_value.first.return_value = None

        team_manager, team_list = self.service.find_by_team(reporting_manager_id_num=99)

        # Assertions
        self.assertIsNone(team_manager)
        self.assertEqual(len(team_list), 0)

    def test_find_by_staff_id(self):
        # Create a mock employee instance with a specific staff_id
        mock_employee = Employees(staff_id=1, staff_fname="John", staff_lname="Doe",
                                  dept="Sales", position="Manager", country="Singapore",
                                  email="john.doe@example.com", reporting_manager=100001, role=3)
        
        # Configure the mock database session to return the mock employee
        self.db.session.query.return_value.filter_by.return_value.first.return_value = mock_employee

        # Call the method under test
        result = self.service.find_by_staff_id(staff_id_num=1)

        # Assertions
        self.assertEqual(result.staff_id, 1)
        self.assertEqual(result.staff_fname, "John")

    def test_get_team_size(self):
        # Mock team size count
        self.db.session.query.return_value.filter.return_value.count.return_value = 3

        team_size = self.service.get_team_size(reporting_manager_id_num=1)

        # Assertions
        self.assertEqual(team_size, 3)

if __name__ == "__main__":
    unittest.main()
