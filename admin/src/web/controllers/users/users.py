from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from src.core.models import users
from src.web.helpers import auth
from src.web import mail

users_blueprint = Blueprint("users", __name__, url_prefix="/usuarios")

@users_blueprint.get("/")
@auth.login_required
def index():
    """
        Redirige al listado de usuarios
    """
    return render_template("users/index.html", users=users.get_users())

@users_blueprint.get("/registrarse")
def new_user():
    """
        Redirige al formulario de registro de usuario
    """
    
    return render_template("users/register.html")

@users_blueprint.post("/register")
def register():
    """
        Registra un nuevo usuario obtiendo los datos del formulario
    """
    
    params = request.form
    user = users.find_user(params["email"])
    if user:
        flash("El email ingresado ya está registrado, por favor ingresa otro", "error")
        return redirect(url_for("users.new_user"))
    
    user = users.create_user(email=params["email"], name=params["name"], lastname=params["lastname"])
    body = """
    <p> Bienvenido a CIDEPINT, para completar el registro ingresa al siguiente link: </p>
    <form action="http://localhost:5000/usuarios/confirmar-registro" method="POST">
        <input type="hidden" name="email" value=""" + user.email + """>
        <button type="submit">Confirmar</button>
    </form>
    """
    mail.send_mail("Confirmación de registro", params["email"], body)
    
    flash("Registro parcial exitoso. Se ha enviado un correo de confirmación de registro a la dirección ingresada", "success")
    
    return redirect(url_for("users.new_user"))

@users_blueprint.post("/confirmar-registro")
def confirm_user():
    """
        Confirma el registro de un usuario
    """
    
    params = request.form
    email = params["email"]
    user = users.find_user(email)
    
    if user and user.confirmed:
        return render_template("users/confirm_success.html")
    
    if params.__len__() == 1:
        return render_template("users/confirm.html", email=email)
    
    if params["password"] != params["confirm-password"]:
        flash("Las contraseñas ingresadas no coinciden", "error")
        return render_template("users/confirm.html", email=email)
    
    user = users.find_user(params["username"])
    
    if user:
        flash("El nombre de usuario ingresado ya existe", "error")
        return render_template("users/confirm.html", email=email)
    
    users.confirm_user(email=email, password=params["password"], username=params["username"])
    
    return render_template("users/confirm_success.html")

@users_blueprint.get("/me/profile")
@auth.login_required
def user_profile():
    user = users.find_user(session["user"])
    return render_template("users/profile.html", user=user)