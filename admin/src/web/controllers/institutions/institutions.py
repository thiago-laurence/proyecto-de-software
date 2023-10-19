from flask import Blueprint, render_template, request, flash, redirect,url_for, json, Response
from src.core.models import institution
from src.web.forms.institution_form import InstitutionForm
from src.core.models import user_institution
from src.core.models import user, system, role
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
    institutions = institution.list_institutions_paginated(page)
    
    return render_template("institutions/index.html", institutions=institutions[0], total_pages=institutions[1], page=page, form=form)


@institutions_blueprint.get("/<institution_id>")
@auth.permission_required("institution_show")
def institution_show(institution_id):
    """"
    Renderiza el template para una institucion especifica y lo muestra y las muestra.
    """

    insti = institution.get_institution_by_id(institution_id)
    duenio = user_institution.get_institution_owner(institution_id)
    
    if insti is None:
        flash("La institución no existe.", "error")
        return redirect(url_for("institutions.index"))
    
    return render_template("institutions/institution.html", institution=insti, duenio=duenio)


@institutions_blueprint.post("/institution-add")
@auth.permission_required("institution_create")
def institution_add():
    """
    Metodo para agregar una nueva institucion
    """
    form = InstitutionForm(request.form)
    email_duenio = request.form.get("duenio")

    duenio = user.find_user(email_duenio)
    
    if(form.validate_on_submit()):
        existe = institution.check_if_institution_exists_by_name(form.name.data)
        if (existe):
            flash("La institución " + form.name.data + " ya se encuentra registrada.", "error")
            return redirect(url_for("institutions.index"))
        data = form.data
        insti = institution.create_institution(**data)
        user_institution.create_user_institution_role(user_id=duenio.id, institution_id=insti.id, role_id=2)
        
        flash("La institución " + form.name.data + " fue registrada correctamente.", "success")   
        return index()
    
    total_pages=institution.total_intitutions_pages(system.pages())
    
    errors = form.errors
    field_errors = errors.items()
    
    # Obtén el primer campo con errores (esto es un par clave-valor)
    first_field, first_error = next(iter(field_errors), (None, None))

    if first_error:
        flash(first_error[0], "error")
            
    return redirect(url_for("institutions.index", page=total_pages))
       
       
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
    
    if (existe is not None and existe.id != insti.id):
         flash("La institución " + request.json['data']['name'] + " ya se encuentra registrada.", "error")
     
    else:
        kwargs = {
            "name":request.json['data']['name'],
            "info":request.json['data']['info'],
            "address":request.json['data']['address'],
            "web":request.json['data']['web'],
            "social_networks":request.json['data']['social_networks'],
            "phone":request.json['data']['phone'],
            "is_enabled":request.json['data']['is_enabled'],
            "localization":request.json['data']['localization'],
            "atencion_days":request.json['data']['atencion_days']
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
        if kwargs["localization"] == "":
            kwargs["localization"] = insti.localization
        if kwargs["atencion_days"] == "":
            kwargs["atencion_days"] = insti.atencion_days
        if kwargs["is_enabled"] == "0":
            kwargs["is_enabled"] = True
        else:
            kwargs["is_enabled"] = False


        email_user = request.form.get("duenio")
        user = user.find_user(email_user)
        role_owner = role.get_role_by_name("Dueño/a")


        # si el usuario se encuentra en la institucion, lo pongo como owner, si no, lo asigno a la institucion como owner
        if (user_institution.check_ui(institution_id, user.id)):
            #2 = role owner
            user_institution.edit_user_role(institution_id, user.id, role_owner.id)
        else:
            user_institution.create_user_institution_role(user_id=user.id, institution_id=insti.id, role_id=role_owner.id)

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