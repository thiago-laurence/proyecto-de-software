from flask import Blueprint, render_template, request
from src.core.models import users

users_blueprint = Blueprint("users", __name__, url_prefix="/users")

@users_blueprint.get("/")
def index():
    return render_template("users/index.html", users=users.list_users())