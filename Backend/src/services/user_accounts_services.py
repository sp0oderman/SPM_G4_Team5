from src.models.user_accounts import User_Accounts
from src.models.employees import Employees

class User_Accounts_Service:
    def __init__(self, db):
        self.db = db

    def login(self, username, password):
        user = self.db.session.query(User_Accounts).filter_by(username=username).first()

        if user and user.password_hash == password:  # Note: In a real app, use proper password hashing

            # Check if staff_id is present in employees table 
            employee = Employees.query.filter_by(staff_id=user.staff_id).first()

            if employee:
                return {
                    "success": True,
                    "user": {
                        "staff_id": employee.staff_id,
                        "staff_fname": employee.staff_fname,
                        "staff_lname": employee.staff_lname,
                        "role": employee.role,
                        "dept": employee.dept,
                        "position": employee.position
                    }
                }, 200
            else:
                return {"success": False, "message": "Employee details not found"}, 404
        else:
            return {"success": False, "message": "Invalid credentials"}, 401
