from flask import render_template, Blueprint, jsonify
from app.transactions.models import Transaction  # Import from transactions.models

# Create the Blueprint for the dashboard
dashboard_bp = Blueprint('dashboard', __name__, template_folder='templates')

# Route to render the dashboard page
@dashboard_bp.route('/')
def dashboard():
    return render_template('dashboard.html')

# API route to fetch transaction data
@dashboard_bp.route("/api/transactions")
def get_transactions_data():
    transactions = Transaction.query.filter_by(user_id=1).order_by(Transaction.date.desc()).all()
    result = []
    for transaction in transactions:
        result.append({
            'id': transaction.id,
            'date': transaction.date.strftime('%Y-%m-%d'),
            'description': transaction.description,
            'amount': transaction.amount,
            'balance': transaction.balance,
            'category': transaction.category,
            'transaction_type': transaction.transaction_type
        })
    return jsonify(result)
