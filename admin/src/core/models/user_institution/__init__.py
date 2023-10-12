from src.core.models.user_institution.user_institution import UserInstitution
from src.core.database import db

def create_user_institution_role(**kwargs):
    """
        Se registra una nueva relación usuario-institución-rol
    """
    
    user_institution = UserInstitution(**kwargs)
    db.session.add(user_institution)
    db.session.commit()
    return user_institution

def remove_user_from_institution(institution_id, user_id):
    ui = UserInstitution.query.filter_by(institution_id = institution_id, user_id = user_id).first()
    if ui:
        db.session.delete(ui)
        db.session.commit()
        return True
    else:
        return False