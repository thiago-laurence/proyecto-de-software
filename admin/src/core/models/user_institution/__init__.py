from src.core.models.user_institution.user_institution import UserInstitution
from src.core.database import db
from src.core.models import role

def create_user_institution_role(**kwargs):
    """
        Se registra una nueva relación usuario-institución-rol
    """
    
    user_institution = UserInstitution(**kwargs)
    db.session.add(user_institution)
    db.session.commit()
    return user_institution

def check_permission(user_id, institution_id, role_id, permission):
    """
    Comprueba si el usuario tiene permisos en esa institucion
    """

    ui = UserInstitution.query.filter_by(institution_id = institution_id, user_id = user_id, role_id = role_id).first()
    if ui:
        return role.contains_permission(role_id, permission)
    else:
        return False

def remove_user_from_institution(institution_id, user_id):
    """
    Elimina al usuario de una institucion
    """
    ui = UserInstitution.query.filter_by(institution_id = institution_id, user_id = user_id).first()
    if ui:
        db.session.delete(ui)
        db.session.commit()
        return True
    else:
        return False
    
def edit_user_role(institution_id, user_id, role_id):
     """
     Edita el rol de un usuario dentro de una institucion
     """
     ui = UserInstitution.query.filter_by(institution_id = institution_id, user_id = user_id).first()
     if ui:
         ui.role_id = role_id
         db.session.commit()
         return True
     else:
         return False
     
def get_role_id_by_user_and_institution(institution_id, user_id):
    """
    Retorna el id del rol que encuentre en la relacion entre institucion y usuario.
    """
    ui = UserInstitution.query.filter_by(institution_id = institution_id, user_id = user_id).first()
    if ui:
        return ui.role_id
    else:
        return None
    
def get_institution_owner(institution_id):
    """
        retorna el usuario duenio de la institucion
    """
    duenio = role.get_role_by_name("Dueño/a")
    userinstitution = UserInstitution.query.filter_by(institution_id = institution_id, role_id = duenio.id).all()
    users = [user.user for user in userinstitution]
    
    return users


def check_ui(institution_id, user_id):
    """
    Me retorna si el usuario se encuentra en la institucion
    """
    ui = UserInstitution.query.filter_by(institution_id = institution_id, user_id = user_id).first()
    return ui is not None

def check_unique_owner(user_id):
    """
    Me retorna si el usuario es el unico duenio en alguna institucion
    """
    role_owner = role.get_role_by_name("Dueño/a")
    uis = UserInstitution.query.filter_by(user_id=user_id, role_id=role_owner.id).all()
    
    for ui in uis:
        owners = UserInstitution.query.filter_by(institution_id = ui.institution_id, role_id= role_owner.id).all()
        if (len(owners) == 1):
            return True
    return False
