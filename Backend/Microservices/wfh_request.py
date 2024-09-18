from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import psycopg2
from dotenv import load_dotenv
import os
from sqlalchemy import BigInteger, or_

from datetime import datetime

load_dotenv()

postgres_user = os.getenv('POSTGRES_USER')
postgres_password = os.getenv('POSTGRES_PASSWORD')
postgres_host = os.getenv('POSTGRES_HOST')
postgres_db = os.getenv('POSTGRES_DB')

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{postgres_user}:{postgres_password}@{postgres_host}/{postgres_db}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class wfh_requests(db.Model):
    __tablename__ = 'wfh_request'

    request_id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    staff_id = db.Column(db.Integer)
    reporting_manager = db.Column(db.Integer, nullable=False)
    dept = db.Column(db.String(50), nullable=False)
    chosen_date = db.Column(db.String(50), nullable=False)
    arrangement_type = db.Column(db.String(20), nullable=False)
    request_datetime = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(20), nullable=False)
    remarks = db.Column(db.String(500), nullable=True)

    def __init__(self, staff_id, reporting_manager, dept, chosen_date, arrangement_type, request_datetime, status, remarks):
        self.staff_id = staff_id
        self.reporting_manager = reporting_manager
        self.dept = dept
        self.chosen_date = chosen_date
        self.arrangement_type = arrangement_type
        self.request_datetime = request_datetime
        self.status = status
        self.remarks = remarks

    def json(self):
        return {
                "request_id": self.request_id,
                "staff_id": self.staff_id,
                "reporting_manager": self.reporting_manager,
                "dept": self.dept,
                "chosen_date": self.chosen_date,
                "arrangement_type": self.arrangement_type,
                "request_datetime": self.request_datetime,
                "status": self.status,
                "remarks": self.remarks,
            }

@app.route("/")
def homepage():
    return "Welcome to the homepage of the wfh_request microservice (SPM)."

@app.route("/wfh_requests")
def get_all():
    wfh_requests_list = db.session.scalars(db.select(wfh_requests)).all()

    if len(wfh_requests_list):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "wfh_requests": [wfh_request.json() for wfh_request in wfh_requests_list]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no work-from-home requests."
        }
    ), 404


@app.route("/wfh_requests/<int:request_id_num>")
def find_by_request_id(request_id_num):
    wfh_request = db.session.scalars(
    	db.select(wfh_requests).filter_by(request_id=request_id_num)
        ).first()

    if wfh_request:
        return jsonify(
            
            {
                "code": 200,
                "data": wfh_request.json()
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "Work-from-home request with that ID number is not found."
        }
    ), 404

@app.route("/wfh_requests/<int:staff_id_num>")
def find_by_staff_id(staff_id_num):
    staff_requests_list = db.session.scalars(
    	db.select(wfh_requests).filter_by(staff_id=staff_id_num)
        ).all()

    if len(staff_requests_list):
        return jsonify(
            
            {
                "code": 200,
                "data": {
                    "staff_id": staff_id_num,
                    "requests": [wfh_request.json() for wfh_request in staff_requests_list]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "Employee with that ID number is not found."
        }
    ), 404


@app.route("/wfh_requests/team/<int:reporting_manager_id_num>")
def find_by_team(reporting_manager_id_num):

    team_manager = db.session.scalars(
    	db.select(wfh_requests).filter_by(staff_id=reporting_manager_id_num).
    	limit(1)
        ).first()
    
    if not team_manager:
        return jsonify(
            {
                "code": 404,
                "message": "Team manager with that ID number is not found."
            }
        ), 404

    team_requests_list = db.session.scalars(
    	db.select(wfh_requests).filter_by(reporting_manager=reporting_manager_id_num)
        ).all()

    if len(team_requests_list):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "team_manager": team_manager,
                    "team_requests": [wfh_request.json() for wfh_request in team_requests_list]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "No requests from this team."
        }
    ), 404

@app.route("/wfh_requests/apply", methods=['POST'])
def insertWfhApplication():
    # Check if application contains valid JSON
    application_details = None
    if request.is_json:
        application_details = request.get_json()
        result = processApplicationDetails(application_details)
        return result, result["code"]
    else:
        data = request.get_data()
        print("Received invalid application details:")
        print(data)
        return jsonify({"code": 400,
                        # make the data string as we dunno what could be the actual format
                        "data": str(data),
                        "message": "Application details should be in JSON."}), 400  # Bad Request input

def processApplicationDetails(application_details):
    print("Processing work-from-home application details:")
    print(application_details)
    staff_id = application_details["staff_id"]
    reporting_manager = application_details['reporting_manager']
    dept = application_details['dept']
    chosen_date = application_details['chosen_date']
    arrangement_type = application_details['arrangement_type']
    request_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    request_status = "Pending"
    remarks = ""
    print()  # print a new line feed as a separator

    wfh_request = wfh_requests(staff_id, reporting_manager, dept, chosen_date, arrangement_type, request_datetime, request_status, remarks)

    try:
        db.session.add(wfh_request)
        db.session.commit()

    except Exception as e:
        return  {
                "code": 500,
                "data": request.get_json(),
                "message": "An error occurred inserting the work-from-home application record.",
                "error": str(e)
                }
    return  {
            "code": 201,
            "message": "Work-from-home application successfully inserted.",
            "data": wfh_request.json(),
            }

# As of now this deletes ANY wfh_request no matter the status
@app.route("/wfh_requests/withdraw/<int:request_id>", methods=['DELETE'])
def deleteWfhRequest(request_id):    
    try:    
        # Find the work-from-home request by request_id
        wfh_request = wfh_requests.query.get(request_id)

        if not wfh_request:
            return {
                "code": 404,
                "message": f"Work-from-home request with ID number:{request_id} not found."
            }, 404

        # Delete the request from the database
        db.session.delete(wfh_request)
        db.session.commit()

        return {
            "code": 200,
            "message": f"Work-from-home request with ID number:{request_id} successfully deleted."
        }, 200

    except Exception as e:
        db.session.rollback()  # Rollback in case of an error
        return {
            "code": 500,
            "message": "An error occurred while deleting the work-from-home request.",
            "error": str(e)
        }, 500

    return  {
            "code": 201,
            "message": "Work-from-home application successfully inserted.",
            "data": wfh_request.json(),
            }

if __name__ == '__main__':
    app.run(port=5100, debug=True)