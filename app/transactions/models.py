from datetime import datetime
from flask_login import UserMixin
from app import db
from app.authentication.models import User

from app import login_manager

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    description = db.Column(db.String(256), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(64), nullable=True)
    transaction_type = db.Column(db.String(32), nullable=True)  # income, expense, transfer
    
    def __repr__(self):
        return f'<Transaction {self.id}: {self.amount} on {self.date}>'