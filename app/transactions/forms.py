from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import StringField,SubmitField, FloatField, SelectField, DateField, FileField
from wtforms.validators import DataRequired,Length,Optional
from datetime import datetime

class TransactionUploadForm(FlaskForm):
    csv_file = FileField('Upload CSV File', validators=[DataRequired()])
    submit = SubmitField('Upload')

class TransactionForm(FlaskForm):
    date = DateField('Date', validators=[DataRequired()], default=datetime.utcnow)
    description = StringField('Description', validators=[DataRequired(), Length(max=256)])
    amount = FloatField('Amount', validators=[DataRequired()])
    category = SelectField('Category', choices=[
        ('Business', 'Business'),
        ('Cash', 'Cash'),
        ('Childcare', 'Childcare'),
        ('Eating out & takeaway', 'Eating out & takeaway'),
        ('Education', 'Education'),
        ('Entertainment', 'Entertainment'),
        ('Fees & interest', 'Fees & interest'),
        ('Gifts & donations', 'Gifts & donations'),
        ('Groceries', 'Groceries'),
        ('Health & medical', 'Health & medical'),
        ('Home', 'Home'),
        ('Home loan', 'Home loan'),
        ('Insurance', 'Insurance'),
        ('Other investments', 'Other investments'),
        ('Personal care', 'Personal care'),
        ('Pets', 'Pets'),
        ('Professional services', 'Professional services'),
        ('Shares', 'Shares'),
        ('Shopping', 'Shopping'),
        ('Sport & fitness', 'Sport & fitness'),
        ('Super contribution', 'Super contribution'),
        ('Tax paid', 'Tax paid'),
        ('Transfer & payments', 'Transfer & payments'),
        ('Travel & holidays', 'Travel & holidays'),
        ('Uncategorised', 'Uncategorised'),
        ('Utilities', 'Utilities'),
        ('Vehicle & transport', 'Vehicle & transport')
    ], validators=[DataRequired()])
    transaction_type = SelectField('Type', choices=[('income', 'Income'), ('expense', 'Expense'), ('transfer', 'Transfer')], validators=[DataRequired()])
    submit = SubmitField('Add Transaction')