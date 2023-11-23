from flask import Blueprint, jsonify
from src.core.models import service_order as Service_Orders

api_data= Blueprint("data", __name__, url_prefix="/data")

@api_data.get("/cant_request")
def cant_request_by_type():
    """
        Cantidad de solicitudes agrupadas por tipo de solicitud.
    """
    request_service = Service_Orders.cant_request_by_type()
        
    data = {}
    for i in request_service:
        data[i[0]] = i[1]
    
    return jsonify(data), 200
    
@api_data.get("/best_request_service")
def best_request_service():
    """
        Mejores solicitudes de servicio.
    """
    request_service = Service_Orders.best_request_service()
    
    data = {}
    for i in request_service:
        data[i[0] + " - " + i[1]] = i[2]
    
    return jsonify(data), 200

@api_data.get("/best_institutions_resolution")
def best_institutions_resolution():
    """
        Mejores instituciones por tiempo de resolucion de solicitudes.
    """
    request_service = Service_Orders.best_institutions_resolution()
    data = {}
    for nombre, tiempo_resolucion in request_service:
        if tiempo_resolucion is not None:
            total_seconds = tiempo_resolucion.total_seconds()
            dias = int(total_seconds // (3600 * 24))
            horas = int(total_seconds % (3600 * 24) // 3600)
            # data[nombre] = f"{horas} horas y {minutos} minutos"
            data[nombre] = [dias, horas]
        else:
            # data[nombre] = f"Sin resoluciones"
            data[nombre] = [0, 0]
    
    return jsonify(data), 200