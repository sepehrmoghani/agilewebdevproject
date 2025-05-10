from flask import Blueprint

authentication_bp = Blueprint(
    'authentication', __name__, 
    template_folder='templates', 
    static_folder='static'
)

from app.authentication import routes