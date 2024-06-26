from src.core.database import db
from datetime import datetime
from enum import Enum
from flask import jsonify

class TypeService(db.Model):
    __tablename__ = "type_services"
    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(50), nullable=False)
    services = db.relationship('Service', back_populates='type_service', lazy=True)
    
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )
    inserted_at = db.Column(
        db.DateTime, default=datetime.utcnow
    )

class Service(db.Model):
    __tablename__ = "services"
    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(50), nullable=False)
    info = db.Column(db.String(200),nullable=False)
    type_service_id = db.Column(db.Integer, db.ForeignKey("type_services.id", ondelete="CASCADE"))
    type_service = db.relationship("TypeService", back_populates="services", lazy=True)
    
    key_words = db.Column(db.String(200), nullable=False)
    is_enabled = db.Column(db.Boolean(), default=True)
    institution_id = db.Column(db.Integer, db.ForeignKey('institutions.id'))
    institution = db.relationship("Institution", back_populates="services")
    service_orders = db.relationship('Service_order', back_populates='service', lazy=True, cascade="all, delete-orphan")
    
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )
    inserted_at = db.Column(
        db.DateTime, default=datetime.utcnow
    )