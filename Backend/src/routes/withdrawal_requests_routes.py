from flask import Blueprint, jsonify, request

# Create a blueprint for withdrawal_requests_routes
def create_withdrawal_requests_blueprint(employees_service, wfh_requests_service, withdrawal_requests_service):
    withdrawal_requests_blueprint = Blueprint('withdrawal_requests_blueprint', __name__)
        
    return withdrawal_requests_blueprint