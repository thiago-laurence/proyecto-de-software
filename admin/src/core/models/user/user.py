from sqlalchemy.orm import validates
from core.models.validation import validation_string, validation_identifier
from src.core.database import db
from datetime import datetime


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, unique=True)
    email = db.Column(db.String(50), unique=True)
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(255))
    name = db.Column(db.String(50))
    lastname = db.Column(db.String(50))
    active = db.Column(db.Boolean, default=True)
    confirmed = db.Column(db.Boolean, default=False)
    institutions = db.relationship("UserInstitution", back_populates="user", lazy=True)
    comments = db.relationship('Comment', back_populates='user', lazy=True)
    service_orders = db.relationship('Service_order', back_populates='user', lazy=True)
    
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )
    inserted_at = db.Column(
        db.DateTime, default=datetime.utcnow
    )

    @validates("id")
    def validate_id(self, key, value):
        if User.query.filter_by(id=value).first():
            raise ValueError("El ID ya existe")
        return value
    
    @validates("email")
    def validate_email(self, key, value):
        validation_string(key, value)
        if "@" not in value:
            raise ValueError("El email ingresado no es válido (no contiene @)")
        
        user = User.query.filter_by(email=value).first()
        validation_identifier(user, self.id, key)
        
        return value
    
    @validates("username")
    def validate_username(self, key, value):
        validation_string(key, value)
        
        user = User.query.filter_by(username=value).first()
        validation_identifier(user, self.id, key)
        
        return value
    
    @validates("lastname", "name")
    def validate_name(self, key, value):
        validation_string(key, value)
        
        return value