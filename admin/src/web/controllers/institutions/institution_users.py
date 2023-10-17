from flask import Blueprint, render_template, request, redirect,url_for, jsonify, flash, session, abort
from src.core.models import institution
from src.core.models import user_institution
from src.core.models import user
from src.core.models import role
from src.web.helpers import auth
iu_blueprint = Blueprint("institution_users", __name__, url_prefix="/")

@iu_blueprint.get("/<institution_id>/users")
@auth.permission_required("ui_index")
def index(institution_id):
    """"
    Renderiza el template para los usuarios de cada institucion.
    """
    page = request.args.get("page", 1, type=int)
    query = request.args.get("query", "", type=str)
    active = request.args.get("active", "", type=str)

    ins = session['user']['actual_institution']
    
    if (str(institution_id) == str(ins)):
        if active != "":
            active = True if active == "True" else False

        users = institution.list_users_from_institution(institution_id,page, query, active)
        
        i = institution.get_institution_by_id(institution_id)
        return render_template("institutions/institution_users.html", institution=i,users=users[0], total_pages=users[1], page=page, query=query, active=active)
    else:
        return abort(404)

@iu_blueprint.post("/<institution_id>/add-user")
@auth.permission_required("ui_create")
def add_user(institution_id): 
    """
    Agrega un usuario a la institucion
    """

    
    u = user.find_user(request.form.get("username"))
    i = institution.get_institution_by_id(institution_id)
    r = role.get_role_by_name(request.form.get("role"))
    
    if (u is None) or (i is None) or (r is None):
        flash("Por favor, seleccione un usuario", "error")
    else:
        user_institution.create_user_institution_role(
            user = u,
            institution = i,
            role = r
        )

        response = {
            "status": 200,
            "url": '/institutions/'+str(institution_id)
        }

    return redirect(url_for('.index', institution_id = institution_id))


@iu_blueprint.post("/<institution_id>/edit-user")
@auth.permission_required("ui_update")
def edit_user_role(institution_id): 
    """
    Edito el rol de un usuario de la institucion
    """

    
    u = user.find_user(request.form.get("user-name"))
    i = institution.get_institution_by_id(institution_id)
    r = role.get_role_by_name(request.form.get("edit-role"))
    
    if (u is None) or (i is None) or (r is None):
        flash("Por favor, seleccione un usuario", "error")
    else:
        user_institution.edit_user_role(i.id, u.id, r.id)

    return redirect(url_for('.index', institution_id = institution_id))

@iu_blueprint.route("/<institution_id>/remove-user/<user_id>", methods=['DELETE'])
@auth.permission_required('ui_destroy')
def remove_user_from_institution(institution_id, user_id):
    res = user_institution.remove_user_from_institution(institution_id, user_id)
    data = {
            'url': '/institutions/' + str(institution_id) + '/users'
        }
    if res:
        flash("El usuario fue eliminado correctamente", "success")
    else:
        flash("El usuario no pudo ser eliminado", "error")
    return jsonify(data)
    


@iu_blueprint.get("/<institution_id>/users-not-in")
@auth.permission_required('ui_index')
def list_users_not_in_institution(institution_id):
    """
    Retorna en JSON los usuarios que no estan en la institucion.
    """
    page = request.args.get("page", 1, type=int)
    query = request.args.get("q", "", type=str)
    active = request.args.get("active", "", type=str)

    if (active != ""):
        active = True if active == 'true' else False
    
    users = institution.list_users_not_in_institution(institution_id, query, page, active)
    serialized_users = []
    for user in users[0]:
        serialized_user = {
            "id": user.id,
            "email": user.email,
            "username": user.username,
            "name": user.name,
            "lastname": user.lastname,
            "active": user.active,
            "confirmed": user.confirmed,
        }
        serialized_users.append(serialized_user)
    
    data = {
        "users": serialized_users,
        "page": page,
        "query": query,
        "total_pages": users[1],
        "active": active
    }
    
    # return render_template("users/index.html", form_create=form_create, users=users[0], total_pages=users[1], page=page, query=query, active=active)
    return jsonify(data)