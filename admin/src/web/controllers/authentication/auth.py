from flask import Blueprint, render_template, request, flash, redirect, url_for, session, Response, jsonify
from src.core.models import user as Users
from src.web.forms import login_form as Forms
from src.web.helpers import auth
from src.web.oauth import oauth as OAuth
from src.core.models import user_institution

auth_blueprint = Blueprint("auth", __name__, url_prefix="/login")

@auth_blueprint.get("/")
def login():
    return render_template("login/login.html", form=Forms.LoginForm())

@auth_blueprint.post("/authenticate")
def authenticate():
    """
        Autenticacion de usuario a traves de login normal mediante username/email y contraseña.
    """    
    params = request.form
    user = Users.check_auth_user(params["email_username"], params["password"])
    
    if not user:
        flash("Email/Nombre de usuario o contraseña incorrectos", "error")
        return redirect(url_for("auth.login"))
        
    return redirect(url_for("auth.init_sesion_user", email_username=params["email_username"]))

@auth_blueprint.post("/update-actual-institution")
def update_actual_institution():
    """
        Actualiza la institucion actual del usuario logueado
    """
    
    id = request.json['institution_id']
    session['user']['actual_institution'] = id
    session['user']['layout'] = auth.render_layout(user_institution.get_role_id_by_user_and_institution(id, session['user']['id']))
    data = {
        "url": url_for('home.index')
    }
    return jsonify(data)

@auth_blueprint.get("/logout")
def logout():
    """
        Cierre la sesión del usuario
    """
    if session.get("user"):
        del session["user"]
        session.clear()
    else:
        flash("No existe una sesión iniciada", "info")
        
    return redirect(url_for("auth.login"))

@auth_blueprint.get("/init-sesion-user/<email_username>")
def init_sesion_user(email_username):
    """
        Inicializa la sesion del usuario
    """
    user = Users.find_user(email_username)
    
    if user:
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
    else:
        flash("El usuario no está registrado", "error")
        return redirect(url_for("auth.login"))


@auth_blueprint.route("/login-google")
def login_google():
    """
        Autenticacion de usuario a traves de google cloud
    """
    redirect_uri = url_for('auth.login_google_callback', _external=True)
    
    return OAuth.google.authorize_redirect(redirect_uri)

@auth_blueprint.route("/google-callback")
def login_google_callback():
    """
        URI de callback de google cloud
    """
    token = OAuth.google.authorize_access_token()
    user = token['userinfo']

    return redirect(url_for("auth.init_sesion_user", email_username=user["email"]))