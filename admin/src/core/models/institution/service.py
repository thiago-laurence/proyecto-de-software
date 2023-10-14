from src.core.database import db
from datetime import datetime
from enum import Enum
from flask import jsonify

class Tipo(Enum):
    Analisis = 1
    Consultoria = 2
    Desarrollo = 3

class Service(db.Model):
    __tablename__ = "services"
    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(50), nullable=False)
    info = db.Column(db.String(200),nullable=False)
    type = db.Column(db.String(50), nullable=False)
    key_words = db.Column(db.String(200), nullable=False)
    is_enabled = db.Column(db.Boolean(), default=True)
    institution_id = db.Column(db.Integer, db.ForeignKey('institutions.id'))
    institution = db.relationship("Institution", back_populates="services")
    
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )
    inserted_at = db.Column(
        db.DateTime, default=datetime.utcnow
    )
    
    def to_json(self):
        service_dict = {
            'name': self.name,
            'description': self.info,
            'laboratory': self.institution.name,
            'keywords': self.key_words,
            'enabled': self.is_enabled
        }
        return service_dict