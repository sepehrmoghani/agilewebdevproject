from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, DateField, FloatField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError


    

class TransactionsForm(FlaskForm):
    date = DateField(validators=[InputRequired()], format='%Y-%m-%d', render_kw={"placeholder": "Date"})
    transaction_detail = StringField(validators=[InputRequired(), Length(min=4, max=50)], render_kw={"placeholder": "Transaction Detail"})
    amount = FloatField(validators=[InputRequired()], render_kw={"placeholder": "Amount"})
    balance = FloatField(validators=[InputRequired()], render_kw={"placeholder": "Balance"})
    # submit = SubmitField("Send")