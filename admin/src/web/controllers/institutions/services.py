from flask import Blueprint, render_template, request, flash, redirect,url_for,json, Response
from src.web.forms.service_form import ServiceCreateForm
from src.core.models import institution
from src.web.helpers import auth


services_blueprint = Blueprint("services", __name__, url_prefix="/services")


@services_blueprint.get("/<institution_id>")
@auth.permission_required("service_index")
def index(institution_id):
    """"
    Renderiza el template para los servicios y los muestra.
    """
    form = ServiceCreateForm(request.form)
    
    page = request.args.get('page', 1, type=int)
    total_pages = institution.total_services_pages(institution_id)
    services = institution.list_services_by_intitution_paginated(page,institution_id)
    insti = institution.get_institution_by_id(institution_id)
    
    if (page <= total_pages and page > 0):
        return render_template("services/index.html", services=services,institution=insti, page=page, form=form)
    else:
        return redirect(url_for("services.index",institution_id=insti.id, page=total_pages))



@services_blueprint.post("/service-add/<institution_id>")
@auth.permission_required("service_create")
def service_add(institution_id):
    """
    Metodo para agregar un nuevo servicio
    """
    form = ServiceCreateForm(request.form)
    
    if(form.validate_on_submit()):
        service = institution.get_service_by_name_and_institution(form.name.data,institution_id)
        
        existe = service is not None
        
        if existe:
            flash("El servicio " + form.name.data + " ya se encuentra registrado para esta institucion.", "error")
        
        else:     
            insti = institution.get_institution_by_id(institution_id)
            institution.assign_service(
                insti,
                institution.create_service(
                    name= form.name.data,
                    info= form.info.data,
                    type= form.type.data,
                    key_words = form.key_words.data,
                )
            )
            flash("El servicio " + form.name.data + " fue registrado correctamente.", "success")   
        return redirect(url_for("services.index",institution_id=institution_id))
    
    return render_template("services/index.html", form=form)
        

@services_blueprint.route("/services-delete/<service_id>", methods=["DELETE"])
@auth.permission_required("service_destroy")
def service_delete(service_id):
    """
    Metodo para eliminar un servicio
    """
    service = institution.get_service_by_id(service_id)
    institution_id = service.institution_id

    institution.delete_service(service)
    
    flash("El servicio " + service.name + " fue eliminado correctamente.", "success")
    
    data = {
        "url": '/services/'+str(institution_id)
    }
    
    response = Response(
        response = json.dumps(data),
        status = 200,
        mimetype = 'application/json'
    )
    
    return response.json


@services_blueprint.put("/services-update/<service_id>")
@auth.permission_required("service_update")
def service_edit(service_id):
    """
    Metodo para editar un servicio
    """
    service = institution.get_service_by_id(service_id)
    
    check = institution.get_service_by_name_and_institution(request.json['data']['name'],service.institution_id)
    
    existe = check is not None and check.id != service.id
    
    if existe:
        flash("El servicio " + request.json['data']['name'] + " ya se encuentra registrado para esta institucion.", "error")
    
    else:
        kwargs = {
            "name": request.json['data']['name'],
            "info": request.json['data']['info'],
            "type": request.json['data']['type'],
            "key_words": request.json['data']['key_words'],
        }

        if kwargs["name"] == "":
            kwargs["name"] = service.name
        if kwargs["info"] == "":
            kwargs["info"] = service.info
        if kwargs["type"] == "":
            kwargs["type"] = service.type
        if kwargs["key_words"] == "":
            kwargs["key_words"] = service.key_words
            
        institution.edit_service(service, **kwargs)
        flash("El servicio " + kwargs["name"] + " se edito con exito.", "success")
    
    data = {
        "url" : '/services/'+str(service.institution_id)
    }
    
    response = Response(
        response = json.dumps(data),
        status = 200,
        mimetype = 'application/json'
    )
    
    return response.json