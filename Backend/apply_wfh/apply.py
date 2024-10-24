from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os
from dotenv import load_dotenv
from pathlib import Path  # To construct paths safely across different OS

# Load env variables from .env and assign to variables
load_dotenv()
postgres_user = os.getenv('POSTGRES_USER')
postgres_password = os.getenv('POSTGRES_PASSWORD')
postgres_host = os.getenv('POSTGRES_HOST')
postgres_db = os.getenv('POSTGRES_DB')

# Initialize Flask app
app = Flask(__name__)

# Enable CORS
CORS(app)

# Get the FLASK_ENV environment variable safely
flask_env = os.getenv('FLASK_ENV')

# Check if the app is in testing mode
if flask_env == 'testing':
    # Use SQLite for testing
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
else:
    # Load environment variables for production/development
    postgres_user = os.getenv('POSTGRES_USER')
    postgres_password = os.getenv('POSTGRES_PASSWORD')
    postgres_host = os.getenv('POSTGRES_HOST')
    postgres_db = os.getenv('POSTGRES_DB')

    # Ensure none of the variables are None
    if not all([postgres_user, postgres_password, postgres_host, postgres_db]):
        raise ValueError("One or more environment variables for PostgreSQL are missing")

    # Configure PostgreSQL URI
    app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{postgres_user}:{postgres_password}@{postgres_host}/{postgres_db}"

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Define Employee Model
class Employee(db.Model):
    __tablename__ = 'Employee'
    Staff_ID = db.Column(db.Integer, primary_key=True)
    Staff_FName = db.Column(db.String(50), nullable=False)
    Staff_LName = db.Column(db.String(50), nullable=False)
    Dept = db.Column(db.String(50), nullable=False)
    Position = db.Column(db.String(50), nullable=False)
    Country = db.Column(db.String(50), nullable=False)
    Email = db.Column(db.String(50), nullable=False)
    Reporting_Manager = db.Column(db.Integer, db.ForeignKey('Employee.Staff_ID'))
    Role = db.Column(db.Integer, nullable=False)

class WFHRequest(db.Model):
    __tablename__ = 'WFHRequest'
    id = db.Column(db.Integer, primary_key=True)
    staff_id = db.Column(db.Integer, db.ForeignKey('Employee.Staff_ID'), nullable=False)  # Link to Employee's Staff_ID
    requested_dates = db.Column(db.String(255), nullable=False)
    time_of_day = db.Column(db.String(10), nullable=False)  # Options: AM, PM, Full Day
    reason = db.Column(db.String(255), nullable=True)
    status = db.Column(db.String(20), default='Pending')  # Default to pending

    # Relationship to access employee details from WFH request
    employee = db.relationship('Employee', backref='wfh_requests')

# Helper function to check if 50% of the team is working from home
def is_team_limit_reached(manager_id, date):
    team_size = Employee.query.filter_by(Reporting_Manager=manager_id).count()
    if team_size == 0:
        return False  # If no team members, 50% limit is not reached

    # Count how many team members have approved WFH on the given date
    wfh_count = WFHRequest.query.filter(
        WFHRequest.staff_id.in_(
            Employee.query.with_entities(Employee.Staff_ID).filter_by(Reporting_Manager=manager_id)
        ),
        WFHRequest.requested_dates.like(f'%{date}%'),
        WFHRequest.status == 'Approved'
    ).count()

    # Return True if more than 50% of the team is working from home on that day
    return (wfh_count / team_size) > 0.5

# Route to apply for WFH arrangement (For Users)
@app.route('/apply_wfh', methods=['POST'])
def apply_wfh():
    try:
        data = request.json
        staff_id = data.get('staff_id')
        requested_dates = data.get('requested_dates')
        time_of_day = data.get('time_of_day')
        reason = data.get('reason', '')

        if not staff_id or not requested_dates or not time_of_day:
            return jsonify({"error": "Missing required fields"}), 400

        # Fetch the employee and their manager
        employee = Employee.query.filter_by(Staff_ID=staff_id).first()
        if not employee:
            return jsonify({"error": "Employee not found"}), 404

        # Check if 50% of the team is already working from home on any requested date
        for date in requested_dates:
            if is_team_limit_reached(employee.Reporting_Manager, date):
                return jsonify({"error": f"More than 50% of the team is already working from home on {date}"}), 400

        # Insert the new WFH request
        new_request = WFHRequest(
            staff_id=staff_id,
            requested_dates=','.join(requested_dates),
            time_of_day=time_of_day,
            reason=reason
        )
        db.session.add(new_request)
        db.session.commit()

        return jsonify({"message": "WFH request submitted successfully!"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Route for Manager to approve WFH requests
@app.route('/approve_wfh_request', methods=['POST'])
def approve_wfh_request():
    data = request.json
    request_id = data.get('request_id')
    manager_id = data.get('manager_id')
    
    # Fetch the WFH request by ID
    wfh_request = WFHRequest.query.filter_by(id=request_id, status='Pending').first()
    if not wfh_request:
        return jsonify({"error": "No pending WFH request found"}), 404
    
    # Check the manager's team size
    team_size = Employee.query.filter_by(Reporting_Manager=manager_id).count()

    if team_size == 0:
        return jsonify({"error": "Manager has no team members"}), 400

    # Check if 50% of the team is already working from home on the requested dates
    for date in wfh_request.requested_dates.split(','):
        if is_team_limit_reached(manager_id, date):
            return jsonify({"error": f"More than 50% of the team is already working from home on {date}"}), 400

    # Approve the request if within limits
    wfh_request.status = 'Approved'
    db.session.commit()
    
    return jsonify({"message": "WFH request approved successfully!"}), 200

# Health check route
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "OK"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
