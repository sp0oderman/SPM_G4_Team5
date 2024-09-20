from flask import Flask, request, jsonify
from flask_cors import CORS

import os, sys

import requests
from invokes import invoke_http

import json

app = Flask(__name__)
CORS(app)

wfh_request_URL = "http://127.0.0.1:5100/wfh_requests/apply"

@app.route("/apply_wfh_request", methods=['POST'])
def apply_wfh():
    # Simple check of input format and data of the request are JSON
    if request.is_json:
        try:
            details = request.get_json()
            print("\nReceived a work-from-home application in JSON:", details)

            # do the actual work
            # 1. Send application details from UI {staff_id, reporting_manager, dept, arrangement_type}
            result = processWfhApplication(details)
            print('\n------------------------')
            print('\nresult: ', result)
            return jsonify(result), result["code"]

        except Exception as e:
            # Unexpected error in code
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            ex_str = str(e) + " at " + str(exc_type) + ": " + fname + ": line " + str(exc_tb.tb_lineno)
            print(ex_str)

            return jsonify({
                "code": 500,
                "message": "apply_wfh_request.py internal error: " + ex_str
            }), 500

    # if reached here, not a JSON request.
    return jsonify({
        "code": 400,
        "message": "Invalid JSON input: " + str(request.get_data())
    }), 400

def processWfhApplication(details):

    # 2. Send new wfh_request details to employee MS
    print('\n\n-----Invoking employee microservice-----')
    application_result = invoke_http(
        wfh_request_URL, method="POST", json=details)
    print("apply_wfh_application_result: ", application_result, '\n')

    return {
        "code": 201,
        "data": {
            "apply_wfh_application_result": application_result,
        }

    }

# Execute this program if it is run as a main script (not by 'import')
if __name__ == "__main__":
    print("This is flask for " + os.path.basename(__file__) +
          " for applying work-from-home requests...")
    app.run(host="0.0.0.0", port=5101, debug=True)