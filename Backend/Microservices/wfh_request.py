from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import psycopg2
from dotenv import load_dotenv
import os
from sqlalchemy import BigInteger, or_

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
    staff_id = db.Column(db.Integer, primary_key=True)
    reporting_manager = db.Column(db.Integer, nullable=True)
    dept = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    arrangement_type = db.Column(db.String(20), nullable=False)
    request_datetime = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(20), nullable=False)
    remarks = db.Column(db.String(500), nullable=True)


    def __init__(self, request_id, staff_id, reporting_manager, dept, email, arrangement_type, request_datetime, status, remarks):
        self.request_id - request_id
        self.staff_id = staff_id
        self.reporting_manager = reporting_manager
        self.dept = dept
        self.email = email
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
                "email": self.email,
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

    if len(wfh_requests):
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
            "message": "Employee not found."
        }
    ), 404


@app.route("/requests/team/<int:reporting_manager_id_num>")
def find_by_team(reporting_manager_id_num):

    team_manager = db.session.scalars(
    	db.select(wfh_requests).filter_by(staff_id=reporting_manager_id_num).
    	limit(1)
        ).first()
    
    if not team_manager:
        return jsonify(
            {
                "code": 404,
                "message": "Team manager not found."
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


# @app.route("/requests/create/<string:id_num>/", methods=['POST'])
# def create_user_account(id_num):
#     if (db.session.scalars(
#       db.select(user_accounts).filter_by(bank_acct_id=id_num).
#       limit(1)
#       ).first()
#       ):
#         return jsonify(
#             {
#                 "code": 400,
#                 "data": {
#                     "bank_acct_id": id_num
#                 },
#                 "message": "Account already exists."
#             }
#         ), 400

#     data = request.get_json()
#     account = user_accounts(id_num, **data)

#     try:
#         db.session.add(account)
#         db.session.commit()
#     except:
#         return jsonify(
#             {
#                 "code": 500,
#                 "data": {
#                     "bank_acct_id": id_num
#                 },
#                 "message": "An error occurred creating the account."
#             }
#         ), 500

#     return jsonify(
#         {
#             "code": 201,
#             "data": account.json()
#         }
#     ), 201

if __name__ == '__main__':
    app.run(port=5100, debug=True)