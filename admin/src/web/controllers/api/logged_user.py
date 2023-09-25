from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from src.core.models import users
from src.web.helpers import auth

api_logged_user= Blueprint("logged_user", __name__, url_prefix="/me")


@api_logged_user.get("/profile")
@auth.login_required
def user_info():
    """
    Retorna en formato JSON la información del usuario logueado.
    """
    user = users.find_user(session['user'])
    print(session)
    return user.to_json()