from flask import Flask
from forms import db
from flask_migrate import Migrate
from app.routes import configure_routes
from app.transactions import transactions_bp
from app.authentication import authentication_bp

migrate = Migrate()

def create_app():
    app = Flask(__name__, static_url_path='/static/css')

    app.config['SECRET_KEY'] = '2fe112ef6f5d5d9b9e9eb49430249167'
    app.config['UPLOAD_FOLDER'] = 'upload_folder'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(transactions_bp, url_prefix='/transactions')
    app.register_blueprint(authentication_bp, url_prefix='/authentication')

    configure_routes(app)

    return app
