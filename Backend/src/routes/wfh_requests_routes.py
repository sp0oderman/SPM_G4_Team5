from flask import Blueprint, jsonify, request
from datetime import timedelta ,datetime

# Create a blueprint for wfh_requests_routes
def create_wfh_requests_blueprint(employees_service, wfh_requests_service, withdrawal_requests_service):
    wfh_requests_blueprint = Blueprint('wfh_requests_blueprint', __name__)

    # Get specific team strength by date
    @wfh_requests_blueprint.route("/team/strength/<int:reporting_manager_id_num>/<string:date>", methods=['GET'])
    def get_strength_by_team_and_date(reporting_manager_id_num, date):
        team_strength_dict = wfh_requests_service.get_team_strength_by_date(reporting_manager_id_num, date)

        if len(team_strength_dict) > 0:
            return jsonify(
                {
                    "code": 200,
                    "data": {
                        "date": date,
                        "AM": team_strength_dict["AM"],
                        "PM": team_strength_dict["PM"]
                    }
                }
            ), 200
        
        # If no requests found
        return jsonify(
            {
                "code": 404,
                "message": "No requests from this team for this date is not found."
            }
        ), 404

    # Get all wfh_requests from specific team by reporting_manager_id_num
    @wfh_requests_blueprint.route("/team/<int:reporting_manager_id_num>/<string:status>", methods=['GET'])
    def get_wfh_requests_by_team(reporting_manager_id_num, status):
        team_manager, team_list = employees_service.find_by_team(reporting_manager_id_num)
        team_requests_list = wfh_requests_service.find_by_employees(team_list, status)

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

    # Get all wfh_requests of staff by staff_id_num from wfh_requests table
    @wfh_requests_blueprint.route("/staff_id/<int:staff_id_num>/<string:status>", methods=['GET'])
    def get_wfh_requests_by_staff_id(staff_id_num, status):
        staff_requests_list = wfh_requests_service.find_by_staff_id(staff_id_num, status)

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

    @wfh_requests_blueprint.route('/apply_wfh_request', methods=['POST'])
    def apply_for_wfh_request():
        data = request.json
        staff_id = data.get("staff_id")
        reporting_manager = data.get("reporting_manager")
        dept = data.get("dept")
        chosen_date = data.get("chosen_date")
        arrangement_type = data.get("arrangement_type")
        request_datetime = data.get("request_datetime") or datetime.now()
        status = "Pending"
        remarks = data.get("remarks")
        recurring_id = data.get("recurring_id")
        reason_for_status = None

        if not all([staff_id, reporting_manager, dept, chosen_date, arrangement_type, remarks]):
            return jsonify({"error": "Missing required fields"}), 400

        # Handle recurring requests
        if recurring_id != -1:
            max_recurring_id = wfh_requests_service.get_max_recurring_id() or 0
            recurring_id = max_recurring_id + 1

            # Convert dates to date objects
            chosen_date = datetime.strptime(data.get("chosen_date"), "%Y-%m-%d")
            end_date = datetime.strptime(data.get("end_date"), "%Y-%m-%d")

            # List to hold dates for recurring requests
            recurring_dates = []
            temp_date = chosen_date

            # Build list of dates for recurring requests
            while temp_date <= end_date:
                recurring_dates.append(temp_date)
                temp_date += timedelta(days=7)

            # Check all dates for conflicts before creating any requests
            for date in recurring_dates:
                if not wfh_requests_service.can_apply_wfh(staff_id, date, arrangement_type):
                    # Conflict found, return an error
                    return jsonify({
                        "error": f"Conflict detected for date {date.strftime('%Y-%m-%d')}. Recurring request cannot be processed."
                    }), 400

            # If no conflicts, proceed to create requests
            returnDict = {"responses": [], "status_codes": []}
            for date in recurring_dates:
                response, status_code = wfh_requests_service.apply_wfh(
                    staff_id, reporting_manager, dept, date, arrangement_type, request_datetime, status, remarks, recurring_id
                )
                returnDict["responses"].append(response)
                returnDict["status_codes"].append(status_code)

            return jsonify(returnDict), 201

        # Handle single WFH request (non-recurring)
        else:
            # Check for conflicts for a single date
            if not wfh_requests_service.can_apply_wfh(staff_id, chosen_date, arrangement_type):
                return jsonify({"error": "You have conflicting dates"}), 400

            response, status_code = wfh_requests_service.apply_wfh(
                staff_id, reporting_manager, dept, chosen_date, arrangement_type, request_datetime, status, remarks, recurring_id
            )
            return jsonify(response), status_code
        
    # Route for Manager to approve WFH requests
    @wfh_requests_blueprint.route('/approve_wfh_request', methods=['PUT'])
    def approve_pending_wfh_request():
        data = request.json
        request_id = data.get('request_id')
        manager_id = data.get('reporting_manager')
        reason_for_status = data.get('reason_for_status')

        recurring_id = data.get('recurring_id')
        if recurring_id == -1:
            response, status_code = wfh_requests_service.approve_wfh_request(request_id, manager_id, reason_for_status)
            return jsonify(response), status_code
        
        response, status_code = wfh_requests_service.approve_recurring_wfh_requests(recurring_id, reason_for_status)
        return jsonify(response), status_code

    # Route for Manager to reject WFH requests
    @wfh_requests_blueprint.route('/reject_wfh_request', methods=['PUT'])
    def reject_pending_wfh_request():
        data = request.json
        request_id = data.get('request_id')
        rejection_reason = data.get('reason_for_status')

        if not request_id or not rejection_reason:
            return jsonify({"error": "Request ID and rejection reason are required"}), 400
        
        recurring_id = data.get('recurring_id')
        if recurring_id == -1:
            response, status_code = wfh_requests_service.reject_wfh_request(request_id, rejection_reason)
            return jsonify(response), status_code
        
        response, status_code = wfh_requests_service.reject_recurring_wfh_requests(recurring_id, rejection_reason)
        return jsonify(response), status_code

    # Withdraw a wfh_request by request_id_num from wfh_requests table
    @wfh_requests_blueprint.route("/withdraw_wfh_request", methods=['PUT'])
    def withdraw_wfh_request():
        data = request.json
        request_id = data.get('request_id')
        withdrawal_reason = data.get('reason_for_status')

        if not request_id or not withdrawal_reason:
            return jsonify({"error": "Request ID and withdrawal reason are required"}), 400

        response, status_code = wfh_requests_service.withdraw_wfh_request(request_id, withdrawal_reason)
        return jsonify(response), status_code

