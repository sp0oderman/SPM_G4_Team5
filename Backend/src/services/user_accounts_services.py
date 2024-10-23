from src.models.user_accounts import User_Accounts
from src.models.employees import Employees
from src.__init__ import db

@app.route('/login', methods=['POST'])
def login(username, password):

    user = User_Accounts.query.filter_by(username=username).first()

    if user and user.password_hash == password:  # Note: In a real app, use proper password hashing
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
