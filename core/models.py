from core import db

class ShortUrls(db.Model):
    """Model Fields to create url"""
    id = db.Column(db.Integer, primary_key=True)
    original_url = db.Column(db.String(500), nullable=False)
    short_id = db.Column(db.String(20), nullable=False, unique=True)
    time_life = db.Column(db.Integer(), default=90, nullable=False)
    created_at = db.Column(db.Integer(), nullable=False)
    expiration_at = db.Column(db.Integer(), nullable=False)