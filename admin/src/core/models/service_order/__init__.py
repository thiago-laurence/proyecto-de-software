from datetime import datetime
from src.core.database import db
from sqlalchemy import or_, select, desc, asc
from src.core.models.service_order.service_order import Service_order, Service_order_status, Service_order_status_changed, Comment
from src.core.models.institution.service import Service, TypeService
from src.core.models.institution.institution import Institution
from src.core.models.user.user import User
from src.core.models import system

def list_page_service_request(institution_id, page, type_service, status, date_from, date_to, user_email):
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
    subquery = db.session.query(Service.id).filter(Service.institution_id == institution_id).subquery().select()
    orders = Service_order.query.filter(Service_order.service_id.in_(subquery)).order_by(Service_order.inserted_at)
    
    if user_email != "":
        orders = orders.filter(Service_order.user.has(User.email.ilike(f"%{user_email}%")))
    if date_from != "" and date_to != "":
        date_from = (datetime.strptime(date_from, '%d/%m/%Y')).strftime('%Y-%m-%d')
        date_to = (datetime.strptime(date_to, '%d/%m/%Y')).strftime('%Y-%m-%d')
        orders_from = orders.filter(Service_order.creation_date >= date_from, Service_order.creation_date <= date_to)
        orders_to = orders.filter(Service_order.close_date <= date_to, Service_order.close_date >= date_from)
        orders = orders_from.union(orders_to)
    if status != "":
        status = int(status)
        subquery = (
            db.session.query(Service_order_status_changed.service_order_status_id)
            .filter(Service_order_status_changed.service_order_id == Service_order.id)
            .order_by(desc(Service_order_status_changed.id))
            .limit(1)
            .subquery()
        )
        orders = orders.filter(subquery.as_scalar() == status)
    if type_service != "":
        type_service = int(type_service)
        orders = orders.filter(Service_order.service.has(Service.type_service_id == type_service))
    
    
    
    orders = orders.paginate(page=page, per_page=system.pages(), error_out=False)
    
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
    orders_in_page = orders.total < page * per_page
    return orders, orders_in_page

def list_orders_paginated_with_filters(status, date_from, date_to, page, per_page, user_id):
    """
        Si el estado es distinto de vacio me devuelve las ordenes filtradas por estado.
        Lo mismo pero con el rango de fechas
    """
    orders = Service_order.query.filter(Service_order.user_id == user_id)
    
    if date_from != "" and date_to != "":
        date_from = (datetime.strptime(date_from, '%Y-%m-%d'))
        date_to = (datetime.strptime(date_to, '%Y-%m-%d'))
        orders_from = orders.filter(Service_order.user_id == user_id, Service_order.creation_date >= date_from, Service_order.creation_date <= date_to)
        orders_to = orders.filter(Service_order.user_id == user_id, Service_order.close_date <= date_to, Service_order.close_date >= date_from)
        orders = orders_from.union(orders_to)
    if status != "":
        status = int(status)
        subquery = (
            db.session.query(Service_order_status_changed.service_order_status_id)
            .filter(Service_order_status_changed.service_order_id == Service_order.id)
            .order_by(desc(Service_order_status_changed.id))
            .limit(1)
            .subquery()
        )
        orders = orders.filter(subquery.as_scalar() == status)
        
    orders = orders.paginate(page=page, per_page=per_page, error_out=False)
    
    return orders, orders.pages
    

def order_orders_by_description(service_orders, order):
    """
    Me devuelve todas las ordenes de servicio ordenadas por descripcion.
    """
    if(order == "asc"):
        orders = sorted(service_orders, key=lambda x: x.description)
    else:
        orders = sorted(service_orders, key=lambda x: x.description, reverse=True)
    return orders

def order_orders_by_creation_date(service_orders, order):
    """
    Me devuelve todas las ordenes de servicio ordenadas por fecha.
    """
    if(order == "asc"):
        orders = sorted(service_orders, key=lambda x: x.creation_date)
    else:
        orders = sorted(service_orders, key=lambda x: x.creation_date, reverse=True)
    return orders

def order_orders_by_close_date(service_orders,order):
    """
    Me devuelve todas las ordenes de servicio ordenadas por fecha.
    """
    if(order == "asc"):
        orders = sorted(service_orders, key=lambda x: x.close_date)
    else:
        orders = sorted(service_orders, key=lambda x: x.close_date, reverse=True)
    return orders

def order_orders_by_title(service_orders, order):
    """
    Me devuelve todas las ordenes de servicio ordenadas por titulo.
    """
    if(order == "asc"):
        orders = sorted(service_orders, key=lambda x: x.title)
    else:
        orders = sorted(service_orders, key=lambda x: x.title, reverse=True)
    return orders

def order_orders(service_orders, sort, order):
    """
    Me devuelve todas las ordenes de servicio ordenadas.
    """
    # if(sort == "title"):
    #     orders = order_orders_by_title(service_orders, order)
    # elif(sort == "description"):
    #     orders = order_orders_by_description(service_orders, order)
    if(sort == "creation_date"):
        orders = order_orders_by_creation_date(service_orders, order)
    elif(sort == "close_date"):
        orders = order_orders_by_close_date(service_orders, order)
    else:
        orders = service_orders
    return orders

def index_status():
    """
    Me devuelve todos los estados de orden de servicio.
    """
    status = Service_order_status.query.all()
    return status

def total_orders_pages(per_page, user_id):
    """
    Me devuelve la cantidad de paginas que ocupan los pedidos de servicios.
    """
    total_orders = Service_order.query.filter(Service_order.user_id == user_id).count()  # Total de pedidos por persona
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
    status = Service_order_status_changed.query.filter(Service_order_status_changed.service_order_id == order_id)\
        .order_by(Service_order_status_changed.id.desc()).first()
    
    return status

def cant_request_by_type():
    """
    Retorna la cantidad de solicitudes procesadas agrupadas por tipo de solicitud.
    """
    
    request = db.session.execute(select(TypeService.name, db.func.count())\
        .join(Service_order.service).join(Service.type_service)\
            .group_by(Service.type_service_id, TypeService.name)).all()
    
    return request

def best_request_service():
    """
    Retorna las cinco solicitudes de servicio mas solicitadas.
    """
    
    request = db.session.execute(select(Service.name, Institution.name, db.func.count(Service_order.service_id).label("Cantidad"))\
        .join(Service_order.service).join(Service.institution)\
            .group_by(Service_order.service_id, Service.name, Institution.name)\
                .order_by(asc("Cantidad"))\
                    .limit(5)).all()
    
    return request

def best_institutions_resolution():
    """
    Retorna las diez instituciones con mejor tiempo de resolucion de solicitudes.
    """
    
    request = db.session.execute(select(Institution.name, db.func.avg(Service_order.end_date - Service_order.inserted_at).label("Tiempo de resolucion"))\
        .join(Service_order.service).join(Service.institution)\
            .group_by(Institution.name)\
                .order_by(asc("Tiempo de resolucion"))\
                    .limit(10)).all()
    
    return request

def update_end_date(service_order_id, end_date):
    """
    Actualiza la fecha de finalizacion de una orden de servicio.
    """
    service_order = Service_order.query.filter(Service_order.id == service_order_id).first()
    service_order.end_date = end_date
    db.session.commit()
    
    return service_order