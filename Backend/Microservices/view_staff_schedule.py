from flask import Flask, jsonify
from dotenv import load_dotenv
import os
from wfh_request import db, wfh_requests

load_dotenv()

postgres_user = os.getenv('POSTGRES_USER')
postgres_password = os.getenv('POSTGRES_PASSWORD')
postgres_host = os.getenv('POSTGRES_HOST')
postgres_db = os.getenv('POSTGRES_DB')

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{postgres_user}:{postgres_password}@{postgres_host}/{postgres_db}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.route("/staff_schedule/<int:staff_id>")
def get_staff_schedule(staff_id):
    staff_requests = db.session.query(wfh_requests).filter_by(staff_id=staff_id).all()

    if staff_requests:
        return jsonify(
            {
                "code": 200,
                "data": {
                    "staff_id": staff_id,
                    "schedule": [request.json() for request in staff_requests]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": f"No schedule found for staff ID: {staff_id}"
        }
    ), 404

if __name__ == '__main__':
    app.run(port=5200, debug=True)