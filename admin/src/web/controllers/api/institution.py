from src.core.models import institution as Institutions
from src.core.models import user
from flask import Blueprint, jsonify, request
from src.web.helpers import auth
from src.web.schemas.institutions import institutions_schema
from src.core.models import system

api_institutions = Blueprint("api_institutions", __name__, url_prefix="/institutions")

@api_institutions.get("/")
#@auth.permission_required("institution_index") 
def get_institutions():
    """
    Retorna en formato JSON la información de las instituciones.
    """
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", system.pages(), type=int)
    total_pages = Institutions.total_intitutions_pages(per_page)
    
    if(page <= total_pages and page > 0):
    
        institutions = Institutions.list_institutions_paginated(page, per_page)
        if institutions.total == 0:
            return jsonify({"error": "No se encontraron resultados"}), 404

        data = institutions_schema.dump(institutions)
        rta = {
            "data": data,
            "page": page,
            "per_page": per_page,
            "total": total_pages
        }

        return rta, 200
    else:   
        return jsonify({"error": "Parametros invalidos"}), 400
