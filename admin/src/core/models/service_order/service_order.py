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


class Service_order_status(db.Model):
    __tablename__ = "service_order_status"
    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(50), unique=True)
    services_orders = db.relationship('Service_order_status_changed', back_populates='service_order_status')
    
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )
    inserted_at = db.Column(
        db.DateTime, default=datetime.utcnow
    )
    
    
class Service_order_status_changed(db.Model):
    __tablename__ = "service_order_status_changed"
    id = db.Column(db.Integer, primary_key=True, unique=True)
    note = db.Column(db.String(200))
    
    service_order = db.relationship('Service_order', back_populates='status_changes')
    service_order_id = db.Column(db.Integer, db.ForeignKey("service_orders.id", ondelete="CASCADE"))
    
    service_order_status = db.relationship('Service_order_status', back_populates='services_orders')
    service_order_status_id = db.Column(db.Integer, db.ForeignKey("service_order_status.id", ondelete="CASCADE"))
    
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
    comments = db.relationship('Comment', back_populates='service_order', lazy=True)
    user = db.relationship('User', back_populates='service_orders')
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete="CASCADE"))
    service = db.relationship('Service', back_populates='service_orders')
    service_id = db.Column(db.Integer, db.ForeignKey("services.id", ondelete="CASCADE"))
    status_changes = db.relationship('Service_order_status_changed', back_populates='service_order', lazy=True)
    
    @property
    def status_actual(self):
        service_order = Service_order_status_changed.query.filter(Service_order_status_changed.service_order_id == self.id)\
            .order_by(Service_order_status_changed.id.desc()).first()
        
        return service_order.service_order_status_id
    
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )
    inserted_at = db.Column(
        db.DateTime, default=datetime.utcnow
    )