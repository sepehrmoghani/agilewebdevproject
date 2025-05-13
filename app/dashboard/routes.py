from flask import render_template, Blueprint, jsonify
from app.transactions.models import Transaction
from app import db  # Ensure you have access to the db object
from sqlalchemy import extract, func
from datetime import datetime

dashboard_bp = Blueprint('dashboard', __name__, template_folder='templates')

# Dashboard main page
@dashboard_bp.route('/dashboard', methods=['GET'])
def dashboard():
    return render_template('dashboard/dashboard.html')

# API: Get all transactions for user_id=1
@dashboard_bp.route("api/transactions")
def get_transactions_data():
    transactions = Transaction.query.filter_by(user_id=1).order_by(Transaction.date.desc()).all()
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
