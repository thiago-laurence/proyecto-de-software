from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from src.core.models import user as Users

auth_blueprint = Blueprint("auth", __name__, url_prefix="/login")

@auth_blueprint.get("/")
def login():
    return render_template("login/login.html")

@auth_blueprint.post("/authenticate")
def authenticate():
    params = request.form
    user = Users.check_auth_user(params["email"], params["password"])
    
    if not user:
        flash("Email/Nombre de usuario o contraseña incorrectos", "error")
        return redirect(url_for("auth.login"))
    
    if not Users.check_state_user(user):
        flash("El usuario no está activo o no está confirmado", "error")
        return redirect(url_for("auth.login"))
        
    first_institution = Users.get_institutions_by_user(user)[0]
    session["user"] = {
        "email": user.email,
        "username": user.username,
        "actual_institution": first_institution.institution_id,
        "institutions": [ui.institution for ui in user.institutions],
        "roles": [ui.role.name for ui in user.institutions]
    } 
    flash("La sesión inicio correctamente", "success")
    return redirect(url_for("home"))

@auth_blueprint.post("/update-actual-institution")
def update_actual_institution():
    id = request.json['institution_id']
    session['user']['actual_institution'] = id
    print(session['user'])
    return redirect(url_for("home"))

@auth_blueprint.get("/logout")
def logout():
    if session.get("user"):
        del session["user"]
        session.clear()
    else:
        flash("No existe una sesión iniciada", "info")
        
    return redirect(url_for("auth.login"))