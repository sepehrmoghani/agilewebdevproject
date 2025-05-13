import csv
import io
from datetime import datetime, timedelta
from flask import render_template, url_for, flash, redirect, request, jsonify, abort, Blueprint, session
import uuid
from sqlalchemy import func
#from flask_login import login_user, current_user, logout_user, login_required
from werkzeug.utils import secure_filename
from .models import User, Transaction
from app import db
from .forms import TransactionUploadForm, TransactionForm
from app.share.models import ShareSettings

# Create a Blueprint
transactions_bp = Blueprint('transactions', __name__, template_folder='templates')

@transactions_bp.route('/transactions', methods=['GET', 'POST'])
#@login_required
def transactions():
    upload_form = TransactionUploadForm()
    transaction_form = TransactionForm()
    
    if transaction_form.validate_on_submit():
        # Calculate the balance
        #last_transaction = TransactionForm.query.filter_by(user_id=current_user.id).order_by(Transaction.date.desc()).first()
        last_transaction = Transaction.query.filter_by(user_id=1).order_by(Transaction.date.desc()).first()

        if last_transaction:
            if transaction_form.transaction_type.data == 'expense':
                balance = last_transaction.balance - transaction_form.amount.data
            else:
                balance = last_transaction.balance + transaction_form.amount.data
        else:
            if transaction_form.transaction_type.data == 'expense':
                balance = -transaction_form.amount.data
            else:
                balance = transaction_form.amount.data
        
        transaction = Transaction(
            user_id = 1,
            #user_id=current_user.id,
            date=transaction_form.date.data,
            description=transaction_form.description.data,
            amount=transaction_form.amount.data,
            balance=balance,
            category=transaction_form.category.data,
            transaction_type=transaction_form.transaction_type.data
        )
        
        db.session.add(transaction)
        db.session.commit()
        flash('Transaction added successfully!', 'success')
        return redirect(url_for('transactions.transactions'))
    
    #transactions = Transaction.query.filter_by(user_id=current_user.id).order_by(Transaction.date.desc()).all()
    transactions = Transaction.query.filter_by(user_id=1).order_by(Transaction.date.desc()).all()
    return render_template('transactions/transactions.html', title='Transactions', 
                           upload_form=upload_form, 
                           transaction_form=transaction_form,
                           transactions=transactions)

@transactions_bp.route('/upload_transactions', methods=['POST'])
#@login_required
def upload_transactions():
    form = TransactionUploadForm()
    if form.validate_on_submit():
        csv_file = form.csv_file.data
        if csv_file:
            try:
                stream = io.StringIO(csv_file.stream.read().decode("UTF8"), newline=None)
                csv_reader = csv.DictReader(stream)
                
                # Check required columns
                required_columns = ['date', 'description', 'amount']
                first_row = next(csv_reader)
                stream.seek(0)
                csv_reader = csv.DictReader(stream)
                
                missing_columns = [col for col in required_columns if col not in first_row]
                if missing_columns:
                    flash(f'CSV file missing required columns: {", ".join(missing_columns)}', 'danger')
                    return redirect(url_for('transactions.transactions'))
                
                # Process transactions
                count = 0
                for row in csv_reader:
                    try:
                        # Parse date
                        try:
                            date = datetime.strptime(row['date'], '%Y-%m-%d')
                        except ValueError:
                            try:
                                date = datetime.strptime(row['date'], '%m/%d/%Y')
                            except ValueError:
                                date = datetime.strptime(row['date'], '%d/%m/%Y')
                        
                        # Get amount and determine transaction type
                        amount = float(row['amount'])
                        transaction_type = 'income' if amount >= 0 else 'expense'
                        amount = abs(amount)
                        
                        # Get category if exists
                        category = row.get('category', '')
                        
                        # Calculate new balance
                        #last_transaction = Transaction.query.filter_by(user_id=current_user.id).order_by(Transaction.date.desc()).first()
                        last_transaction = Transaction.query.filter_by(user_id=1).order_by(Transaction.date.desc()).first()
                        
                        if last_transaction:
                            if transaction_type == 'expense':
                                balance = last_transaction.balance - amount
                            else:
                                balance = last_transaction.balance + amount
                        else:
                            if transaction_type == 'expense':
                                balance = -amount
                            else:
                                balance = amount
                        
                        # Create transaction record
                        transaction = Transaction(
                            user_id = 1,
                            #user_id=current_user.id,
                            date=date,
                            description=row['description'],
                            amount=amount,
                            balance=balance,
                            category=category,
                            transaction_type=transaction_type
                        )
                        
                        db.session.add(transaction)
                        count += 1
                    except Exception as e:
                        flash(f'Error processing row: {str(e)}', 'danger')
                
                db.session.commit()
                flash(f'Successfully imported {count} transactions!', 'success')
            except Exception as e:
                flash(f'Error processing CSV file: {str(e)}', 'danger')
        else:
            flash('No file selected', 'danger')
    return redirect(url_for('transactions.transactions'))

