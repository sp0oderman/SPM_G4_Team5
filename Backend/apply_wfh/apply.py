from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os
from datetime import datetime

# Initialize Flask app
app = Flask(__name__)

# Enable CORS
CORS(app)

# Load environment variables
DATABASE_URL = os.getenv('mysql+mysqlconnector://root@localhost:3306/employee', 'sqlite:///wfh_requests.db')  # Fallback to SQLite if env variable not set
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Define WFH Request Model
class WFHRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    requested_dates = db.Column(db.Text, nullable=False)
    time_of_day = db.Column(db.String(10), nullable=False)  # Options: AM, PM, Full Day
    reason = db.Column(db.String(255), nullable=True)
    status = db.Column(db.String(20), default='Pending')  # Default to pending
    team = db.Column(db.String(50), nullable=False)  # Manager's team or department

    def __repr__(self):
        return f'<WFHRequest {self.username} - {self.requested_dates}>'

# Create the database tables
@app.before_first_request
def create_tables():
    db.create_all()

# Route to apply for WFH arrangement (For Users)
@app.route('/apply_wfh', methods=['POST'])
def apply_wfh():
    try:
        data = request.json
        username = data.get('username')
        requested_dates = data.get('requested_dates')
        time_of_day = data.get('time_of_day')
        reason = data.get('reason', '')

        if not username or not requested_dates or not time_of_day:
            return jsonify({"error": "Missing required fields"}), 400

        # Check if user has reached the WFH limit (Mock)
        if not can_apply_wfh(username, requested_dates):
            return jsonify({"error": "You have reached your WFH limit or have conflicting dates"}), 400

        new_request = WFHRequest(username=username, requested_dates=','.join(requested_dates), time_of_day=time_of_day, reason=reason, team='Team A')
        db.session.add(new_request)
        db.session.commit()

        return jsonify({"message": "WFH request submitted successfully!"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Helper function to check if user can apply for WFH
def can_apply_wfh(username, requested_dates):

    # Retrieve all WFH requests for the user in the current month
    current_month = datetime.now().month
    current_year = datetime.now().year
    user_requests = WFHRequest.query.filter_by(username=username).all()

    # Check for conflicts in requested dates
    for req in user_requests:
        existing_dates = req.requested_dates.split(',')
        for date in requested_dates:
            if date in existing_dates:
                return False
    return True

# Route for Manager to view pending WFH requests
@app.route('/pending_wfh_requests', methods=['GET'])
def view_pending_wfh_requests():
    manager_username = request.args.get('manager_username')
    if not manager_username:
        return jsonify({"error": "Manager username is required"}), 400

    team = get_manager_team(manager_username)
    pending_requests = WFHRequest.query.filter_by(team=team, status='Pending').all()

    requests_data = [
        {
            "id": req.id,
            "username": req.username,
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
    try:
        data = request.json
        request_id = data.get('request_id')
        manager_username = data.get('manager_username')

        if not request_id or not manager_username:
            return jsonify({"error": "Request ID and Manager username are required"}), 400

        wfh_request = WFHRequest.query.filter_by(id=request_id, status='Pending').first()
        if not wfh_request:
            return jsonify({"error": "No pending WFH request found"}), 404

        team = get_manager_team(manager_username)
        current_team_wfh = get_team_wfh_count(team, wfh_request.requested_dates)
        total_team_members = get_total_team_members(team)

        if current_team_wfh / total_team_members > 0.5:
            return jsonify({"error": "Cannot approve request: More than 50% of the team is already working from home"}), 400

        wfh_request.status = 'Approved'
        db.session.commit()

        notify_staff_member(wfh_request.username, wfh_request.requested_dates, "Approved")
        return jsonify({"message": "WFH request approved successfully!"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/reject_wfh_request', methods=['POST'])
def reject_wfh_request():
    """
    Manager rejects a WFH request with a reason, ensuring that the rejection reason is non-empty.
    """
    try:
        data = request.json
        request_id = data.get('request_id')
        manager_username = data.get('manager_username')
        rejection_reason = data.get('rejection_reason')

        # Validate that request ID, manager username, and rejection reason are provided
        if not request_id or not manager_username or not rejection_reason:
            return jsonify({"error": "Request ID, Manager username, and rejection reason are required"}), 400

        if len(rejection_reason.strip()) == 0:
            return jsonify({"error": "Rejection reason cannot be empty"}), 400

        # Retrieve the WFH request by ID
        wfh_request = WFHRequest.query.filter_by(id=request_id, status='Pending').first()
        if not wfh_request:
            return jsonify({"error": "No pending WFH request found"}), 404

        # Reject the WFH request and store the rejection reason
        wfh_request.status = 'Rejected'
        wfh_request.reason = rejection_reason
        db.session.commit()

        # Notify the staff member (mock function)
        notify_staff_member(wfh_request.username, wfh_request.requested_dates, "Rejected", rejection_reason)

        return jsonify({"message": "WFH request rejected successfully!"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Helper functions (mock implementations)

def get_manager_team(manager_username):
    return "Team A"

def get_team_wfh_count(team, requested_dates):
    return 3

def get_total_team_members(team):
    return 10

def notify_staff_member(username, requested_dates, status, reason=""):
     print(f"Notified {username} that their WFH request for {requested_dates} was {status}. Reason: {reason}")

# Health check route
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "OK"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
