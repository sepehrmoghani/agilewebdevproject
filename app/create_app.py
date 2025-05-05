from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.routes import configure_routes
from .transactions import transactions_bp
from .authentication import authentication_bp
from .budgeting_and_goals import budgeting_and_goals_bp
#from .dashboard_and_analytics import dashboard_and_analytics_bp

db = SQLAlchemy()

def create_app():
    app = Flask(__name__, static_url_path='/static/css')
    
    # Configuration settings
    app.config['SECRET_KEY'] = '2fe112ef6f5d5d9b9e9eb49430249167'
    app.config['UPLOAD_FOLDER'] = 'upload_folder'

    # Configure database URI
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    # Register blueprints
    app.register_blueprint(transactions_bp, url_prefix='/transactions')
    app.register_blueprint(authentication_bp, url_prefix='/authentication')
    app.register_blueprint(budgeting_and_goals_bp, url_prefix='/budgeting_and_goals')
    #app.register_blueprint(dashboard_and_analytics_bp, url_prefix='/dashboard_and_analytics')

    # Configure routes
    configure_routes(app)

    # Create database and tables
    with app.app_context():
        db.create_all()

    # Add more configuration and initialization as needed

    return app