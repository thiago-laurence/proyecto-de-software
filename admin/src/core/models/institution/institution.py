from src.core.database import db
from datetime import datetime


class Institution(db.Model):
    __tablename__ = "institutions"
    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(50), unique=True)
    info = db.Column(db.String(100))
    address = db.Column(db.String(100))
    is_enabled = db.Column(db.Boolean(), default=False)
    web = db.Column(db.String(100))
    phone = db.Column(db.String(50))
    social_networks = db.Column(db.String(100))
    services = db.relationship('Service', back_populates ='institution')
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


        