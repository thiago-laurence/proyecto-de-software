from flask import Blueprint, render_template, request, flash, redirect,url_for, jsonify
from src.core.models import institution
from src.core.models import user
from src.web.helpers import auth

from src.web.controllers.institutions.institution_users import iu_blueprint

institutions_blueprint = Blueprint("institutions", __name__, url_prefix="/institutions")

institutions_blueprint.register_blueprint(iu_blueprint)

@institutions_blueprint.get("/")
@auth.permission_required("institution_index")
def index():
    """"
    Renderiza el template para las instituciones y las muestra.
    """
    return render_template("institutions/index.html", institutions=institution.list_institutions(), users = user.get_users())


@institutions_blueprint.get("/<institution_id>")
@auth.permission_required("institution_show")
def institution_show(institution_id):
    """"
    Renderiza el template para una institucion especifica y lo muestra y las muestra.
    """
    insti = institution.get_institution_by_id(institution_id)
    if insti is None:
        flash("La institución no existe.", "error")
        return redirect(url_for("institutions.index"))
    
    return render_template("institutions/institution.html", institution=insti)


@institutions_blueprint.post("/institution-add")
@auth.permission_required("institution_create")
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
        web = request.form.get("web"),
        social_networks = request.form.get("social_networks"),
        phone = request.form.get("phone")
    )
    flash("La institución " + request.form.get("name") + " fue registrada correctamente.", "success")   
    return index()
       
       
@institutions_blueprint.route("/institution-delete/<institution_id>", methods=["DELETE"])
@auth.permission_required("institution_destroy")
def intitution_delete(institution_id):
    """
    Metodo para eliminar una institucion
    """
    insti = institution.get_institution_by_id(institution_id)

    institution.delete_institution(insti)
    
    flash("La institución " + insti.name + " fue eliminada correctamente.", "success")
    
    data = {
        "url": '/institutions'
    }
    
    return jsonify(data)

@institutions_blueprint.route("/institution-edit/<institution_id>", methods=["PUT"])
@auth.permission_required("institution_update")
def institution_update(institution_id):
    """
    Metodo para editar una institucion
    """
    insti = institution.get_institution_by_id(institution_id)
    existe = institution.get_institution_by_name(request.json['name'])
    
    if (existe is not None and existe.id != insti.id):
         flash("La institución " + request.json['name'] + " ya se encuentra registrada.", "error")
     
    else:
        kwargs = {
            "name":request.json['name'],
            "info":request.json['info'],
            "adress":request.json['adress'],
            "web":request.json['web'],
            "social_networks":request.json['social_networks'],
            "phone":request.json['phone']
        }
        if kwargs["name"] == "":
            kwargs["name"] = insti.name
        if kwargs["info"] == "":
            kwargs["info"] = insti.info
        if kwargs["adress"] == "":
            kwargs["adress"] = insti.address
        if kwargs["web"] == "":
            kwargs["web"] = insti.web
        if kwargs["social_networks"] == "":
            kwargs["social_networks"] = insti.social_networks
        if kwargs["phone"] == "":
            kwargs["phone"] = insti.phone
            
        institution.edit_institution(insti, **kwargs)
        
        flash("La institución " + request.json['name']+ " fue editada correctamente.", "success")   
        
    data = {
        "url": '/institutions/'+str(institution_id)
    }
    
    return jsonify(data)