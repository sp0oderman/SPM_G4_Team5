from flask import Blueprint, jsonify, request
import datetime 

# Create a blueprint for withdrawal_requests_routes
def create_withdrawal_requests_blueprint(employees_service, wfh_requests_service, withdrawal_requests_service):
    withdrawal_requests_blueprint = Blueprint('withdrawal_requests_blueprint', __name__)

    # Get all wfh_requests from specific team by reporting_manager_id_num
    @withdrawal_requests_blueprint.route("/team/<int:reporting_manager_id_num>/<string:status>", methods=['GET'])
    def get_withdrawal_requests_by_team(reporting_manager_id_num, status):
        team_manager, team_list = employees_service.find_by_team(reporting_manager_id_num)
        team_requests_list = withdrawal_requests_service.find_by_employees(team_list, status)

        if len(team_requests_list) > 0:
            return jsonify(
                {
                    "code": 200,
                    "data": {
                        "team_requests": [withdrawal_request.json() for withdrawal_request in team_requests_list]
                    }
                }
            ), 200
        
        # If no requests found
        return jsonify(
            {
                "code": 404,
                "message": "No requests from this team is not found."
            }
        ), 404
    
    # Staff apply to withdraw an approved request
    @withdrawal_requests_blueprint.route("/apply_withdrawal_request", methods=['POST'])
    def apply_withdrawal_request():
        data = request.json
        staff_id = data.get("staff_id")
        reporting_manager = data.get("reporting_manager")
        wfh_request_id = data.get("wfh_request_id")
        request_datetime = data.get("request_datetime") or datetime.now()
        status = "Pending"
        remarks = data.get("remarks")
        reason_for_status = None

        if not all([staff_id, reporting_manager, wfh_request_id, remarks]):
            return jsonify({"error": "Missing required fields"}), 400

        if not withdrawal_requests_service.can_apply_withdrawal(staff_id, wfh_request_id):
            return jsonify({"error": "You have conflicting dates"}), 400

        response, status_code = wfh_requests_service.apply_wfh(
            staff_id, reporting_manager, dept, chosen_date, arrangement_type, request_datetime, status, remarks, recurring_id
        )
        return jsonify(response), status_code

    # Approve withdrawal request
    @withdrawal_requests_blueprint.route("/approve_withdrawal_request", methods=['PUT'])
    def approve_pending_withdrawal_request():
        data = request.json
        request_id = data.get('request_id')
        reason_for_status = data.get('reason_for_status')

        response, status_code = wfh_requests_service.approve_withdrawal_request(request_id, reason_for_status)
        return jsonify(response), status_code
    
    # Reject withdrawal request
    @withdrawal_requests_blueprint.route("/reject_withdrawal_request", methods=['PUT'])
    def reject_pending_withdrawal_request():
        data = request.json
        request_id = data.get('request_id')
        reason_for_status = data.get('reason_for_status')

        if not request_id or not reason_for_status:
            return jsonify({"error": "Request ID and rejection reason are required"}), 400

        response, status_code = wfh_requests_service.reject_withdrawal_request(request_id, reason_for_status)
        return jsonify(response), status_code
    
    # Get withdrawal requests by staff_id
    @withdrawal_requests_blueprint.route("/staff_id/<int:staff_id_num>/<string:status>", methods=['GET'])
    def get_wfh_requests_by_staff_id(staff_id_num, status):
        staff_requests_list = withdrawal_requests_service.find_by_staff_id(staff_id_num, status)
        if len(staff_requests_list):
            return jsonify(
                {
                    "code": 200,
                    "data": {
                        "staff_id": staff_id_num,
                        "requests": [withdrawal_request.json() for withdrawal_request in staff_requests_list]
                    }
                }
            ), 200
        return jsonify(
            {
                "code": 404,
                "message": "Employee with that ID number is not found."
            }
        ), 404

        
    return withdrawal_requests_blueprint