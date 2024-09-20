from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os
from datetime import datetime

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Load environment variables
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///wfh_requests.db')  # Fallback to SQLite if env variable not set
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Define WFH Request Model
class WFHRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    requested_dates = db.Column(db.String(255), nullable=False)
    time_of_day = db.Column(db.String(10), nullable=False)  # Options: AM, PM, Full Day
    reason = db.Column(db.String(255), nullable=True)
    status = db.Column(db.String(20), default='Pending')  # Default to pending

    def __repr__(self):
        return f'<WFHRequest {self.username} - {self.requested_dates}>'

# Create the database tables
@app.before_first_request
def create_tables():
    db.create_all()

# Route to apply for WFH arrangement
@app.route('/apply_wfh', methods=['POST'])
def apply_wfh():
    try:
        data = request.json
        username = data.get('username')
        requested_dates = data.get('requested_dates')
        time_of_day = data.get('time_of_day')
        reason = data.get('reason', '')

        # Validate required fields
        if not username or not requested_dates or not time_of_day:
            return jsonify({"error": "Missing required fields"}), 400

        # Check if user has reached the WFH limit (Mock)
        if not can_apply_wfh(username, requested_dates):
            return jsonify({"error": "You have reached your WFH limit or have conflicting dates"}), 400

        # Create WFH request object
        new_request = WFHRequest(username=username, requested_dates=','.join(requested_dates), time_of_day=time_of_day, reason=reason)
        db.session.add(new_request)
        db.session.commit()

        # Return success response within 30 seconds
        return jsonify({"message": "WFH request submitted successfully!"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Helper function to check if user can apply for WFH
def can_apply_wfh(username, requested_dates):
    """
    Mock function to check WFH limits and conflicts.
    """
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

    # Check if user has reached the monthly limit (mock rule: 5 requests per month)
    month_requests = [req for req in user_requests if datetime.strptime(req.requested_dates.split(',')[0], '%Y-%m-%d').month == current_month and datetime.strptime(req.requested_dates.split(',')[0], '%Y-%m-%d').year == current_year]
    if len(month_requests) >= 5:
        return False

    return True

# Health check route
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "OK"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
