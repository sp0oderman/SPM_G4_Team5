from flask import Blueprint, request, render_template, redirect, url_for, session

# Create a blueprint for user_accounts_routes
def create_user_accounts_blueprint(user_accounts_service, employees_service):
    user_accounts_blueprint = Blueprint('user_accounts_blueprint', __name__)

    # Log user into WFH system
    @user_accounts_blueprint.route('/login', methods=['GET','POST'])
    def login_to_wfh_system():
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']

            # Call the login function from user_accounts_service
            response, status_code = user_accounts_service.login(username, password)

            if status_code == 200:
                session['user'] = response['user']
                return redirect(url_for('user_accounts_blueprint.display_index_page'))
            elif status_code == 404:
                return render_template('login.html', error=response['message'])
            elif status_code == 401:
                return render_template('login.html', error="Invalid credentials")

        return render_template('login.html')
    
    # Log user out of WFH system
    @user_accounts_blueprint.route('/logout', methods=['GET'])
    def logout_of_wfh_system():
        # Clear session 
        session.clear()

        # Redirect to login page
        return redirect(url_for('user_accounts_blueprint.login_to_wfh_system'))
    
    # Get index page of system (the calendar with wfh_request functionality page)
    @user_accounts_blueprint.route('/index', methods=['GET'])
    def display_index_page():

        # Check if user is in session, else redirect to login page
        if 'user' not in session:
            return redirect(url_for('user_accounts_blueprint.login_to_wfh_system'))

        # Get user data in "user" variable
        user = session['user']

        # Retrieve employee details of "user"
        employee = employees_service.find_by_staff_id(user['staff_id'])

        if employee:
            user['reporting_manager'] = employee.reporting_manager
            user['dept'] = employee.dept
        else:
            user['reporting_manager'] = None
            user['dept'] = None

        session['user'] = user

        return render_template('index.html', user=user)

    
    return user_accounts_blueprint