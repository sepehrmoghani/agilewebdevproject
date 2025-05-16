from datetime import datetime, timezone
from app import db
from app.authentication.models import User
from app import login_manager

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Budget(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    category = db.Column(db.String(64), nullable=False)
    limit = db.Column(db.Float, nullable=False)
    period = db.Column(db.String(20), nullable=False)  # 'weekly' or 'monthly' or 'yearly'
    description = db.Column(db.Text, nullable=True)

    user = db.relationship('User', backref='budgets')

class Goal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    target_amount = db.Column(db.Float, nullable=False)
    current_amount = db.Column(db.Float, nullable=False)
    salary_percentage = db.Column(db.Float, nullable=False)
    start_date = db.Column(db.Date, nullable=False, default=lambda: datetime.now(timezone.utc).date())
    deadline = db.Column(db.Date, nullable=False)
    description = db.Column(db.Text, nullable=True)
    date_completed = db.Column(db.DateTime, nullable=True)
    is_hidden = db.Column(db.Boolean, default=False)

    user = db.relationship('User', backref=db.backref('goals', lazy=True))

    # Method to check if the goal is overdue
    def __repr__(self):
        return f'<Goal {self.title}, Started on {self.date_started}, Deadline: {self.deadline}>'