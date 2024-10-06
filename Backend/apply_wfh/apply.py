from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os
from datetime import datetime

# Initialize Flask app
app = Flask(__name__)

# Enable CORS
CORS(app)

# Database Configuration (change the username and pw to your own)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://username:pw@localhost/employee_management'
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

# Create the database tables
@app.before_first_request
def create_tables():
    db.create_all()

# Route for Manager to view employees reporting to them
@app.route('/get_manager_team/<int:manager_id>', methods=['GET'])
def get_manager_team(manager_id):
    try:
        team = Employee.query.filter_by(Reporting_Manager=manager_id).all()
        team_data = [{
            'Staff_ID': employee.Staff_ID,
            'Staff_FName': employee.Staff_FName,
            'Staff_LName': employee.Staff_LName,
            'Position': employee.Position
        } for employee in team]
        return jsonify(team_data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
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

        # Check if user has reached the WFH limit or has conflicting dates
        if not can_apply_wfh(staff_id, requested_dates):
            return jsonify({"error": "You have reached your WFH limit or have conflicting dates"}), 400

        # Insert the new WFH request
        new_request = WFHRequest(staff_id=staff_id, requested_dates=','.join(requested_dates), time_of_day=time_of_day, reason=reason)
        db.session.add(new_request)
        db.session.commit()

        return jsonify({"message": "WFH request submitted successfully!"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Helper function to check if user can apply for WFH
def can_apply_wfh(staff_id, requested_dates):
    # # Retrieve all WFH requests for the staff in the current month
    # current_month = datetime.now().month
    # user_requests = WFHRequest.query.filter_by(staff_id=staff_id).all()

    # # Check for conflicts in requested dates
    # for req in user_requests:
    #     existing_dates = req.requested_dates.split(',')
    #     for date in requested_dates:
    #         if date in existing_dates:
    #             return False
    return True

# Route for Manager to view pending WFH requests
@app.route('/pending_wfh_requests', methods=['GET'])
def view_pending_wfh_requests():
    manager_id = request.args.get('manager_id')
    if not manager_id:
        return jsonify({"error": "Manager ID is required"}), 400

    # Fetch the manager's team and their pending requests
    team = Employee.query.filter_by(Reporting_Manager=manager_id).all()
    team_ids = [emp.Staff_ID for emp in team]
    pending_requests = WFHRequest.query.filter(WFHRequest.staff_id.in_(team_ids), WFHRequest.status == 'Pending').all()

    requests_data = [
        {
            "id": req.id,
            "staff_id": req.staff_id,
            "requested_dates": req.requested_dates,
            "time_of_day": req.time_of_day,
            "reason": req.reason,
            "status": req.status
        } for req in pending_requests
    ]

    return jsonify(requests_data), 200

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

    # Example business logic: enforce 50% team limit
    wfh_count = WFHRequest.query.filter_by(status='Approved').count()
    if wfh_count / team_size > 0.5:
        return jsonify({"error": "More than 50 percent of the team is already working from home"}), 400

    # Approve the request if within limits
    wfh_request.status = 'Approved'
    db.session.commit()
    
    return jsonify({"message": "WFH request approved successfully!"})
    
# Route for Manager to reject WFH requests
@app.route('/reject_wfh_request', methods=['POST'])
def reject_wfh_request():
    try:
        data = request.json
        request_id = data.get('request_id')
        rejection_reason = data.get('rejection_reason')

        if not request_id or not rejection_reason:
            return jsonify({"error": "Request ID and rejection reason are required"}), 400

        # Retrieve the WFH request by ID
        wfh_request = WFHRequest.query.filter_by(id=request_id, status='Pending').first()
        if not wfh_request:
            return jsonify({"error": "No pending WFH request found"}), 404

        # Reject the WFH request
        wfh_request.status = 'Rejected'
        wfh_request.reason = rejection_reason
        db.session.commit()

        return jsonify({"message": "WFH request rejected successfully!"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Health check route
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "OK"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
