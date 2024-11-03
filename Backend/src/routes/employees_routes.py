from flask import Blueprint, jsonify
# from src.utils.hr_auth import hr_required

# Create a blueprint for wfh_requests_routes
def create_employees_blueprint(employees_service, wfh_requests_service):
    employees_blueprint = Blueprint('employees_blueprint', __name__)


    # Get all employees from employees database model
    @employees_blueprint.route('/', methods=['GET'])
    # @hr_required
    def get_all_employees():
        employee_list = employees_service.get_all()

        if len(employee_list):
            return jsonify(
                {
                    "code": 200,
                    "data": {
                        "employees": [employee.json() for employee in employee_list]
                    }
                }
            )
        return jsonify(
            {
                "code": 404,
                "message": "There are no employees."
            }
        ), 404

    # Get all departments from employees database model
    @employees_blueprint.route('/dept_list', methods=['GET'])
    def get_list_of_departments():
        departments_list = employees_service.get_departments_list()

        if departments_list:
            return jsonify(
                {
                    "code": 200,
                    "data": {
                        "departments": departments_list
                    }
                }
            )
        return jsonify(
            {
                "code": 404,
                "message": "No departments found."
            }
        ), 404

    # Get specific employee by staff_id from employees database model
    @employees_blueprint.route('/staff/<int:staff_id_num>', methods=['GET'])
    # @hr_required
    def get_staff_by_id(staff_id_num):
        employee = employees_service.find_by_staff_id(staff_id_num)

        if employee:
            return jsonify(
                {
                    "code": 200,
                    "data": {
                        "staff_id": staff_id_num,
                        "employee": employee.json()
                    }
                }
            )
        return jsonify(
            {
                "code": 404,
                "message": "Employee not found."
            }
        ), 404


    # Get all employees in a specific team from employees database model
    @employees_blueprint.route('/team/<int:reporting_manager_id_num>', methods=['GET'])
    # @hr_required
    def get_team_by_reporting_manager(reporting_manager_id_num):
        team_manager, team_list = employees_service.find_by_team(reporting_manager_id_num)

        if team_manager is None:
            return jsonify(
                {
                    "code": 404,
                    "message": "Team manager not found."
                }
            ), 404

        if len(team_list) > 0:
            return jsonify(
                {
                    "code": 200,
                    "data": {
                        # when the json returns, the team_manager data is all the way at the bottom
                        "team_manager": team_manager.json(),
                        "team_list": [employee.json() for employee in team_list]
                    }
                }
            )
        return jsonify(
            {
                "code": 404,
                "message": f"Staff ID provided:{reporting_manager_id_num} does not have a team."
            }
        ), 404

    # Get all employees in a specific department from employees database model
    @employees_blueprint.route("/staff/dept/<string:dept_name>")
    # @hr_required
    def get_staff_by_dept(dept_name):
        dept_list = employees_service.find_by_dept(dept_name)

        if len(dept_list):
            return jsonify(
                {
                    "code": 200,
                    "data": {
                        "dept": dept_name,
                        "employees": [employee.json() for employee in dept_list]
                    }
                }
            )
        return jsonify(
            {
                "code": 404,
                "message": "Department not found."
            }
        ), 404

    # Get all employees with a specific role from employees database model
    @employees_blueprint.route("/staff/role/<string:role_num>")
    # @hr_required
    def get_staff_by_role(role_num):
        role_list = employees_service.find_by_role(role_num)

        if len(role_list):
            return jsonify(
                {
                    "code": 200,
                    "data": {
                        "role": role_num,
                        "employees": [employee.json() for employee in role_list]
                    }
                }
            )
        return jsonify(
            {
                "code": 404,
                "message": "Role not found."
            }
        ), 404

    # Get specific employee by unique email from employees databse model
    @employees_blueprint.route("/staff/email/<string:staff_email>")
    def get_staff_by_email(staff_email):
        employee = employees_service.find_by_email(staff_email)
        
        if employee:
            return jsonify(
                {
                    "code": 200,
                    "data": employee.json()
                }
            )
        return jsonify(
            {
                "code": 404,
                "message": "Employee not found."
            }
        ), 404
    
    return employees_blueprint