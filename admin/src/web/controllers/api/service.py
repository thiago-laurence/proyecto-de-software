from src.core.models import institution as Institutions
from src.core.models.institution import service as Service
from src.core.models import user
from flask import Blueprint, jsonify, request
from src.web.helpers import auth
from src.web.schemas.services import services_schema,service_schema, types_services_schema
from src.web.schemas.state_orders import state_order_schema
from src.core.models import system, service_order as orders


api_services = Blueprint("api_services", __name__, url_prefix="/services")

@api_services.get("/search")
def search():
    """
    Retorna en formato JSON la información de los servicios habilitados que coincidan con la búsqueda.
    """
    if  not "q" in request.args:
        return jsonify({"error": "Parámetros inválidos"}), 400
        
    substr = request.args.get("q")
    tipo = request.args.get("type","",type=str)
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", system.pages(), type=int)
    
    total_pages = Institutions.total_services_pages_for_search(substr,page,per_page,tipo)
    
    if(page <= total_pages and page > 0):
    
        services = Institutions.services_serch(substr,page,per_page,tipo)

        if services.total == 0:
            return jsonify({"mensaje": "No se encontraron resultados"}), 200
        
        data = services_schema.dump(services)
        rta = {
            "data": data,
            "page": page,
            "per_page": per_page,
            "total": total_pages
        }
            
        return jsonify(rta), 200
    else:
        return jsonify({"error":"No hay elementos en esa pagina"})

@api_services.get("/<service_id>")
#@auth.permission_required("service_show")
def search_by_id(service_id):
    """
    Retorna en formato JSON la información del servicio que coincida con la búsqueda.
    """
    service = Institutions.get_service_by_id(service_id)

    if service is None:
        return jsonify({"error": "No se encontraron resultados"}), 404
    
    return service_schema.dump(service), 200


@api_services.get("/services-types")
def get_services_types():
    """
    Retorna en formato JSON los tipos de servicios disponibles.
    """
    types_services = Institutions.index_type_service()
    
    return types_services_schema.dump(types_services), 200

@api_services.get("/orders-state")
def get_orders_state():
    """
    Retorna en formato JSON los estados de las solicitudes.
    """
    states = orders.index_status()
    
    return state_order_schema.dump(states), 200

    