from flask import Blueprint, jsonify, request

# Create a blueprint for wfh_requests_routes
def create_wfh_requests_blueprint(employees_service, wfh_requests_service, user_accounts_service):
    wfh_requests_blueprint = Blueprint('wfh_requests_blueprint', __name__)

    # WUHAO'S ROUTES
            
    # Route for Manager to view employees reporting to them
    @wfh_requests_blueprint.route('/get_manager_team/<int:manager_id>', methods=['GET'])
    def get_team_by_reporting_manager(manager_id):
        team_data, status_code = wfh_requests_service.get_manager_team(manager_id)

        if status_code == 200:
            return jsonify(
                {
                    "code": 200,
                    "data": team_data
                }
            ), 200
        
        # If an error occurs, the service returns a dictionary with an error message
        return jsonify(
            {
            "code": 500,
            "message": "An error occurred while retrieving the team data.",
            "error": team_data["error"]
            }
        ), 500

    # Route to apply for WFH arrangement (For Users)
    @wfh_requests_blueprint.route('/apply_wfh', methods=['POST'])
    def apply_for_wfh_request():
        data = request.json
        staff_id = data.get("staff_id")
        reporting_manager = data.get("reporting_manager")
        dept = data.get("dept")
        chosen_date = data.get("chosen_date")
        arrangement_type = data.get("arrangement_type")
        request_datetime = data.get("request_datetime")
        status = data.get("status")
        remarks = data.get("remarks","")


        if not staff_id or not chosen_date or not arrangement_type:
            return jsonify({"error": "Missing required fields"}), 400

        # Check if user has reached the WFH limit or has conflicting dates
        if not wfh_requests_service.can_apply_wfh(staff_id, chosen_date):
            return jsonify({"error": "You have reached your WFH limit or have conflicting dates"}), 400
        
        # Call the service function
        response, status_code = wfh_requests_service.apply_wfh(staff_id, reporting_manager, dept, chosen_date, arrangement_type, request_datetime, status, remarks)

        # Return the response from the service
        return jsonify(response), status_code

    # Route for Manager to view pending WFH requests
    @wfh_requests_blueprint.route('/pending_wfh_requests', methods=['GET'])
    def get_pending_wfh_requests_of_own_team():
        manager_id = request.args.get("manager_id")

        # Validate the manager_id parameter
        if not manager_id:
            return jsonify({"error": "Manager ID is required"}), 400
        
        # Call the service function
        requests_data, status_code = wfh_requests_service.view_pending_wfh_requests(manager_id)

        # Return the response based on the service's return values
        return jsonify(requests_data), status_code
        
    # Route for Manager to approve WFH requests
    @wfh_requests_blueprint.route('/approve_wfh_request', methods=['PUT'])
    def approve_pending_wfh_request():
        data = request.json
        request_id = data.get('request_id')
        manager_id = data.get('manager_id')

        response, status_code = wfh_requests_service.approve_wfh_request(request_id, manager_id)
        return jsonify(response), status_code

    # Route for Manager to reject WFH requests
    @wfh_requests_blueprint.route('/reject_wfh_request', methods=['PUT'])
    def reject_pending_wfh_request():
        data = request.json
        request_id = data.get('request_id')
        rejection_reason = data.get('rejection_reason')

        if not request_id or not rejection_reason:
            return jsonify({"error": "Request ID and rejection reason are required"}), 400
        
        response, status_code = wfh_requests_service.reject_wfh_request(request_id, rejection_reason)
        return jsonify(response), status_code

    # JAKOB'S ROUTES

    # Get all wfh_requests from wfh_requests table
    @wfh_requests_blueprint.route('/<string:status>', methods=['GET'])
    def get_all_wfh_requests(status):
        wfh_requests_list = wfh_requests_service.get_all(status)

        if len(wfh_requests_list):
            return jsonify(
                {
                    "code": 200,
                    "data": {
                        "wfh_requests": [wfh_request.json() for wfh_request in wfh_requests_list]
                    }
                }
            ), 200
        return jsonify(
            {
                "code": 404,
                "message": "There are no work-from-home requests."
            }
        ), 404

    # Get wfh_request with specific request_id_num from wfh_requests table
    @wfh_requests_blueprint.route('/request_id/<int:request_id_num>', methods=['GET'])
    def get_wfh_request_by_request_id(request_id_num):
        wfh_request = wfh_requests_service.find_by_request_id(request_id_num)

        if wfh_request:
            return jsonify(        
                {
                    "code": 200,
                    "data": wfh_request.json()
                }
            ), 200
        return jsonify(
            {
                "code": 404,
                "message": "Work-from-home request with that ID number is not found."
            }
        ), 404

    # Get all wfh_requests of staff by staff_id_num from wfh_requests table
    @wfh_requests_blueprint.route("/staff_id/<int:staff_id_num>", methods=['GET'])
    def get_wfh_requests_by_staff_id(staff_id_num):
        staff_requests_list = wfh_requests_service.find_by_staff_id(staff_id_num)

        if len(staff_requests_list):
            return jsonify(
                {
                    "code": 200,
                    "data": {
                        "staff_id": staff_id_num,
                        "requests": [wfh_request.json() for wfh_request in staff_requests_list]
                    }
                }
            ), 200
        return jsonify(
            {
                "code": 404,
                "message": "Employee with that ID number is not found."
            }
        ), 404

    # Get all wfh_requests from specific team by reporting_manager_id_num from wfh_requests table
    @wfh_requests_blueprint.route("/team/<int:reporting_manager_id_num>", methods=['GET'])
    def get_wfh_requests_by_team(reporting_manager_id_num):
        # Get all subordinates of the reporting_manager recursively (subordinates of manager who reports to this manager also shown)
        subordinates_list = employees_service.get_all_subordinates(reporting_manager_id_num, None)
        team_requests_list = wfh_requests_service.find_by_employees(subordinates_list)

        if len(team_requests_list) > 0:
            return jsonify(
                {
                    "code": 200,
                    "data": {
                        "team_requests": [wfh_request.json() for wfh_request in team_requests_list]
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

    # Delete a wfh_request by request_id_num from wfh_requests table
    @wfh_requests_blueprint.route("/withdraw/request_id/<int:request_id_num>", methods=['DELETE'])
    def withdraw_request_by_id(request_id_num):
        status_code, error_message = wfh_requests_service.delete_wfh_request(request_id_num)

        if status_code == 404:
            return jsonify(
                {
                    "code": 404,
                    "message": f"Work-from-home request with ID number:{request_id_num} not found."
                }
            ), 404
        elif status_code == 200:
            return jsonify(
                {
                    "code": 200,
                    "message": f"Work-from-home request with ID number:{request_id_num} successfully deleted."
                }
            ), 200
        else:
            return jsonify(
                {
                    "code": 500,
                    "message": "An error occurred while deleting the work-from-home request.",
                    "error": str(error_message)
                }
            ), 500
        
    return wfh_requests_blueprint