@transactions_bp.route("/api/transactions")
#@login_required
def get_transactions_data():
    #transactions = Transaction.query.filter_by(user_id=current_user.id).order_by(Transaction.date.desc()).all()
    transactions = Transaction.query.filter_by(user_id=1).order_by(Transaction.date.desc()).all()

@transactions_bp.route('/delete/<int:transaction_id>', methods=['DELETE'])
def delete_transaction(transaction_id):
    transaction = Transaction.query.get_or_404(transaction_id)
    db.session.delete(transaction)
    db.session.commit()
    return jsonify({'success': True})
    


@transactions_bp.route('/share', methods=['GET', 'POST'])
def share_settings():
    if 'user' not in session:
        return redirect(url_for('authentication.login'))
    
    user_id = session['user']['id']
    share_settings = ShareSettings.query.filter_by(user_id=user_id).first()
    
    # Get unique categories
    categories = db.session.query(Transaction.category).distinct().all()
    categories = [cat[0] for cat in categories if cat[0]]  # Remove None/empty categories
    
    if not share_settings:
        share_settings = ShareSettings(
            user_id=user_id,
            share_url=str(uuid.uuid4())[:8],
            is_public=False
        )
        db.session.add(share_settings)
        db.session.commit()
    
    selected_categories = share_settings.selected_categories.split(',') if share_settings.selected_categories else []
    improvements = calculate_improvements(user_id, selected_categories)
    
    if request.method == 'POST':
        selected = request.form.getlist('categories')
        share_settings.selected_categories = ','.join(selected)
        db.session.commit()
        flash('Share settings updated!', 'success')
        return redirect(url_for('transactions.share_settings'))
    
    return render_template('transactions/share.html', 
                         categories=categories,
                         share_settings=share_settings,
                         selected_categories=selected_categories,
                         improvements=improvements)

@transactions_bp.route('/toggle_share', methods=['POST'])
def toggle_share():
    if 'user' not in session:
        return jsonify({'success': False}), 401
    
    data = request.get_json()
    user_id = session['user']['id']
    share_settings = ShareSettings.query.filter_by(user_id=user_id).first()
    
    if share_settings:
        share_settings.is_public = data['is_public']
        db.session.commit()
        return jsonify({'success': True})
    
    return jsonify({'success': False}), 404

@transactions_bp.route('/shared/<share_url>')
def view_shared(share_url):
    share_settings = ShareSettings.query.filter_by(share_url=share_url).first()
    
    if not share_settings:
        abort(404)
        
    if not share_settings.is_public:
        return render_template('transactions/shared_view.html', is_private=True)
    
    user = User.query.get(share_settings.user_id)
    selected_categories = share_settings.selected_categories.split(',') if share_settings.selected_categories else []
    improvements = calculate_improvements(share_settings.user_id, selected_categories)
    
    return render_template('transactions/shared_view.html',
                         is_private=False,
                         username=f"{user.first_name} {user.last_name}",
                         categories=selected_categories,
                         improvements=improvements)

def calculate_improvements(user_id, categories):
    improvements = {}
    now = datetime.now()
    week_ago = now - timedelta(days=7)
    two_weeks_ago = now - timedelta(days=14)
    
    for category in categories:
        # Current week's total
        current_week = db.session.query(func.sum(Transaction.amount)).filter(
            Transaction.user_id == user_id,
            Transaction.category == category,
            Transaction.date > week_ago
        ).scalar() or 0
        
        # Previous week's total
        previous_week = db.session.query(func.sum(Transaction.amount)).filter(
            Transaction.user_id == user_id,
            Transaction.category == category,
            Transaction.date > two_weeks_ago,
            Transaction.date <= week_ago
        ).scalar() or 0
        
        if previous_week > 0:
            improvement = ((current_week - previous_week) / previous_week) * 100
            improvements[category] = round(max(min(improvement, 100), -100))
        else:
            improvements[category] = 0
            
    return improvements

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