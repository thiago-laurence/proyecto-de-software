from flask import Blueprint, render_template

auth_blueprint = Blueprint("auth", __name__, url_prefix="/auth")

@auth_blueprint.get("/login")
def index():
    return render_template("login.html")
