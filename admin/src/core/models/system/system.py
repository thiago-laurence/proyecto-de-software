from src.core.database import db
from datetime import datetime


class System(db.Model):
    __tablename__ = "system"
    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(255))
    element_page = db.Column(db.Integer, default=10)
    info = db.Column(db.String(255))
    activate = db.Column(db.Boolean, default=True)
    message = db.Column(db.String(255))
    
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )
    inserted_at = db.Column(
        db.DateTime, default=datetime.utcnow
    )