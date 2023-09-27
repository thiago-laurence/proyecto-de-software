from flask import Blueprint, render_template, request, flash, redirect,url_for
from src.core.models import institution
from src.core.models import user

institutions_blueprint = Blueprint("institutions", __name__, url_prefix="/institutions")

@institutions_blueprint.get("/")
def index():
    """"
    Renderiza el template para las instituciones y las muestra.
    """
    return render_template("institutions/index.html", institutions=institution.list_institutions(), users = user.get_users())

@institutions_blueprint.post("/institution-add")
def institution_add():
    """
    Metodo para agregar una nueva institucion
    """

    existe = institution.check_if_institution_exists_by_name(request.form.get("name"))
    if (existe):
         flash("La institución " + request.form.get("name") + " ya se encuentra registrada.", "error")

         return redirect(url_for("institutions.index"))


    print("institution user_id: " + request.form.get("owner"))
    institution.create_institution(
        name= request.form.get("name"),
        info= request.form.get("info"),
        address = request.form.get("address"),
    )
    flash("La institución " + request.form.get("name") + " fue registrada correctamente.", "success")   
    return index()
       