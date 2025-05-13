
from flask import Blueprint

share_bp = Blueprint('share', __name__, template_folder='templates')

from . import routes
