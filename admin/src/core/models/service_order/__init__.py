from src.core.database import db
from sqlalchemy import or_
from src.core.models.service_order.service_order import Service_order, Service_order_status, Service_order_status_changed
from src.core.models.service_order.service_order import Comment
from src.core.models.user.user import User
from src.core.models import system

def list_page_service_request(page, type_service, status, date_from, date_to, user_email):
    """
    Me devuelve todas las paginas de solicitudes de servicio coincidentes con la busqueda.
    
    Args:
        page -> numero de pagina a retornar. \n
        user_email -> filtro de busqueda por email del usuario. \n
        status -> estado actual de la solicitud. \n
        type_service -> tipo del servicio. \n
        date_from -> fecha desde la cual se quiere buscar. \n
        date_to -> fecha hasta la cual se quiere buscar. \n
    """
    subquery = db.session.query(User.id).filter(User.email.ilike(f"%{user_email}%")).subquery()
    orders = Service_order.query.filter(Service_order.user_id.in_(subquery)).paginate(page=page, per_page=system.pages(), error_out=False)
    
    return orders, orders.pages


def service_request_show(issue_id):
    """
        Busca y retorna una solicitud de servicio a traves de su id.
    """
    service_request = Service_order.query.filter(Service_order.id == issue_id).first()

    return service_request

def get_order_status_by_name(name):
    """
    Me devuelve un estado de orden de servicio por nombre.
    """   
    order_status = Service_order_status.query.filter(Service_order_status.name == name).first()
    return order_status

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

def list_status():
    """
    Me devuelve todos los estados de orden de servicio.
    """
    status = Service_order_status.query.all()
    return status

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
    
    change_status_order(
        service_order=order,
        service_order_status=get_order_status_by_name("En proceso"),
        note="Se ha recibido una nueva solicitud de servicio."
    )
    
    return order

def add_comment(**kwargs):
    """"
    Crear un comentario y almacenarla en la db.
    """
    comment = Comment(**kwargs)
    db.session.add(comment)
    db.session.commit()
    return comment

def create_order_status(**kwargs):
    """"
    Crear un estado de orden de servicio y almacenarla en la db.
    """
    order_status = Service_order_status(**kwargs)
    db.session.add(order_status)
    db.session.commit()
    return order_status

def change_status_order(**kwargs):
    """"
    Crear un cambio de estado de orden de servicio y almacenarla en la db.
    """
    order_status_changed = Service_order_status_changed(**kwargs)
    db.session.add(order_status_changed)
    db.session.commit()
    return order_status_changed

def get_actual_state(order_id):
    """
    Me devuelve el estado actual de una orden de servicio.
    """
    status = Service_order_status_changed.query.filter(Service_order_status_changed.service_order_id == order_id).order_by(Service_order_status_changed.id.desc()).first()
    
    return status