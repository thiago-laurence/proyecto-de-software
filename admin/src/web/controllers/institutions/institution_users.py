from flask import Blueprint, render_template, request, redirect,url_for, jsonify
from src.core.models import institution
from src.core.models import user_institution
from src.core.models import user
from src.core.models import role
from src.web.helpers import auth
iu_blueprint = Blueprint("institution_users", __name__, url_prefix="/")

@iu_blueprint.get("/<institution_id>/users")
@auth.login_required
@auth.permission_required("institution_index")
def index(institution_id):
    """"
    Renderiza el template para los usuarios de cada institucion.
    """
    return render_template("institutions/institution_users.html", users=institution.list_users_from_institution(institution_id),institution=institution.get_institution_by_id(institution_id))

@iu_blueprint.post("/<institution_id>/add-user")
def add_user(institution_id):
    """
    Agrega un usuario a la institucion
    """

    
    u = user.find_user(request.form.get("username"))
    i = institution.get_institution_by_id(institution_id)
    r = role.get_role_by_name(request.form.get("role"))
    

    user_institution.create_user_institution_role(
        user = u,
        institution = i,
        role = r
    )

    response = {
        "status": 200,
        "url": '/institutions/'+str(institution_id)
    }

    return render_template("institutions/institution_users.html", users=institution.list_users_from_institution(institution_id),institution=institution.get_institution_by_id(institution_id))
        


@iu_blueprint.get("/<institution_id>/users-not-in")
@auth.login_required
def list_users_not_in_institution(institution_id):
    """
    Retorna en JSON los usuarios que no estan en la institucion.
    """
    users = institution.list_users_not_in_institution(institution_id)
    serialized_users = []
    for user in users:
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

    return jsonify(serialized_users)