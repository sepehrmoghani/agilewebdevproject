import csv
import io
from datetime import datetime, timedelta
from flask import render_template, url_for, flash, redirect, request, jsonify, abort, Blueprint, session, Response
import uuid
from sqlalchemy import func
from app.authentication.utils import login_required
from werkzeug.utils import secure_filename
from .models import User, Transaction
from app import db
from .forms import TransactionUploadForm, TransactionForm

# Create a Blueprint
transactions_bp = Blueprint('transactions', __name__, template_folder='templates')

def calculate_balance(transactions):
    total = 0
    for transaction in transactions:
        if transaction.transaction_type == 'income':
            total += transaction.amount
        else:
            total -= transaction.amount
    return total

@transactions_bp.route('/transactions', methods=['GET', 'POST'])
@login_required
def transactions():
    upload_form = TransactionUploadForm()
    transaction_form = TransactionForm()

    if transaction_form.validate_on_submit():
        #last_transaction = TransactionForm.query.filter_by(user_id=current_user.id).order_by(Transaction.date.desc()).first()
        #last_transaction = Transaction.query.filter_by(user_id=1).order_by(Transaction.date.desc()).first()

        transaction = Transaction(
            user_id = session['user']['id'],
            #user_id=current_user.id,
            date=transaction_form.date.data,
            description=transaction_form.description.data,
            amount=transaction_form.amount.data,
            category=transaction_form.category.data,
            transaction_type=transaction_form.transaction_type.data
        )

        db.session.add(transaction)
        db.session.commit()
        flash('Transaction added successfully!', 'success')
        return redirect(url_for('transactions.transactions'))

    #transactions = Transaction.query.filter_by(user_id=current_user.id).order_by(Transaction.date.desc()).all()
    transactions = Transaction.query.filter_by(user_id=session['user']['id']).order_by(Transaction.date.desc()).all()
    current_balance = calculate_balance(transactions)
    return render_template('transactions/transactions.html', title='Transactions', 
                           upload_form=upload_form, 
                           transaction_form=transaction_form,
                           transactions=transactions,
                           current_balance=current_balance)

@transactions_bp.route('/upload_transactions', methods=['POST'])
@login_required
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

                        #last_transaction = Transaction.query.filter_by(user_id=current_user.id).order_by(Transaction.date.desc()).first()
                        #last_transaction = Transaction.query.filter_by(user_id=1).order_by(Transaction.date.desc()).first()

                        # Create transaction record
                        transaction = Transaction(
                            user_id = session['user']['id'],
                            #user_id=current_user.id,
                            date=date,
                            description=row['description'],
                            amount=amount,
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
@login_required
def get_transactions_data():
    #transactions = Transaction.query.filter_by(user_id=current_user.id).order_by(Transaction.date.desc()).all()
    transactions = Transaction.query.filter_by(user_id=session['user']['id']).order_by(Transaction.date.desc()).all()

@transactions_bp.route('/delete/<int:transaction_id>', methods=['POST'])
def delete_transaction(transaction_id):
    transaction = Transaction.query.get_or_404(transaction_id)

    # Only allow deletion if the transaction belongs to the current user
    #user_id = 1  # Placeholder for the logged-in user's ID
    user_id = session['user']['id']
    if transaction.user_id != user_id:
        flash("You are not authorized to delete this transaction.", "danger")
        return redirect(url_for('transactions.transactions'))

    db.session.delete(transaction)
    db.session.commit()
    flash("Transaction deleted successfully.", "success")
    return redirect(url_for('transactions.transactions'))

@transactions_bp.route('/export')
def export_transactions():
    transactions = Transaction.query.filter_by(user_id=session['user']['id']).order_by(Transaction.date.desc()).all()

    output = io.StringIO()
    writer = csv.writer(output)

    # Write header
    writer.writerow(['Date', 'Description', 'Amount', 'Category', 'Type'])

    # Write transactions
    for transaction in transactions:
        writer.writerow([
            transaction.date.strftime('%Y-%m-%d'),
            transaction.description,
            transaction.amount,
            transaction.category,
            transaction.transaction_type])

    output.seek(0)
    return Response(
        output.getvalue(),
        mimetype='text/csv',
        headers={'Content-Disposition': 'attachment; filename=transactions.csv'}
    )

@transactions_bp.route('/edit/<int:transaction_id>', methods=['GET', 'POST'])
@login_required
def edit_transaction(transaction_id):
    transaction = Transaction.query.get_or_404(transaction_id)
    form = TransactionForm(obj=transaction)

    if form.validate_on_submit():
        new_amount = form.amount.data

        transaction.date = form.date.data
        transaction.description = form.description.data
        transaction.amount = new_amount
        transaction.category = form.category.data
        transaction.transaction_type = form.transaction_type.data

        later_transactions = Transaction.query.filter(
            Transaction.user_id == transaction.user_id,
            Transaction.date >= transaction.date,
            Transaction.id != transaction.id
        ).order_by(Transaction.date.asc()).all()

        db.session.commit()
        flash('Transaction updated successfully!', 'success')
        return redirect(url_for('transactions.transactions'))

    return render_template('transactions/transactions_edit.html', form=form, transaction=transaction)