from flask import Blueprint, request, jsonify
from src.services.user_accounts_services import login

user_accounts_blueprint = Blueprint('user_accounts_blueprint', __name__)

@user_accounts_blueprint.route('/login', methods=['POST'])
def login_to_wfh_system():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    response, status_code = login(username, password)
    return jsonify(response), status_code