from flask import Blueprint, render_template, request, url_for, session
from src.core.models import system as System
from src.web.helpers import auth

system_blueprint = Blueprint("system", __name__, url_prefix="/system")

@system_blueprint.get("/")
@auth.login_required
@auth.permission_required("system_show")
def index():
    """
        Redirige a la configuración del sistema
    """
    sys = System.system_show("CINDEPINT")
    return render_template("system/index.html", system=sys.to_json())