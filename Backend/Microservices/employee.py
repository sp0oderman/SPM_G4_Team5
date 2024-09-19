from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import psycopg2
from dotenv import load_dotenv
import os

from sqlalchemy import or_, and_

load_dotenv()

postgres_user = os.getenv('POSTGRES_USER')
postgres_password = os.getenv('POSTGRES_PASSWORD')
postgres_host = os.getenv('POSTGRES_HOST')
postgres_db = os.getenv('POSTGRES_DB')

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{postgres_user}:{postgres_password}@{postgres_host}/{postgres_db}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class employees(db.Model):
    __tablename__ = 'employee'

    staff_id = db.Column(db.Integer, primary_key=True)
    staff_fname = db.Column(db.String(100), nullable=False)
    staff_lname = db.Column(db.String(100), nullable=False)
    dept = db.Column(db.String(100), nullable=False)
    position = db.Column(db.String(100), nullable=False)
    country = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    reporting_manager = db.Column(db.Integer, nullable=True)
    role = db.Column(db.String(100), nullable=False)

    def __init__(self, staff_id, staff_fname, staff_lname, dept, position, country, email, reporting_manager, role):
        self.staff_id = staff_id
        self.staff_fname = staff_fname
        self.staff_lname = staff_lname
        self.dept = dept
        self.position = position
        self.country = country
        self.email = email
        self.reporting_manager = reporting_manager
        self.role = role

    def json(self):
        return {
                "staff_id": self.staff_id,
                "staff_fname": self.staff_fname,
                "staff_lname": self.staff_lname,
                "dept": self.dept,
                "position": self.position,
                "country": self.country,
                "email": self.email,
                "reporting_manager": self.reporting_manager,
                "role": self.role
            }

@app.route("/")
def homepage():
    return "Welcome to the homepage of the employee microservice (SPM)."

@app.route("/employees")
def get_all():
    employee_list = db.session.scalars(db.select(employees)).all()

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


@app.route("/employees/<int:staff_id_num>")
def find_by_staff_id(staff_id_num):
    employee = db.session.scalars(
    	db.select(employees).filter_by(staff_id=staff_id_num).
    	limit(1)
        ).first()

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


@app.route("/employees/team/<string:dept_name>/<int:reporting_manager_id_num>")
def find_by_team(dept_name, reporting_manager_id_num):
    
    # Check if department exists
    dept_exists = db.session.query(
        db.session.query(employees).filter_by(dept=dept_name).exists()
    ).scalar()

    if not dept_exists:
        return jsonify(
            {
                "code": 404,
                "message": f"Department with name:{dept_name} is not found."
            }
        ), 404

    team_manager = db.session.scalars(
    	db.select(employees).filter_by(staff_id=reporting_manager_id_num).
    	limit(1)
        ).first()
    
    if not team_manager:
        return jsonify(
            {
                "code": 404,
                "message": "Team manager not found."
            }
        ), 404
    
    team_list = db.session.scalars(
    	db.select(employees).filter(
            and_(
                employees.reporting_manager == reporting_manager_id_num,
                employees.dept == dept_name
            )
        )
    ).all()

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

@app.route("/employees/dept/<string:dept_name>")
def find_by_dept(dept_name):
    dept_list = db.session.scalars(
    	db.select(employees).filter_by(dept=dept_name)).all()

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

@app.route("/employees/role/<int:role_num>")
def find_by_role(role_num):
    role_list = db.session.scalars(
    	db.select(employees).filter_by(role=role_num)).all()

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

if __name__ == '__main__':
    app.run(port=5000, debug=True)