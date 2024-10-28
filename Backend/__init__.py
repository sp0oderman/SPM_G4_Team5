from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session

# Initialize extensions
db = SQLAlchemy()
session = Session()

def create_app(config_class):
    """Application factory function."""
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(config_class)
    
    # Initialize extensions
    db.init_app(app)
    session.init_app(app)

    from .services.employees_services import Employees_Service
    from .services.wfh_requests_services import WFH_Requests_Service
    from .services.user_accounts_services import User_Accounts_Service

    # Create Service instances
    employees_service = Employees_Service(db)
    wfh_requests_service = WFH_Requests_Service(db)
    user_accounts_service = User_Accounts_Service(db)
        
    # Import blueprints
    from .routes.employees_routes import create_employees_blueprint
    from .routes.wfh_requests_routes import create_wfh_requests_blueprint
    from .routes.user_accounts_routes import create_user_accounts_blueprint
    
    # Register blueprints
    app.register_blueprint(create_employees_blueprint(employees_service), url_prefix='/employees')
    app.register_blueprint(create_wfh_requests_blueprint(wfh_requests_service), url_prefix='/wfh_requests')
    app.register_blueprint(create_user_accounts_blueprint(user_accounts_service, employees_service), url_prefix='/user_accounts')


    return app
