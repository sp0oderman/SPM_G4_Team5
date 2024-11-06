from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from apscheduler.schedulers.background import BackgroundScheduler

# Initialize extensions
db = SQLAlchemy()
session = Session()

# For scehduled functions


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
    from src.services.withdrawal_requests_services import Withdrawal_Requests_Service

    # Create Service instances
    employees_service = Employees_Service(db)
    wfh_requests_service = WFH_Requests_Service(db)
    withdrawal_requests_service = Withdrawal_Requests_Service(db)
        
    # Import blueprints
    from src.routes.employees_routes import create_employees_blueprint
    from src.routes.wfh_requests_routes import create_wfh_requests_blueprint
    from src.routes.withdrawal_requests_routes import create_withdrawal_requests_blueprint

    
    # Register blueprints
    app.register_blueprint(create_employees_blueprint(employees_service, wfh_requests_service, withdrawal_requests_service), url_prefix='/employees')
    app.register_blueprint(create_wfh_requests_blueprint(employees_service, wfh_requests_service, withdrawal_requests_service), url_prefix='/wfh_requests')
    app.register_blueprint(create_withdrawal_requests_blueprint(employees_service, wfh_requests_service, withdrawal_requests_service), url_prefix='/withdrawal_requests')

    # Initialize APScheduler
    scheduler = BackgroundScheduler()
    
    # Define the task to run daily
    def reject_old_pending_wfh_requests():
        with app.app_context():
            wfh_requests_service.reject_old_pending_wfh_requests()

    # Define the Withdrawal requests task to run daily at midnight
    def reject_old_pending_withdrawal_requests():
        with app.app_context():
            withdrawal_requests_service.reject_old_pending_withdrawal_requests()

    # Schedule the tasks to run every day at a specific time, e.g., midnight
    scheduler.add_job(reject_old_pending_wfh_requests, 'cron', hour=0, minute=0)
    scheduler.add_job(reject_old_pending_withdrawal_requests, 'cron', hour=0, minute=0)

    # Start the scheduler
    scheduler.start()

    # Ensure scheduler shuts down with the app
    app.scheduler = scheduler

    return app
