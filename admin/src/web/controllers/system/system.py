from flask import Blueprint, render_template, flash, redirect, url_for
from src.core.models import system as System
from src.web.forms import system_form as Forms
from src.web.helpers import auth

system_blueprint = Blueprint("system", __name__, url_prefix="/system")

@system_blueprint.get("/")
@auth.permission_required("system_show")
def index():
    """
        Redirige a la configuración del sistema
    """
    system = System.system_show()
    form = Forms.SystemForm()
    form.message.data = system.message
    form.info.data = system.info
    return render_template("system/index.html", system=system, form=form)


@system_blueprint.post("/system-update/")
@auth.permission_required("system_update")
def system_update():
    """
        Actualiza la información del sistema.
    """
    form = Forms.SystemForm()
    if form.validate_on_submit():
        form.activate.data = True if form.activate.data == "True" else False
        System.system_update(**form.data)
        flash("La información del sistema ha sido actualizada con exito!", "success")
    
    return redirect(url_for("system.index"))