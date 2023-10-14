from src.core.database import db
from datetime import datetime
from src.core.models.user.user import User

class Comment(db.Model):
    __tablename__ = "comments"
    id = db.Column(db.Integer, primary_key=True, unique=True)
    comment = db.Column(db.String(200))
    user = db.relationship('User', back_populates='comments')
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete="CASCADE"))
    service_order = db.relationship('Service_order', back_populates='comments')
    service_order_id = db.Column(db.Integer, db.ForeignKey("service_orders.id", ondelete="CASCADE"))
    
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )
    inserted_at = db.Column(
        db.DateTime, default=datetime.utcnow
    )
    

class Service_order(db.Model):
    __tablename__ = "service_orders"
    id = db.Column(db.Integer, primary_key=True, unique=True)
    title = db.Column(db.String(100), unique=True)
    description = db.Column(db.String(200))
    creation_date = db.Column(db.DateTime, default=datetime.utcnow)
    close_date = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(50))
    statusChanged = db.Column(db.DateTime, default=datetime.utcnow)
    comments = db.relationship('Comment', back_populates='service_order', lazy=True)
    user = db.relationship('User', back_populates='service_orders')
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete="CASCADE"))
    service = db.relationship('Service', back_populates='service_orders')
    service_id = db.Column(db.Integer, db.ForeignKey("services.id", ondelete="CASCADE"))
    
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )
    inserted_at = db.Column(
        db.DateTime, default=datetime.utcnow
    )