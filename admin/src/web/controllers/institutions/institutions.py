from flask import Blueprint, render_template, request, flash, redirect,url_for, json, Response
from src.core.models import institution
from src.web.forms.institution_form import InstitutionForm
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
    form = InstitutionForm(request.form)
    
    page = request.args.get("page", 1, type=int)
    total_pages=institution.total_intitutions_pages()
    institutions = institution.list_institutions_paginated(page)
    if(page <= total_pages and page > 0):
        return render_template("institutions/index.html", institutions=institutions, users = user.get_users(), page=page, form=form)
    else:
        return redirect(url_for("institutions.index", page=total_pages))


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
    form = InstitutionForm(request.form)
    
    if(form.validate_on_submit()):
        existe = institution.check_if_institution_exists_by_name(form.name.data)
        if (existe):
            flash("La institución " + form.name.data + " ya se encuentra registrada.", "error")
            return redirect(url_for("institutions.index"))

        institution.create_institution(
            name= form.name.data,
            info= form.info.data,
            address = form.address.data,
            web = form.web.data,
            social_networks = form.social_networks.data,
            phone = form.phone.data
        )
        flash("La institución " + form.name.data + " fue registrada correctamente.", "success")   
        return index()
    
    return render_template("institutions/index.html", form=form)
       
       
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