from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, DateField, FloatField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError

db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(128), nullable=False)

    date_of_birth = db.Column(db.Date, nullable=True)
    phone = db.Column(db.String(50), nullable=True)
    address = db.Column(db.String(50), nullable=True)
    city = db.Column(db.String(50), nullable=True)
    state = db.Column(db.String(50), nullable=True)
    country = db.Column(db.String(50), nullable=True)
    postcode = db.Column(db.String(50), nullable=True)

    def get_id(self):
        return str(self.id)
    

class TransactionsForm(FlaskForm):
    date = DateField(validators=[InputRequired()], format='%Y-%m-%d', render_kw={"placeholder": "Date"})
    transaction_detail = StringField(validators=[InputRequired(), Length(min=4, max=50)], render_kw={"placeholder": "Transaction Detail"})
    amount = FloatField(validators=[InputRequired()], render_kw={"placeholder": "Amount"})
    balance = FloatField(validators=[InputRequired()], render_kw={"placeholder": "Balance"})
    # submit = SubmitField("Send")
    
    
class Budget(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(50), nullable=False)
    limit = db.Column(db.Float, nullable=False)
    period = db.Column(db.String(20), nullable=False)  # 'weekly' or 'monthly'
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    user = db.relationship('User', backref='budgets')

class Goal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    target_amount = db.Column(db.Float, nullable=False)
    current_amount = db.Column(db.Float, nullable=False)
    deadline = db.Column(db.Date, nullable=False)

    user = db.relationship('User', backref=db.backref('goals', lazy=True))
