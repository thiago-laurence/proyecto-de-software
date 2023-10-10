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

def get_institutions_by_userID(user_id):
    """
        Devuelte todas las instituciones de un usuario
    """   
    institutions = db.session.query(UserInstitution).filter_by(user_id=user_id).all()
    
    return institutions

def get_role_institution_by_user(user, institution):
    """
        Devuelte el rol de un usuario en una institución
    """   
    role = db.session.query(UserInstitution).filter_by(user_id=user.id, institution_id=institution.id).first()
    
    return role.role

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
    kwargs['email'] = kwargs['email'].lower()
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
        user.username = username.lower()
        user.password = hash.decode('utf-8')
        user.confirmed = True

    db.session.commit()

def find_user(identifier):
    """
        Busca un usuario por email o username y lo retorna.
        
        identify: email o username del usuario.
    """
    identifier = identifier.lower()
    
    return User.query.filter((User.email == identifier) | (User.username == identifier)).first()

def check_auth_user(email, password):
    """
        Valida las credenciales y estado (activo/confirmado) del usuario, y lo retorna si es válido.
    """
    user = find_user(email)
    if user and user.password != None and bcrypt.check_password_hash(user.password, password.encode('utf-8')):
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

def get_first_institution_rol(user):
    """
        Devuelve los ID de la primera institución y rol de un usuario
        return:
            tuple: (institution_id, role_id)
    """
    result = db.session.query(UserInstitution).filter_by(user_id=user.id).first()
    if result is None:
        return None
    return result.institution_id, result.role_id


def user_index():
    """
        Retorna todos los usuarios registrados.
            
        return:
            List [User]
    """
    users = User.query.all()
    
    return users

def user_show(id):
    """
        Busca y retorna un usuario.
        
        args:
            id: identificador del usuario
            
        return:
            Si existe --> User
            
            No existe --> None
    """
    user = User.query.filter(User.id == id).first()
    
    return user
    
    
def user_create(**kwargs):
    """
        Crea un nuevo usuario.
        
        args:
            kwargs: datos del usuario.
            
        return:
            User -> el usuario fue creado.
            
            None -> parametros invalidos.
    """
    kwargs['email'] = kwargs['email'].lower()
    kwargs['username'] = kwargs['username'].lower()
    user = User(**kwargs)
    db.session.add(user)
    db.session.commit()
    
    return user

def user_update(user_id, **kwargs):
    """
        Actualiza la información de un usuario.
        
        args:
            user_id -> id del usuario a modificar.
            
            kwargs -> campos del objeto usuario actualizados.
        
        return:
            User -> el usuario fue actualizado.
            
            None -> el usuario no existe.
    """
    
    kwargs['active'] = True if kwargs['active'] == "True" else False

    user = user_show(user_id)
    if user is None:
        return None
    
    for key, value in kwargs.items():
        setattr(user, key, value)

    db.session.commit()    
    
    return user

def user_destroy(user_id):
    """
        Elimina un usuario del sistema.
    
    args:
        user_id -> ID del usuario a eliminar.
    
    return:
        True -> el usuario existe y fue eliminado con exito.
        
        False -> el usuario no existe.
    """
    
    user = user_show(user_id)
    if user is None:
        return False
        
    db.session.delete(user)
    db.session.commit()
    
    return True