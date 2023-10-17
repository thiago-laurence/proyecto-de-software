from flask import Blueprint, render_template, request, flash, redirect, url_for, session, Response, jsonify
from src.core.models import user as Users
from src.web.forms import login_form as Forms
from src.web.helpers import auth
from src.core.models import user_institution

auth_blueprint = Blueprint("auth", __name__, url_prefix="/login")

@auth_blueprint.get("/")
def login():
    return render_template("login/login.html", form=Forms.LoginForm())

@auth_blueprint.post("/authenticate")
def authenticate():    
    params = request.form
    user = Users.check_auth_user(params["email_username"], params["password"])
    
    if not user:
        flash("Email/Nombre de usuario o contraseña incorrectos", "error")
        return redirect(url_for("auth.login"))
    
    if not Users.check_state_user(user):
        flash("El usuario no está activo o no está confirmado", "error")
        return redirect(url_for("auth.login"))
        
    institution_role = Users.get_first_institution_rol(user)
    if institution_role is None:
        session["user"] = {
            "id": user.id,
            "email": user.email,
            "username": user.username,
            "institutions": [],
            "actual_institution": None,
            "role": None,
            "layout": auth.render_layout(0)
        }
    else:   
        session["user"] = {
            "id": user.id,
            "email": user.email,
            "username": user.username,
            "institutions": [i.institution for i in Users.get_institutions_by_userID(user.id)],
            "actual_institution": institution_role[0],
            "role": institution_role[1],
            "layout": auth.render_layout(institution_role[1])
        }
    
    return redirect(url_for("home.index"))

@auth_blueprint.post("/update-actual-institution")
def update_actual_institution():
    id = request.json['institution_id']
    session['user']['actual_institution'] = id
    session['user']['layout'] = auth.render_layout(user_institution.get_role_id_by_user_and_institution(id, session['user']['id']))
    data = {
        "url": url_for('home.index')
    }
    return jsonify(data)

@auth_blueprint.get("/logout")
def logout():
    if session.get("user"):
        del session["user"]
        session.clear()
    else:
        flash("No existe una sesión iniciada", "info")
        
    return redirect(url_for("auth.login"))