from src.core.models import institution as Institutions
from src.core.models import user as User
from flask import Blueprint, jsonify, request
from src.web.helpers import auth
from src.web.schemas.auth import create_auth_schema

api_auth = Blueprint("api_auth", __name__, url_prefix="/auth")

@api_auth.post("/")
def create_jwt():
    params = request.get_json()
    data = create_auth_schema.load(params)
    user = User.check_auth_user(data["email"],data["password"])
    if(user is None):
        return jsonify({"error": "Parámetros inválidos"}), 400
    else:
        return jsonify({"success": "Usuario existente"}), 200