#####################################################################################################################
#                                                                                                                   #
#                                                UNUSED ROUTES                                                      #
#                                                                                                                   #
#####################################################################################################################

    # Get all wfh_requests from wfh_requests table
    @wfh_requests_blueprint.route('/<string:status>', methods=['GET'])
    def get_wfh_requests_by_status(status):
        wfh_requests_list = wfh_requests_service.get_by_status(status)

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


    # # Route for Manager to view pending WFH requests
    # @wfh_requests_blueprint.route('/pending_wfh_requests', methods=['GET'])
    # def get_pending_wfh_requests_of_own_team():
    #     manager_id = request.args.get("manager_id")

    #     # Validate the manager_id parameter
    #     if not manager_id:
    #         return jsonify({"error": "Manager ID is required"}), 400
        
    #     # Call the service function
    #     requests_data, status_code = wfh_requests_service.view_pending_wfh_requests(manager_id)

    #     # Return the response based on the service's return values
    #     return jsonify(requests_data), status_code
        
    # # DEPRECATED - Route for Manager to view employees reporting to them 
    # @wfh_requests_blueprint.route('/get_manager_team/<int:manager_id>', methods=['GET'])
    # def get_team_by_reporting_manager(manager_id):
    #     team_data, status_code = wfh_requests_service.get_manager_team(manager_id)

    #     if status_code == 200:
    #         return jsonify(
    #             {
    #                 "code": 200,
    #                 "data": team_data
    #             }
    #         ), 200
        
    #     # If an error occurs, the service returns a dictionary with an error message
    #     return jsonify(
    #         {
    #         "code": 500,
    #         "message": "An error occurred while retrieving the team data.",
    #         "error": team_data["error"]
    #         }
    #     ), 500

    # # DEPRECATED - Get all wfh_requests from specific team by reporting_manager_id_num from wfh_requests table
    # @wfh_requests_blueprint.route("/team2/<int:reporting_manager_id_num>", methods=['GET'])
    # def get_wfh_requests_by_team2(reporting_manager_id_num):
    #     # Get all subordinates of the reporting_manager recursively (subordinates of manager who reports to this manager also shown)
    #     subordinates_list = employees_service.get_all_subordinates(reporting_manager_id_num, None)
    #     team_requests_list = wfh_requests_service.find_by_employees(subordinates_list)

    #     if len(team_requests_list) > 0:
    #         return jsonify(
    #             {
    #                 "code": 200,
    #                 "data": {
    #                     "team_requests": [wfh_request.json() for wfh_request in team_requests_list]
    #                 }
    #             }
    #         ), 200
        
    #     # If no requests found
    #     return jsonify(
    #         {
    #             "code": 404,
    #             "message": "No requests from this team is not found."
    #         }
    #     ), 404

    # # DEPERCATED - Route to apply for WFH arrangement (For Users)
    # @wfh_requests_blueprint.route('/apply_wfh', methods=['POST'])
    # def apply_for_wfh_request():
    #     data = request.json
    #     staff_id = data.get("staff_id")
    #     reporting_manager = data.get("reporting_manager")
    #     dept = data.get("dept")
    #     chosen_date = data.get("chosen_date")
    #     arrangement_type = data.get("arrangement_type")
    #     request_datetime = data.get("request_datetime")
    #     status = data.get("status")
    #     remarks = data.get("remarks","")


    #     if not staff_id or not chosen_date or not arrangement_type:
    #         return jsonify({"error": "Missing required fields"}), 400

    #     # Check if user has reached the WFH limit or has conflicting dates
    #     if not wfh_requests_service.can_apply_wfh(staff_id, chosen_date):
    #         return jsonify({"error": "You have reached your WFH limit or have conflicting dates"}), 400
        
    #     # Call the service function
    #     response, status_code = wfh_requests_service.apply_wfh(staff_id, reporting_manager, dept, chosen_date, arrangement_type, request_datetime, status, remarks)

    #     # Return the response from the service
    #     return jsonify(response), status_code

    return wfh_requests_blueprint