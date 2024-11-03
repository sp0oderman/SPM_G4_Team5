from flask import Blueprint, jsonify, request

# Create a blueprint for withdrawal_requests_routes
def create_withdrawal_requests_blueprint(employees_service, wfh_requests_service, withdrawal_requests_service):
    withdrawal_requests_blueprint = Blueprint('withdrawal_requests_blueprint', __name__)

    # Get all wfh_requests from specific team by reporting_manager_id_num
    @withdrawal_requests_blueprint.route("/team/<int:reporting_manager_id_num>", methods=['GET'])
    def get_withdrawal_requests_by_team(reporting_manager_id_num):
        team_manager, team_list = employees_service.find_by_team(reporting_manager_id_num)
        team_requests_list = withdrawal_requests_service.find_by_employees(team_list)

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
        
    return withdrawal_requests_blueprint