from src.core.models.service_order.service_order import Service_order
from src.core.models.service_order.service_order import Comment
from src.core.database import db
from sqlalchemy import or_

def list_orders_paginated(page, per_page):
    """
    Me devuelve todas las ordenes de servicio.
    """
    
    orders = Service_order.query.paginate(page=page, per_page=per_page, error_out=False)
    return orders

def list_orders_paginated_by_user(page, per_page, user_id):
    """
    Me devuelve todas las ordenes de servicio de un usuario.
    """
    
    orders = Service_order.query.filter(Service_order.user_id == user_id).paginate(page=page, per_page=per_page, error_out=False)
    return orders

def total_orders_pages(per_page):
    """
    Me devuelve la cantidad de paginas que ocupan los pedidos de servicios.
    """
    total_orders = Service_order.query.count()  # Total de pedidos
    if(total_orders == 0):
        return 1
    total_pages = (total_orders + per_page - 1)// per_page  # Cálculo de páginas
    return total_pages

def get_order_by_id(id):
    """
    Me devuelve una orden de servicio por id.
    """   
    order = Service_order.query.filter(Service_order.id == id).first()
    return order

def create_order(**kwargs):
    """"
    Crear una orden de servicio y almacenarla en la db.
    """
    order = Service_order(**kwargs)
    db.session.add(order)
    db.session.commit()
    return order

def add_comment(**kwargs):
    """"
    Crear un comentario y almacenarla en la db.
    """
    comment = Comment(**kwargs)
    db.session.add(comment)
    db.session.commit()
    return comment