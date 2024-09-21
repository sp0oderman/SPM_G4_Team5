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

@app.route("/team_schedule/<int:reporting_manager>")
def get_team_schedule(reporting_manager):
    team_requests = db.session.query(wfh_requests).filter_by(reporting_manager=reporting_manager).all()

    if team_requests:
        return jsonify(
            {
                "code": 200,
                "data": {
                    "reporting_manager": reporting_manager,
                    "team_schedule": [request.json() for request in team_requests]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": f"No schedule found for team under reporting manager: {reporting_manager}"
        }
    ), 404

if __name__ == '__main__':
    app.run(port=5300, debug=True)