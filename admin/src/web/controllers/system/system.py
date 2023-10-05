from flask import Blueprint, render_template, request, Response, json, flash
from src.core.models import system as System
from src.web.helpers import auth

system_blueprint = Blueprint("system", __name__, url_prefix="/system")

@system_blueprint.get("/<system_id>")
@auth.permission_required("system_show")
def index(system_id):
    """
        Redirige a la configuración del sistema
        
        args:
            system_name: nombre del sistema a mostrar su configuración.
    """
    sys = System.system_show(system_id)
    
    if sys is None:
        cod = 400
        data = {
            "error": "El sistema no existe"
        }
    else:
        cod = 200
        data = sys.to_json()
        
    response = Response(
        response = json.dumps(data),
        status = cod,
        mimetype = 'application/json'
    )
    
    return render_template("system/index.html", system=response.json)


@system_blueprint.put("/system-update/<system_id>")
@auth.permission_required("system_update")
def system_update(system_id):
    """
        Actualiza la información del sistema.
        
        args:
            system_id: id del sistema a modificar.
        
        return:
            JSON response system 200
            
            JSON response error 400
    """
    response = Response(mimetype = 'application/json')
    
    if int(request.json['data']['element_page']) == 0:
        response.set_data(json.dumps({
            "error": "parametros invalidos",
            "url": "/system/"+ str(system_id)
        }))
        response.status_code = 400
        flash("La cantidad de elementos de página no puede ser cero", "error")
        return response.get_json()
    
    system = System.system_update(system_id, **request.json['data'])

    if system is None:
        data = {
            "error": "parametros incorrectos"
        }
        cod = 400
    else:
        data = {
            "url" : '/system/'+ str(system.id),
        }
        cod = 200
    
    response = Response(
        response = json.dumps(data),
        status = cod,
        mimetype = 'application/json'
    )
    
    flash("La información del sistema ha sido actualizada con exito!", "success")
    
    return response.json