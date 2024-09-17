from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Get PostgreSQL credentials from environment variables
postgres_user = os.getenv('POSTGRES_USER')
postgres_password = os.getenv('POSTGRES_PASSWORD')
postgres_host = os.getenv('POSTGRES_HOST')
postgres_db = os.getenv('POSTGRES_DB')

# Initialize Flask app
app = Flask(__name__)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{postgres_user}:{postgres_password}@{postgres_host}/{postgres_db}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Employee Details Model
class employee_details(db.Model):
    __tablename__ = 'employee'

    staff_id = db.Column(db.Integer, primary_key=True)
    staff_fname = db.Column(db.String(100), nullable=False)
    staff_lname = db.Column(db.String(100), nullable=False)
    dept = db.Column(db.String(100), nullable=False)
    position = db.Column(db.String(100), nullable=False)
    country = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    reporting_manager = db.Column(db.Integer, nullable=True)
    role = db.Column(db.Integer, nullable=False)

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

# Route to get team members based on reporting manager (team schedule)
@app.route("/team_schedule/<int:staff_id_num>")
def get_team_schedule(staff_id_num):
    # Get the employee by their staff ID
    employee = db.session.scalars(
        db.select(employee_details).filter_by(staff_id=staff_id_num).limit(1)
    ).first()

    if not employee:
        return jsonify(
            {
                "code": 404,
                "message": "Employee not found."
            }
        ), 404

    # Get team members who report to the same manager
    team_members = db.session.scalars(
        db.select(employee_details).filter_by(reporting_manager=employee.reporting_manager)
    ).all()

    if not team_members:
        return jsonify(
            {
                "code": 404,
                "message": "No team members found."
            }
        ), 404

    return jsonify(
        {
            "code": 200,
            "data": {
                "team_members": [member.json() for member in team_members]
            }
        }
    )

# Main entry point
if __name__ == '__main__':
    app.run(debug=True)
