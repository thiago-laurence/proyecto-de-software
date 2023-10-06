from src.core.models import institution as Institutions
from src.core.models.institution import service as Service
from src.core.models import user
from flask import Blueprint, jsonify, request
from src.web.helpers import auth


api_services = Blueprint("api_services", __name__, url_prefix="/services")

@api_services.get("/search")
def search():
    """
    Retorna en formato JSON la información de los servicios que coincidan con la búsqueda.
    Por ahora solo busca por id de insti, faltan mas parametros en la url
    """
    if  not "q" in request.args:
        return jsonify({"error": "Parámetros inválidos"}), 400
        
    substr = request.args.get("q")
    
    services = Institutions.services_serch(substr)

    #intitution = Institutions.get_institution_by_id(institution_id)

    if len(services) == 0:
        return jsonify({"mensaje": "No se encontraron resultados"}), 200
    
    rta = {
        "data": [   
        ]
    }
    
    for service in services:
        rta["data"].append(service.to_json())
        
    return jsonify(rta), 200

@api_services.get("/<service_id>")
@auth.login_required
def search_by_id(service_id):
    """
    Retorna en formato JSON la información del servicio que coincida con la búsqueda.
    """
    if service_id == "":
        return jsonify({"error": "Parámetros inválidos"}), 400
    
    service = Institutions.get_service_by_id(service_id)

    if service is None:
        return jsonify({"error": "No se encontraron resultados"}), 404
    
    return jsonify(service.to_json()), 200


@api_services.get("/services-types")
def get_services_types():
    """
    Retorna en formato JSON los tipos de servicios disponibles.
    """
    if "Authorization" in request.headers:
        username = request.headers["Authorization"].split(":")[0]
                
        print("nombre de usuario: ",username)
    
        usuario = user.find_user(username)
        
        if usuario is not None:
            return jsonify({"data": [service.name for service in Service.Tipo]}), 200

    # Si la autenticación falla
    return jsonify({"error": "Autenticación fallida"}), 401

    