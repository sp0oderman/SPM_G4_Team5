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

    from src.services.employees_services import Employees_Service
    from src.services.wfh_requests_services import WFH_Requests_Service

    # Create Service instances
    employees_service = Employees_Service(db)
    wfh_requests_service = WFH_Requests_Service(db)
        
    # Import blueprints
    from src.routes.employees_routes import create_employees_blueprint
    from src.routes.wfh_requests_routes import create_wfh_requests_blueprint
    
    # Register blueprints
    app.register_blueprint(create_employees_blueprint(employees_service, wfh_requests_service), url_prefix='/employees')
    app.register_blueprint(create_wfh_requests_blueprint(employees_service, wfh_requests_service), url_prefix='/wfh_requests')

    return app
