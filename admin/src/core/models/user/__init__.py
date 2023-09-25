from src.core.models.user.user import User
from src.core.models.user_institution.user_institution import UserInstitution
from src.core.database import db
from src.core.bcrypt import bcrypt

def get_users():
    """
        Retorna todos los usuarios
    """   
    users = User.query.all()
    return users

def get_institutions_by_user(user):
    """
        Devuelte todas las instituciones de un usuario
    """   
    user.institutions = db.session.query(UserInstitution).filter_by(user_id=user.id).all()
    
    return user.institutions


def assign_institution_and_role(user, role_institution_list):
    """
        Asigna un rol a un usuario en una institución
    """
    user.institutions.extend(role_institution_list)
    db.session.add(user)
    db.session.commit()

def create_user(**kwargs):
    """
        Se registra un nuevo usuario
    """
    
    user = User(**kwargs)
    db.session.add(user)
    db.session.commit()
    return user

def confirm_user(email, username, password):
    """
        Confirma el registro de un usuario.
        Actualiza su username, password, y estado de confirmación
    """
    hash = bcrypt.generate_password_hash(password.encode('utf-8'))
    user = find_user(email)
    if user:
        user.username = username
        user.password = hash.decode('utf-8')
        user.confirmed = True
    
    db.session.commit()

def find_user(identifier):
    """
        Busca un usuario por email o username y lo retorna.
        
        identify: email o username del usuario.
    """
    
    return User.query.filter((User.email == identifier) | (User.username == identifier)).first()

def check_auth_user(email, password):
    """
        Valida las credenciales y estado (activo/confirmado) del usuario, y lo retorna si es válido.
    """
    user = find_user(email)
    if user and bcrypt.check_password_hash(user.password, password.encode('utf-8')):
        return user
    else:
        return None
    
def check_state_user(user):
    """
        Valida el estado (activo/confirmado) del usuario.
        
        return:
            True: si el usuario está activo y confirmado.
            False: caso contrario.
    """
    if user.confirmed and user.active:
        return True
    else:
        return False