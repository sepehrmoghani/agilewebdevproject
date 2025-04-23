from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from instance.config import Config

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__, static_url_path='/static/css')
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # Register blueprints
    from app.authentication import authentication_bp
    app.register_blueprint(authentication_bp, url_prefix='/authentication')

    # Add other blueprints as needed
    # from app.transactions import transactions_bp
    # app.register_blueprint(transactions_bp, url_prefix='/transactions')

    # from app.budgeting_and_goals import budgeting_and_goals_bp
    # app.register_blueprint(budgeting_and_goals_bp, url_prefix='/budgeting_and_goals')

    # from app.dashboard_and_analytics import dashboard_and_analytics_bp
    # app.register_blueprint(dashboard_and_analytics_bp, url_prefix='/dashboard_and_analytics')

    return app