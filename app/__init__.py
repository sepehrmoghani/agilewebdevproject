from flask import Flask
from flask_migrate import Migrate
from app.routes import configure_routes
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager

db = SQLAlchemy()
csrf = CSRFProtect()
login_manager = LoginManager()
login_manager.login_view = 'authentication.login'

migrate = Migrate()

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = '2fe112ef6f5d5d9b9e9eb49430249167'
    app.config['UPLOAD_FOLDER'] = 'upload_folder'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)
    login_manager.init_app(app)

    from app.transactions import transactions_bp
    from app.authentication import authentication_bp
    from app.budgeting_and_goals import budgeting_and_goals_bp
    from app.dashboard import dashboard_bp
    from app.share import share_bp

    app.register_blueprint(transactions_bp, url_prefix='/transactions')
    app.register_blueprint(authentication_bp, url_prefix='/authentication')
    app.register_blueprint(budgeting_and_goals_bp, url_prefix='/budgeting_and_goals')
    app.register_blueprint(dashboard_bp, url_prefix='/dashboard')
    app.register_blueprint(share_bp, url_prefix='/share')

    configure_routes(app)

    return app