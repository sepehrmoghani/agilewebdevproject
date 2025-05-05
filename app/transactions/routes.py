import csv
import io
from datetime import datetime
from flask import render_template, url_for, flash, redirect, request, jsonify, abort, Blueprint
#from flask_login import login_user, current_user, logout_user, login_required
from werkzeug.utils import secure_filename
from .models import User, Transaction
from forms import User, LoginForm, TransactionUploadForm, TransactionForm, db

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
    return render_template('transactions.html', title='Transactions', 
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