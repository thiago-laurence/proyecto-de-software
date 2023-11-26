from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required
from src.core.models import user as Users
from src.core.models import service_order as orders
from src.core.models import institution
from src.core.models import system
from src.web.helpers import auth
from src.web.schemas.service_orders import service_orders_schema, service_order_schema, service_order_schema_with_id, create_service_order_schema, comment_schema, create_comment_schema
from src.web.schemas.users import user_schema, create_user_schema

api_logged_user= Blueprint("logged_user", __name__, url_prefix="/me")


@api_logged_user.get("/profile")
@jwt_required()
def user_show():
    # Requiere recepcion y validacion de JWT
    user_id = get_jwt_identity()
    user = Users.user_show(user_id)
    
    if user is None:
        return jsonify({"error": "Parámetros inválidos"}), 400
    
    data = user_schema.dump(user)
    
    return data, 200


@api_logged_user.post("/user-create")
@jwt_required()
def user_create():
    data = request.get_json()
    try:
        new_user = create_user_schema.load(data)
    except Exception as err:
        return jsonify({"error": err.messages}), 400
    
    if Users.exists_user(new_user["email"]):
        return jsonify({"error": "El email ya existe, por favor ingresa otro"}), 400
    
    if Users.exists_user(new_user["username"]):
        return jsonify({"error": "El nombre de usuario ya existe, por favor ingresa otro"}), 400
    
    user = Users.user_create(**new_user)
    
    return user_schema.dump(user), 201

#hay que agregarle sort (criterio de ordenacion) y order (desc o asc)
@api_logged_user.get("/requests")
@jwt_required()
def user_requests():
    """
    Retorna en formato JSON las solicitudes del usuario logueado.
    """ 
    user_id = get_jwt_identity()
    
    #parametros de paginacion
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', system.pages(), type=int)
    #parametros de ordenacion
    sort = request.args.get('sort', "", type=str)
    order = request.args.get('order', "asc", type=str) #asc es ascendente y desc es descendente
    #parametros de filtrado
    status = request.args.get('status', "", type=str)
    creation_date = request.args.get('creation_date', "", type=str)
    close_date = request.args.get('close_date', "", type=str)
    
    # if(status != "Aceptada" and status != "Rechazada" and status != "En proceso" and status != "Finalizada" and status != "Cancelada"):
    #     return jsonify({"error": "Parámetros inválidos"}), 400
    
    if(page == 0 or per_page == 0):
        return jsonify({"error": "Parámetros inválidos"}), 400
    
    if(sort != "creation_date" and sort != "close_date"):
        sort = ""
        order = ""
    else: 
        if(order != "asc" and order != "desc"):
            order = "asc"
            
    if(status != "" or (creation_date != "" and close_date != "")):
        filtered_services = orders.list_orders_paginated_with_filters(status, creation_date, close_date, page, per_page, user_id)
        service_orders = filtered_services[0]
        total_pages = filtered_services[1]
    else:
        orders_without_filters = orders.list_orders_paginated_by_user(page, per_page, user_id)
        service_orders = orders_without_filters[0]
        total_pages = orders.total_orders_pages(per_page,user_id)
    
    print(service_orders)
    if(service_orders.total == 0):
        return jsonify({"error": "No se encontraron elementos"}), 400
    else:    
        if(page > total_pages):
            return jsonify({"error": "No hay elementos en esa pagina"}), 400
    
    order_services = orders.order_orders(service_orders, sort, order)
    
    data = service_orders_schema.dump(order_services)
    
    response = [
        {
            "data": data,
            "page": page,
            "per_page": per_page,
            "total": total_pages
        }
    ]
    return jsonify(response) 


@api_logged_user.get("/requests/<id>")
@jwt_required()
def user_request_by_id(id):
    """
    Retorna en formato JSON la solicitud del usuario logueado.
    """ 
    user_id = get_jwt_identity()
    
    service_order = orders.get_order_by_id(id)
    
    if(service_order is None or service_order.user_id != user_id):
        data = {"error": "Parámetros inválidos"}
        return jsonify(data), 400
    else:     
        data = service_order_schema.dump(service_order)
        return jsonify(data)
    

@api_logged_user.post("/requests")
@jwt_required()
def create_order():
    """
    Crea una orden de servicio.
    """
    user_id = get_jwt_identity()
    
    data = request.get_json()
    service = institution.get_service_by_id(data['service_id'])
    insti = institution.get_institution_by_id(service.institution_id)
    
    if(not insti.is_enabled):
        return jsonify({"error": "Institucion deshabilitada"}), 400
    
    if(service is None or data['title'] == None or data['description'] == None):
        return jsonify({"error": "Parámetros inválidos"}), 400
    
    else:
        data['user_id']= user_id
        
        errors = create_service_order_schema.validate(data)
        if errors:
            return errors, 400
        
        new_order = create_service_order_schema.load(data)
        obj_new_order = orders.create_order(**data)
        
        return service_order_schema_with_id.dumps(obj_new_order), 201

@api_logged_user.post("/requests/<id>/notes")
@jwt_required()
def add_comment(id):
    """
    Crea un comentario en una orden de servicio.
    """
    data = request.get_json()
    user_id = get_jwt_identity()
    
    order = orders.get_order_by_id(id)

    if(order is None or order.user_id != user_id or data['comment'] == None):
        response = {"error": "Parámetros inválidos"}
        return jsonify(response), 400
    
    data['user_id']= user_id
    data['service_order_id']= id
    
    errors = create_comment_schema.validate(data)
    if errors:
        return errors, 400
    
    new_comment = create_comment_schema.load(data)
    obj_new_comment = orders.add_comment(**data)
    
    return comment_schema.dumps(obj_new_comment), 201