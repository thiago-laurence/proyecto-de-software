from flask import Blueprint, render_template, request, flash, redirect, url_for, session, Response, json
from src.core.models import user as Users
from src.web.helpers import auth
from src.web import mail

users_blueprint = Blueprint("users", __name__, url_prefix="/users")

@users_blueprint.get("/sing-up")
def sign_up():
    """
        Redirige al formulario de registro de usuario.
    """
    
    return render_template("users/sign_up.html")

@users_blueprint.post("/sign-up/register")
def register():
    """
        Registra un nuevo usuario (de forma parcial) obtiendo los datos del formulario.
        args:
            email: email del usuario a registrar.
            name: nombre del usuario a registrar.
            lastname: apellido del usuario a registrar.
    """

    params = request.form
    user = Users.find_user(params['email'])
    if user:
        flash("El email ingresado ya está registrado, por favor ingresa otro", "error")
        return redirect(url_for("users.sign_up"))
    
    user = Users.create_user(email=params['email'], name=params['name'], lastname=params['lastname'])
    url = request.host_url + "/users/sign-up/confirm"
    body = """
        <p> Bienvenido a CIDEPINT, para completar el registro ingresa al siguiente link: </p>
        <form action=""" + url + """ method="POST">
            <input type="hidden" name="email" value=""" + user.email + """>
            <button type="submit">Confirmar</button>
        </form>
    """
    mail.send_mail("Confirmación de registro", params['email'], body)
    
    flash("Registro parcial exitoso. Se ha enviado un correo de confirmación de registro a la dirección ingresada", "success")
    
    return redirect(url_for("users.sign_up"))

@users_blueprint.post("/sign-up/confirm")
def confirm_register():
    """
        Confirma el registro de un usuario.
        
        args:
            email: email del usuario a confirmar
            username: nobre de usuario
            password: contraseña del usuario
    """
    
    params = request.form
    user = Users.find_user(params['email'])
    
    if user and user.confirmed:
        return redirect(url_for("auth.login"))
    
    if params.__len__() == 1:
        return render_template("users/confirm.html", email=params['email'])
    
    if params['password'] != params['confirm-password']:
        flash("Las contraseñas ingresadas no coinciden", "error")
        return render_template("users/sign_up_confirm.html", email=params['email'])
    
    user = Users.find_user(params['username'])
    
    if user:
        flash("El nombre de usuario ingresado ya existe", "error")
        return render_template("users/sign_up_confirm.html", email=params['email'])
    
    Users.confirm_user(email=params['email'], password=params['password'], username=params['username'])
    
    return redirect(url_for("auth.login"))


@users_blueprint.get("/user_index")
@auth.permission_required("user_index")
def user_index():
    """
        Retorna todos los usuarios.
            
        return:
            JSON response users 200
            
            JSON response error 400
    """
    users = Users.get_users()
    data = [u.to_json() for u in users]
    response = Response(
        response = json.dumps(data),
        status = 200,
        mimetype = 'application/json'
    )
    
    return render_template("users/index.html", users=response.get_json())

@users_blueprint.get("/user-show/<user_id>")
@auth.permission_required("user_show")
def user_profile(user_id):
    user = Users.user_show(user_id)
    if user is None:
        cod = 400
        data = {
            "error": "El usuario no existe"
        }
    else:
        cod = 200
        data = user.to_json()
        
    response = Response(
        response = json.dumps(data),
        status = cod,
        mimetype = 'application/json'
    )
    
    return render_template("users/profile.html", user=response.get_json())
