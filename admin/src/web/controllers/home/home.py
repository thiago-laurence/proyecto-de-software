from flask import Blueprint, render_template, request, flash, redirect, url_for
from src.web.helpers import auth

home_blueprint = Blueprint("home", __name__, url_prefix="/home")

@home_blueprint.get("/")
@auth.login_required
def index():
    """
        Redirige a la página de inicio de la administración
    """
    return render_template("home.html")