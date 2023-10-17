from flask import Blueprint, request, jsonify
from src.core.models import user as Users
from src.web.schemas.users import user_schema, create_user_schema
from src.web.helpers import auth 

api_users = Blueprint("api_users", __name__, url_prefix="/api/users")


@api_users.get("/profile")
@auth.login_required
def user_show():
    # Requiere validacion de JWT
    
    user = Users.user_show(request.args.get("id"))
    if user is None:
        return jsonify({"error": "Parámetros inválidos"}), 400
    
    data = user_schema.dumps(user)
    
    return data, 200

@api_users.post("/user-create")
@auth.permission_required("user_create")
def user_create():
    data = request.get_json()
    new_user = create_user_schema.load(data)
    if Users.exists_user(new_user["email"]):
        return jsonify({"error": "El email ya existe, por favor ingresa otro"}), 400
    
    if Users.exists_user(new_user["username"]):
        return jsonify({"error": "El nombre de usuario ya existe, por favor ingresa otro"}), 400
    
    user = Users.user_create(**new_user)
    
    return user_schema.dumps(user), 201