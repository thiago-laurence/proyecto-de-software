from flask import Blueprint, render_template, request, flash, redirect, url_for
from src.web.controllers.api.logged_user import api_logged_user
from src.web.controllers.api.service import api_services

api_blueprint = Blueprint("api", __name__, url_prefix="/api")

api_blueprint.register_blueprint(api_logged_user)
api_blueprint.register_blueprint(api_services)