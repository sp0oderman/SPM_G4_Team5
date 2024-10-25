from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session

import os
from dotenv import load_dotenv
load_dotenv()

# Initialize extensions
db = SQLAlchemy()
session = Session()

def create_app(config_class):
    """Application factory function."""
    app = Flask(__name__, template_folder="src/templates")
    
    # Load configuration
    app.config.from_object(config_class)
    
    #---------------------------------------------
    # Retrieve the database URL from the environment
    database_url = os.getenv("DATABASE_URL")
    print("DATABASE_URL:", database_url)  # Print the database URL

    if not database_url:
        print("Error: No DATABASE_URL environment variable set")
        raise ValueError("No DATABASE_URL environment variable set")
    #---------------------------------------------

    # Initialize extensions
    db.init_app(app)
    print("Database initialized")  # Confirm database initialization
    session.init_app(app)

    from src.services.employees_services import Employees_Service
    from src.services.wfh_requests_services import WFH_Requests_Service
    from src.services.user_accounts_services import User_Accounts_Service

    # Create Service instances
    employees_service = Employees_Service(db)
    wfh_requests_service = WFH_Requests_Service(db)
    user_accounts_service = User_Accounts_Service(db)
        
    # Import blueprints
    from src.routes.employees_routes import create_employees_blueprint
    from src.routes.wfh_requests_routes import create_wfh_requests_blueprint
    from src.routes.user_accounts_routes import create_user_accounts_blueprint
    
    # Register blueprints
    app.register_blueprint(create_employees_blueprint(employees_service), url_prefix='/employees')
    app.register_blueprint(create_wfh_requests_blueprint(wfh_requests_service), url_prefix='/wfh_requests')
    app.register_blueprint(create_user_accounts_blueprint(user_accounts_service, employees_service), url_prefix='/user_accounts')


    return app
