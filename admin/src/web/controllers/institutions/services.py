from flask import Blueprint, render_template, request, flash, redirect,url_for
from src.core.models import institution
from src.core.models import users

services_blueprint = Blueprint("services", __name__, url_prefix="/services")

@services_blueprint.get("/<institution_id>")
def index(institution_id):
    """"
    Renderiza el template para los servicios y los muestra.
    """
    return render_template("services/index.html", services=institution.list_services_by_institution(institution_id),institution=institution.get_institution_by_id(institution_id))


@services_blueprint.post("/service-add/<institution_id>")
def service_add(institution_id):
    """
    Metodo para agregar un nuevo servicio
    """
    
    #print("institution: " + insti.name)
    existe = institution.check_if_service_exists_by_name_create(institution_id, request.form.get("name"))
    
    if existe:
        flash("El servicio " + request.form.get("name") + " ya se encuentra registrado para esta institucion.", "error")
    
    else:     
        insti = institution.get_institution_by_id(institution_id)
        institution.assign_service(
            insti,
            institution.create_service(
                name= request.form.get("name"),
                info= request.form.get("info"),
                type= request.form.get("type"),
                key_words = request.form.get("key_words"),
            )
        )
        flash("El servicio " + request.form.get("name") + " fue registrado correctamente.", "success")   
    return redirect(url_for("services.index",institution_id=institution_id))
        
    
@services_blueprint.route("/service-delete/<service_id>")
def service_delete(service_id):
    """
    Metodo para eliminar un servicio
    """
    service = institution.get_service_by_id(service_id)
    institution_id = service.institution_id

    institution.delete_service(service)
    
    flash("El servicio " + service.name + " fue eliminado correctamente.", "success")   
    return redirect(url_for("services.index",institution_id=institution_id))


@services_blueprint.get("/edit/<service_id>")
def access_service_edit(service_id):
    """
    Metodo para acceder a la edicion de un servicio
    """
    service = institution.get_service_by_id(service_id)
    print("nombre del servicio: ",service.name)
    
    return render_template("services/edit.html",service=service)

@services_blueprint.route("/service-edit/<service_id>", methods=["POST"])
def service_edit(service_id):
    """
    Metodo para editar un servicio
    """
    service = institution.get_service_by_id(service_id)
    
    existe = institution.check_if_service_exists_by_name_update(service.institution_id, request.form.get("name"),service_id)
    
    if existe:
        flash("El servicio " + service.name + " ya se encuentra registrado para esta institucion.", "error")
        return redirect(url_for("services.index",institution_id=service.institution_id))
    
    else:
        kwargs = {
            "name": request.form.get("name"),
            "info": request.form.get("info"),
            "type": request.form.get("type"),
            "key_words": request.form.get("key_words"),
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
        flash("El servicio " + request.form.get("name") + " se edito con exito.", "success")
    
    return redirect(url_for("services.index",institution_id=service.institution_id))