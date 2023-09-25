from flask import json, jsonify
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
    
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )
    inserted_at = db.Column(
        db.DateTime, default=datetime.utcnow
    )

    def to_json(self):
        user_dict = {
            'id': self.id,
            'email': self.email,
            'username': self.username,
            'password': self.password,
            'name': self.name,
            'lastname': self.lastname,
            'active': self.active,
            'confirmed': self.confirmed,
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
            'inserted_at': self.inserted_at.strftime('%Y-%m-%d %H:%M:%S')
        }
        return jsonify(user_dict)