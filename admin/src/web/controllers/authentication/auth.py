from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from src.core.models import users

auth_blueprint = Blueprint("auth", __name__, url_prefix="/login")

@auth_blueprint.get("/")
def login():
    return render_template("login/login.html")

@auth_blueprint.post("/authenticate")
def authenticate():
    params = request.form
    user = users.check_auth_user(params["email"], params["password"])
    
    if not user:
        flash("Email/Nombre de usuario o contraseña incorrectos", "error")
        return redirect(url_for("auth.login"))
    
    if not users.check_state_user(user):
        flash("El usuario no está activo o no está confirmado", "error")
        return redirect(url_for("auth.login"))
    
    session["user"] = user.email
    session["username"] = user.username
    
    flash("La sesión inicio correctamente", "success")
    return redirect(url_for("home"))

@auth_blueprint.get("/logout")
def logout():
    if session.get("user"):
        del session["user"]
        session.clear()
    else:
        flash("No existe una sesión iniciada", "info")
        
    return redirect(url_for("auth.login"))