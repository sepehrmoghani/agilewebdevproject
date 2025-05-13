
from app import db

class ShareSettings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    is_public = db.Column(db.Boolean, default=False)
    selected_categories = db.Column(db.String(500), nullable=True)
    share_url = db.Column(db.String(100), unique=True, nullable=False)
    
    def __repr__(self):
        return f'<ShareSettings {self.id}: {self.share_url}>'
