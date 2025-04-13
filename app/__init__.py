from flask import Blueprint

transactions_bp = Blueprint('transactions', __name__)
#authentication_bp = Blueprint('authentication', __name__)
#budgeting_and_goals_bp = Blueprint('budgeting_and_goals', __name__)
#dashboard_and_analytics_bp = Blueprint('dashboard_and_analytics', __name__)

from . import routes