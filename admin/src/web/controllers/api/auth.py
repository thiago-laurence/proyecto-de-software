import requests
from flask import Blueprint, jsonify, request, url_for, render_template
from flask_jwt_extended import create_access_token
from src.core.models import user as User
from src.web.schemas.auth import create_auth_schema
from src.web.schemas.users import create_user_signup_schema
from src.web import mail as Mail
from src.web import token as Token

api_auth = Blueprint("api_auth", __name__, url_prefix="/auth")

@api_auth.post("/")
def create_jwt():
    params = request.get_json()
    try:
        data = create_auth_schema.load(params)
    except Exception as err:
        result = {"error": ""}
        for i in err.messages:
            result["error"] += err.messages[i][0] + ". \n"
        return jsonify(result), 400
    
    user = User.check_auth_user(data["email"], data["password"])
    
    if(user is None):
        return jsonify({"error": "Acceso no autorizado"}), 401
    else:
        access_token = create_access_token(identity=user.id)
        return jsonify({"token": access_token}), 200

@api_auth.post("/sign-up")
def sign_up():
    data = request.get_json()
    try:
        new_user = create_user_signup_schema.load(data)
    except Exception as err:
        result = {"error": ""}
        for i in err.messages:
            result["error"] += err.messages[i][0] + ". \n"
        return jsonify(result), 400

    if User.exists_user(new_user["email"]):
        return jsonify({"error": "El email ya existe, por favor ingresa otro"}), 400

    user = User.parcial_register_user(**new_user)
    token = Token.generate_confirmation_token(user.email)
    confirm_url = url_for('users.confirm_email', token=token, _external=True)
    html = render_template('users/_email-confirm-account.html', confirm_url=confirm_url)
    subject = "Confirme su cuenta"
    Mail.send_email(user.email, subject, html)
    
    return jsonify({"success": "El registro parcial fue exitoso, por favor verifique su casilla de correo"}), 201

@api_auth.post("/google")
def login_google():
    data = request.get_json()['userInfo']
    user = User.find_user(data["email"])
    
    if(user is None):
        new_user = {
            "email": data["email"], 
            "lastname": data["family_name"], 
            "name": data["given_name"],
            "username": data["email"].split("@")[0]
        }
        user = User.parcial_register_user(**new_user)    
        
    access_token = create_access_token(identity=user.id)
    return jsonify({"token": access_token}), 200


@api_auth.route('/verify-token', methods=['POST'])
def verify_token():
    token = request.get_json()['token']
    # google_response = requests.get(f'https://www.googleapis.com/oauth2/v1/tokeninfo?access_token={token}')
    google_response = requests.get(f'https://www.googleapis.com/oauth2/v3/userinfo?access_token={token}') 
    
    if google_response.ok:
        user_info = google_response.json()
        user = User.find_user(user_info['email'])
        if user is None:
            new_user = {
                "email": user_info["email"], 
                "lastname": user_info["family_name"], 
                "name": user_info["given_name"],
                "username": user_info["email"].split("@")[0]
            }
            user = User.parcial_register_user(**new_user)
        
        access_token = create_access_token(identity=user.id)
        return jsonify({"token": access_token}), 200
    
    else:
        return jsonify({'error': 'Token inválido'}), 401