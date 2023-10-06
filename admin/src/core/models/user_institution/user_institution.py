from sqlalchemy import UniqueConstraint
from src.core.database import db
from datetime import datetime


class UserInstitution(db.Model):
    __tablename__ = "user_institutions"
    __table_args__ = (UniqueConstraint('user_id', 'institution_id', name='_user_institution_uc'),)
    id = db.Column(db.Integer, primary_key=True, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"))
    institution_id = db.Column(db.Integer, db.ForeignKey("institutions.id", ondelete="CASCADE"))
    role_id = db.Column(db.Integer, db.ForeignKey("roles.id", ondelete="CASCADE"))
    
    user = db.relationship("User", back_populates="institutions", lazy=True)
    institution = db.relationship("Institution", back_populates="users", lazy=True)
    role = db.relationship("Role", back_populates="users_institutions", lazy=True)
    
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )
    inserted_at = db.Column(
        db.DateTime, default=datetime.utcnow
    )