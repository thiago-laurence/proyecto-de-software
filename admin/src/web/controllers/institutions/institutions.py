from flask import Blueprint, render_template, request, flash, redirect,url_for, json, Response
from src.core.models import institution
from src.core.models import user
from src.web.helpers import auth

institutions_blueprint = Blueprint("institutions", __name__, url_prefix="/institutions")

@institutions_blueprint.get("/")
@auth.permission_required("institution_index")
def index():
    """"
    Renderiza el template para las instituciones y las muestra.
    """
    page = request.args.get("page", 1, type=int)
    institutions = institution.list_institutions_paginated(page)
    return render_template("institutions/index.html", institutions=institutions, users = user.get_users(), page=page, total_pages=institution.total_intitutions_pages())


@institutions_blueprint.get("/<institution_id>")
@auth.permission_required("institution_show")
def institution_show(institution_id):
    """"
    Renderiza el template para una institucion especifica y lo muestra y las muestra.
    """
    print("entro al show")

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
       
       
@institutions_blueprint.route("/institutions-delete/<institution_id>", methods=["DELETE"])
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
    
    response = Response(
        response = json.dumps(data),
        status = 200,
        mimetype = 'application/json'
    )
    
    return response.json

@institutions_blueprint.route("/institutions-update/<institution_id>", methods=["PUT"])
@auth.permission_required("institution_update")
def institution_update(institution_id):
    """
    Metodo para editar una institucion
    """
    insti = institution.get_institution_by_id(institution_id)
    existe = institution.get_institution_by_name(request.json['data']['name'])
    print(existe)
    print(request.json['data'])
    if (existe is not None and existe.id != insti.id):
         flash("La institución " + request.json['data']['name'] + " ya se encuentra registrada.", "error")
     
    else:
        kwargs = {
            "name":request.json['data']['name'],
            "info":request.json['data']['info'],
            "address":request.json['data']['address'],
            "web":request.json['data']['web'],
            "social_networks":request.json['data']['social_networks'],
            "phone":request.json['data']['phone']
        }
        if kwargs["name"] == "":
            kwargs["name"] = insti.name
        if kwargs["info"] == "":
            kwargs["info"] = insti.info
        if kwargs["address"] == "":
            kwargs["address"] = insti.address
        if kwargs["web"] == "":
            kwargs["web"] = insti.web
        if kwargs["social_networks"] == "":
            kwargs["social_networks"] = insti.social_networks
        if kwargs["phone"] == "":
            kwargs["phone"] = insti.phone
            
        institution.edit_institution(insti, **kwargs)
        
        flash("La institución " + kwargs["name"] + " fue editada correctamente.", "success")   
        
    data = {
        "url": '/institutions/'+str(institution_id)
    }
    
    response = Response(
        response = json.dumps(data),
        status = 200,
        mimetype = 'application/json'
    )
    
    return response.json