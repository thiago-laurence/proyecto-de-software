from flask import Blueprint, jsonify
from src.core.models import system as System
api_contact = Blueprint("api_contact", __name__, url_prefix="/contact")

@api_contact.get('/')
def get_contact_info():
    """
    Retorna en formato JSON la informacion de
    contacto.
    """
    info = System.contact()
    return jsonify(info), 200


