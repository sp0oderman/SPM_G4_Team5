from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from flask_session import Session
import requests
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

# Microservice URLs
EMPLOYEE_URL = "http://127.0.0.1:5000/employees"
WFH_REQUEST_URL = "http://127.0.0.1:5100/wfh_requests"
STAFF_SCHEDULE_URL = "http://127.0.0.1:5200/staff_schedule"
TEAM_SCHEDULE_URL = "http://127.0.0.1:5300/team_schedule"
AUTH_URL = "http://127.0.0.1:5500/login"


@app.route('/')
def index():
    if 'user' not in session:
        return redirect(url_for('login'))

    user = session['user']

    # Fetch the reporting manager and department
    response = requests.get(f"http://127.0.0.1:5000/employees/reporting_manager/{user['staff_id']}")
    if response.status_code == 200:
        data = response.json()['data']
        user['reporting_manager'] = data['reporting_manager']
        user['dept'] = data['dept']
    else:
        user['reporting_manager'] = None
        user['dept'] = None

    session['user'] = user
    return render_template('index.html', user=user)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        response = requests.post(AUTH_URL, json={'username': username, 'password': password})

        if response.status_code == 200:
            data = response.json()
            if data['success']:
                session['user'] = data['user']
                return redirect(url_for('index'))
            else:
                return render_template('login.html', error=data['message'])
        else:
            return render_template('login.html', error="Invalid credentials")

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

def make_request(url, params=None):
    if 'user' not in session:
        return jsonify({"success": False, "error": "Not authenticated"}), 401

    headers = {
        'X-User-Role': str(session['user']['role']),
        'X-User-ID': str(session['user']['staff_id'])
    }
    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        return jsonify({"success": True, "data": response.json()})
    except requests.RequestException as e:
        return jsonify({"success": False, "error": str(e)})

@app.route('/get_employees')
def get_employees():
    return make_request(EMPLOYEE_URL)

@app.route('/get_departments')
def get_departments():
    url = f"{EMPLOYEE_URL}/departments"  # We'll create this endpoint in the employee microservice
    return make_request(url)

@app.route('/get_wfh_requests')
def get_wfh_requests():
    return make_request(WFH_REQUEST_URL)


@app.route('/get_staff_schedule/<int:staff_id>')
def get_staff_schedule(staff_id):
    return make_request(f"{STAFF_SCHEDULE_URL}/{staff_id}")


@app.route('/get_team_schedule/<int:reporting_manager>')
def get_team_schedule(reporting_manager):
    department = request.args.get('department')
    url = f"{TEAM_SCHEDULE_URL}/{reporting_manager}"
    if department:
        url += f"?department={department}"
    return make_request(url)


if __name__ == '__main__':
    app.run(port=5400, debug=True)