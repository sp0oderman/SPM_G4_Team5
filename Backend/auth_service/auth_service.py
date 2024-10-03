from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

load_dotenv()

postgres_user = os.getenv('POSTGRES_USER')
postgres_password = os.getenv('POSTGRES_PASSWORD')
postgres_host = os.getenv('POSTGRES_HOST')
postgres_db = os.getenv('POSTGRES_DB')

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{postgres_user}:{postgres_password}@{postgres_host}/{postgres_db}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class EmployeeLogin(db.Model):
    __tablename__ = 'employee_login'

    login_id = db.Column(db.Integer, primary_key=True)
    staff_id = db.Column(db.Integer, nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    last_login = db.Column(db.DateTime)
    role = db.Column(db.Integer, nullable=False)

class Employee(db.Model):
    __tablename__ = 'employee'

    staff_id = db.Column(db.Integer, primary_key=True)
    staff_fname = db.Column(db.String(50), nullable=False)
    staff_lname = db.Column(db.String(50), nullable=False)
    dept = db.Column(db.String(50), nullable=False)
    position = db.Column(db.String(50), nullable=False)
    country = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    reporting_manager = db.Column(db.Integer)
    role = db.Column(db.Integer, nullable=False)

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    user = EmployeeLogin.query.filter_by(username=username).first()

    if user and user.password_hash == password:  # Note: In a real app, use proper password hashing
        employee = Employee.query.filter_by(staff_id=user.staff_id).first()

        if employee:
            return jsonify({
                "success": True,
                "user": {
                    "staff_id": employee.staff_id,
                    "staff_fname": employee.staff_fname,
                    "staff_lname": employee.staff_lname,
                    "role": employee.role,
                    "dept": employee.dept,
                    "position": employee.position
                }
            }), 200
        else:
            return jsonify({"success": False, "message": "Employee details not found"}), 404
    else:
        return jsonify({"success": False, "message": "Invalid credentials"}), 401

if __name__ == '__main__':
    app.run(port=5500, debug=True)