from app import db

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