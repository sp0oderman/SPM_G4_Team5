from flask import Flask, jsonify, request
from dotenv import load_dotenv
import os
from wfh_request import db, wfh_requests
from functools import wraps

load_dotenv()

postgres_user = os.getenv('POSTGRES_USER')
postgres_password = os.getenv('POSTGRES_PASSWORD')
postgres_host = os.getenv('POSTGRES_HOST')
postgres_db = os.getenv('POSTGRES_DB')

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{postgres_user}:{postgres_password}@{postgres_host}/{postgres_db}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

def access_control(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user_role = request.headers.get('X-User-Role')
        user_id = request.headers.get('X-User-ID')
        requested_staff_id = kwargs.get('staff_id')

        if not user_role or not user_id:
            return jsonify({"code": 401, "message": "Unauthorized: Missing user information"}), 401

        user_role = int(user_role)
        user_id = int(user_id)

        if user_role != 1 and user_id != requested_staff_id:
            return jsonify({"code": 403, "message": "Forbidden: You can only view your own schedule"}), 403

        return f(*args, **kwargs)
    return decorated_function

@app.route("/staff_schedule/<int:staff_id>")
@access_control
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