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
    category = StringField('Category', validators=[Optional(), Length(max=64)])
    transaction_type = SelectField('Type', choices=[('income', 'Income'), ('expense', 'Expense'), ('transfer', 'Transfer')], validators=[DataRequired()])
    submit = SubmitField('Add Transaction')