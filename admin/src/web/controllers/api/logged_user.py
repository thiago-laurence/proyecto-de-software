from flask import Blueprint, render_template, request, flash, redirect, url_for, session, jsonify
from src.core.models import user as Users
from src.core.models import institution
from src.web.helpers import auth
from src.core.models import service_order as orders
from src.web.schemas.service_orders import service_orders_schema, service_order_schema, service_order_schema_with_id, create_service_order_schema, comment_schema, create_comment_schema
from datetime import datetime

api_logged_user= Blueprint("logged_user", __name__, url_prefix="/me")


@api_logged_user.get("/profile")
@auth.login_required
def user_info():
    """
    Retorna en formato JSON la información del usuario logueado.
    """ 
    user = Users.find_user(session['user']['email'])
    return user.to_json()


@api_logged_user.get("/requests")
#@auth.login_required
def user_requests():
    """
    Retorna en formato JSON las solicitudes del usuario logueado.
    """ 
    user = Users.find_user(session['user']['email'])
    
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    if(page == 0 or per_page == 0):
        return jsonify({"error": "Parámetros inválidos"}), 400
        
    service_orders = orders.list_orders_paginated_by_user(page, per_page, user.id)
    total_pages = orders.total_orders_pages(per_page,user.id)
    
    if(service_orders[1]):
        return jsonify({"error": "Parámetros inválidos"}), 400
    
    data = service_orders_schema.dump(service_orders[0])
    
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
#@auth.login_required
def user_request_by_id(id):
    """
    Retorna en formato JSON la solicitud del usuario logueado.
    """ 
    user = Users.find_user(session['user']['email'])
    service_order = orders.get_order_by_id(id)
    
    if(service_order.user_id != user.id):
        data = {"error": "Parámetros inválidos"}
        return jsonify(data), 400
    else:     
        data = service_order_schema.dump(service_order)
        return jsonify(data)
    

#tanto en la creacion de pedidos de servicios como de comentarios a los mismos comente la logica de los usuarios para poder probarlo con el cliente thunder client
@api_logged_user.post("/requests")
#@auth.login_required
def create_order():
    """
    Crea una orden de servicio.
    """
    #user = Users.find_user(session['user']['email'])
    data = request.get_json()
    service = institution.get_service_by_id(data['service_id'])
    
    if(service is None or data['title'] == None or data['description'] == None):
        response = {"error": "Parámetros inválidos"}
        return jsonify(response), 400
    
    else:
        #data['user_id']= user.id
        data['status'] = "Pendiente"
        data['statusChanged'] = datetime.utcnow()
        
        errors = create_service_order_schema.validate(data)
        if errors:
            return errors, 400
        
        new_order = create_service_order_schema.load(data)
        obj_new_order = orders.create_order(**data)
        
        return service_order_schema_with_id.dumps(obj_new_order), 201

@api_logged_user.post("/requests/<id>/notes")
#@auth.login_required
def add_comment(id):
    """
    Crea un comentario en una orden de servicio.
    """
    data = request.get_json()
    #user = Users.find_user(session['user']['email'])
    order = orders.get_order_by_id(id)
    
    #order.user_id != user.id or 
    if(data['comment'] == None):
        response = {"error": "Parámetros inválidos"}
        return jsonify(response), 400
    
    #data['user_id']= user.id
    data['service_order_id']= id
    
    errors = create_comment_schema.validate(data)
    if errors:
        return errors, 400
    
    new_comment = create_comment_schema.load(data)
    obj_new_comment = orders.add_comment(**data)
    
    return comment_schema.dumps(obj_new_comment), 201