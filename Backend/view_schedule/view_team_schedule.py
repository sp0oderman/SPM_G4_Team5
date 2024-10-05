from flask import Flask, jsonify, request
from dotenv import load_dotenv
import os
from sqlalchemy.orm import aliased
from employee import employees
from wfh_request import db, wfh_requests
from functools import wraps
from sqlalchemy import text

load_dotenv()

postgres_user = os.getenv('POSTGRES_USER')
postgres_password = os.getenv('POSTGRES_PASSWORD')
postgres_host = os.getenv('POSTGRES_HOST')
postgres_db = os.getenv('POSTGRES_DB')

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{postgres_user}:{postgres_password}@{postgres_host}/{postgres_db}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

def access_control(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user_role = request.headers.get('X-User-Role')
        user_id = request.headers.get('X-User-ID')
        requested_manager_id = kwargs.get('reporting_manager')

        if not user_role or not user_id:
            return jsonify({"code": 401, "message": "Unauthorized: Missing user information"}), 401

        user_role = int(user_role)
        user_id = int(user_id)

        # HR can access any team schedule
        if user_role == 1:
            return f(*args, **kwargs)

        # For managers, check if they're requesting their own team
        if user_role == 3:
            if int(user_id) != int(requested_manager_id):
                return jsonify({"code": 403, "message": "Managers can only view their own team's schedule"}), 403
            return f(*args, **kwargs)

        # Get user's reporting manager
        user_reporting_manager = db.session.execute(text(
            "SELECT reporting_manager FROM employee WHERE staff_id = :user_id"
        ), {"user_id": user_id}).scalar()

        if user_reporting_manager is None:
            return jsonify({"code": 404, "message": "User not found"}), 404

        # Check if user is the manager or if they're requesting their own team's schedule
        if user_id != requested_manager_id and user_reporting_manager != requested_manager_id:
            return jsonify({"code": 403, "message": "Forbidden: You can only view your own team's schedule"}), 403

        return f(*args, **kwargs)
    return decorated_function


@app.route("/team_schedule/<int:reporting_manager>")
@access_control
def get_team_schedule(reporting_manager):
    department = request.args.get('department')
    user_role = int(request.headers.get('X-User-Role'))
    user_id = int(request.headers.get('X-User-ID'))

    # Create aliases for the employee table
    employee = aliased(employees)

    # HR (role 1) can access any team schedule without restrictions
    if user_role == 1:
        pass  # No additional checks needed for HR

    # For staff, verify they're only viewing their reporting manager's schedule
    elif user_role == 2:  # Staff role
        user_data = db.session.query(employees).filter(employees.staff_id == user_id).first()
        if not user_data or user_data.reporting_manager != reporting_manager:
            return jsonify({"code": 403, "message": "Staff can only view their own reporting manager's schedule"}), 403
        if department != user_data.dept:
            return jsonify({"code": 403, "message": "Staff can only view their own department"}), 403

    # For managers, verify department
    elif user_role == 3:
        if int(user_id) != int(reporting_manager):
            return jsonify({"code": 403, "message": "Managers can only view their own team's schedule"}), 403
        manager_dept = db.session.query(employees.dept).filter(employees.staff_id == user_id).scalar()
        if department != manager_dept:
            return jsonify({"code": 403, "message": "Managers can only view their own department"}), 403

    # Start with a query that joins wfh_requests and employee tables
    query = db.session.query(wfh_requests, employee).join(
        employee, wfh_requests.staff_id == employee.staff_id
    ).filter(employee.reporting_manager == reporting_manager)

    if department:
        query = query.filter(employee.dept == department)

    team_requests = query.all()

    if team_requests:
        return jsonify(
            {
                "code": 200,
                "data": {
                    "reporting_manager": reporting_manager,
                    "department": department,
                    "team_schedule": [{
                        **request.json(),
                        "reporting_manager": reporting_manager  # Override with the correct reporting_manager
                    } for request, emp in team_requests]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": f"No schedule found for team under reporting manager: {reporting_manager} in department: {department}"
        }
    ), 404


if __name__ == '__main__':
    app.run(port=5300, debug=True)