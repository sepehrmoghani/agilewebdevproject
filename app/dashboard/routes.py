
from app.authentication.utils import login_required

from flask import render_template, Blueprint, jsonify, session
from app.transactions.models import Transaction
from app import db  # Ensure you have access to the db object
from sqlalchemy import extract, func
from datetime import datetime

dashboard_bp = Blueprint('dashboard', __name__, template_folder='templates')

# Dashboard main page
@dashboard_bp.route('/dashboard', methods=['GET'])
@login_required
def dashboard():
    transactions = Transaction.query.filter_by(user_id=session['user']['id']).all()
    current_balance = sum(t.amount if t.transaction_type == 'income' else -t.amount for t in transactions)
    return render_template('dashboard/dashboard.html', current_balance=current_balance)

# API: Get all transactions for user_id=1
@dashboard_bp.route("api/transactions")
@login_required
def get_transactions_data():
    transactions = Transaction.query.filter_by(user_id=session['user']['id']).order_by(Transaction.date.desc()).all()
    result = [{
        'id': t.id,
        'date': t.date.strftime('%Y-%m-%d'),
        'description': t.description,
        'amount': t.amount,
        'category': t.category,
        'transaction_type': t.transaction_type
    } for t in transactions]
    return jsonify(result)

# Render: Monthly Analytics Page (Chart)
@dashboard_bp.route("/dashboard/analytics/monthly")
def monthly_analytics_page():
    return render_template("dashboard/monthly_analytics.html")

# Render: Category Analytics Page (Chart)
@dashboard_bp.route("/dashboard/analytics/category")
def category_analytics_page():
    return render_template("dashboard/category_analytics.html")
