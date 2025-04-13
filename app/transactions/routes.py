from flask import Blueprint, render_template, redirect, url_for, request, flash, Response
from flask_login import login_required, current_user
from instance.webforms import CSVUploadForm, TransactionsForm, db
from datetime import datetime  # Import datetime for date conversion
import csv

# Create a Blueprint
transactions_bp = Blueprint('transactions', __name__, template_folder='templates')

@transactions_bp.route('/', methods=['GET'])
def view_transactions():
    user_id = 1  # Placeholder for user_id, replace with current_user.id in production
    user_transactions = TransactionsForm.query.filter_by(user_id=user_id).all()
    form = CSVUploadForm()
    return render_template('transactions.html', form=form, transactions=user_transactions)


@transactions_bp.route('/import_data', methods=['GET', 'POST'])
#@login_required
def import_data():
    user_id = 1 # Placeholder for user_id, replace with current_user.id in production
    form = CSVUploadForm()
    #user_transactions = TransactionsForm.query.filter_by(user_id=current_user.id).all()
    user_transactions = TransactionsForm.query.filter_by(user_id=1).all()
    if form.validate_on_submit():
        csv_file = form.csv_file.data
        try:
            # Read CSV file
            stream = csv_file.stream.read().decode("UTF-8")
            csv_reader = csv.DictReader(stream.splitlines())
            for row in csv_reader:
                print(f"Processing row: {row}")  # Debugging: Print each row
                # Convert the date string to a Python date object
                transaction_date = datetime.strptime(row['date'], '%Y-%m-%d').date()
                transaction = TransactionsForm(
                    user_id=user_id,  # Use the placeholder user ID
                    #user_id=current_user.id,
                    date=transaction_date,
                    transaction_detail=row['transaction_detail'],
                    amount=float(row['amount']),
                    balance=float(row['balance'])
                )
                db.session.add(transaction)
            db.session.commit()
            flash('Transactions uploaded successfully!', 'success')
        except Exception as e:
            print(f"Error: {e}")  # Debugging: Print the error
            flash(f'Error processing file: {e}', 'danger')
        return redirect(url_for('transactions.import_data'))
    return render_template('transactions.html', form=form, transactions=user_transactions)

@transactions_bp.route('/export_data', methods=['GET'])
def export_data():
    user_id = 1  # Placeholder for user_id, replace with current_user.id in production
    transactions = TransactionsForm.query.filter_by(user_id=user_id).all()

    # Create a CSV response
    def generate():
        # Write the header row
        yield 'date,transaction_detail,amount,balance\n'
        # Write each transaction row
        for transaction in transactions:
            yield f'{transaction.date},{transaction.transaction_detail},{transaction.amount},{transaction.balance}\n'

    # Return the response as a CSV file
    return Response(
        generate(),
        mimetype='text/csv',
        headers={'Content-Disposition': 'attachment;filename=transactions.csv'}
    )

@transactions_bp.route('/edit', methods=['GET'])
def edit_transactions():
    """Render the edit transactions page."""
    user_id = 1  # Placeholder for user_id, replace with current_user.id in production
    user_transactions = TransactionsForm.query.filter_by(user_id=user_id).all()
    return render_template('edit_transactions.html', transactions=user_transactions)

@transactions_bp.route('/add', methods=['POST'])
def add_transaction():
    """Add a new transaction."""
    user_id = 1  # Placeholder for user_id, replace with current_user.id in production
    date = request.form['date']
    transaction_detail = request.form['transaction_detail']
    amount = float(request.form['amount'])
    balance = float(request.form['balance'])

    transaction = TransactionsForm(
        user_id=user_id,
        date=datetime.strptime(date, '%Y-%m-%d').date(),
        transaction_detail=transaction_detail,
        amount=amount,
        balance=balance
    )
    db.session.add(transaction)
    db.session.commit()
    flash('Transaction added successfully!', 'success')
    return redirect(url_for('transactions.edit_transactions'))

@transactions_bp.route('/delete', methods=['POST'])
def delete_transactions():
    """Delete selected transactions."""
    transaction_ids = request.form.getlist('transaction_ids')
    for transaction_id in transaction_ids:
        transaction = TransactionsForm.query.get(transaction_id)
        if transaction:
            db.session.delete(transaction)
    db.session.commit()
    flash('Selected transactions deleted successfully!', 'success')
    return redirect(url_for('transactions.edit_transactions'))

@transactions_bp.route('/edit/<int:transaction_id>', methods=['GET', 'POST'])
def edit_transaction(transaction_id):
    """Edit a specific transaction."""
    transaction = TransactionsForm.query.get(transaction_id)
    if request.method == 'POST':
        transaction.date = datetime.strptime(request.form['date'], '%Y-%m-%d').date()
        transaction.transaction_detail = request.form['transaction_detail']
        transaction.amount = float(request.form['amount'])
        transaction.balance = float(request.form['balance'])
        db.session.commit()
        flash('Transaction updated successfully!', 'success')
        return redirect(url_for('transactions.edit_transactions'))
    return render_template('edit_transaction.html', transaction=transaction)