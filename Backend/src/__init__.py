from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Initialize extensions
db = SQLAlchemy()

def create_app(config_class):
    """Application factory function."""
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(config_class)
    
    # Initialize extensions
    db.init_app(app)
    
    # Register blueprints
    from .routes.employees_routes import employees_blueprint
    from .routes.wfh_requests_routes import wfh_requests_blueprint
    
    app.register_blueprint(employees_blueprint, url_prefix='/employees')
    app.register_blueprint(wfh_requests_blueprint, url_prefix='/wfh_requests')

    
    return app
