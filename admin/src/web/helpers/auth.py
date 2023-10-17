from functools import wraps
from flask import session, abort
from src.core.models import role
from src.core.models import system
from src.core.models import user_institution

def is_authenticated(session):
    """
        Verifica si el usuario está autenticado
        return:
            True si está autenticado, False en caso contrario
    """
    return session.get("user") is not None


def system_available():
    """
        Verifica si el sistema está disponible.
        
        args:
            system: ID del sistema a verificar su disponibilidad. Por defecto 1 para CIDEPINT.
            
        return:
            True -> el sistema está disponible.
            
            Error 503 --> caso contrario.
    """
    
    return system.is_available()


def login_required(f):
    """
        Decorador para verificar si el usuario está autenticado, y el sistema está disponible.
        
        return:
            Si está autenticado, y el sistema está disponible -> ejecuta la función decorada.
            
            En caso de que el sistema no esté disponible y sea SuperAdministrador/a -> ejecuta la funcion decorada.
            
            Si no está autenticado -> retorna un error 401.
            
            Si está autenticado, pero el sistema no está disponible -> retorna un error 503.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not is_authenticated(session):
            return abort(401)

        if not system_available() and session["user"]["role"] != 1:
            return abort(503)
            
        return f(*args, **kwargs)
    return decorated_function


def permission_required(permission):
    """
        Decorador para verificar si el usuario está autenticado, tiene el permiso requerido, 
        el sistema está disponible (en caso de no ser SuperAdministrador/a).
        
        args:
            permission: nombre del permiso requerido
            
        return:
            Si está autenticado, tiene el permiso, y el sistema está disponible -> ejecuta la función decorada.
            En caso de que el sistema no esté disponible, y el usuario no sea SuperAdministrador/a, retorna error 503.
            
            Si no está autenticado -> retorna error 401
            
            Si no tiene el permiso -> retorna error 403.
    """
    def decorator(f):
        @wraps(f)
        @login_required
        def decorated_function(*args, **kwargs):
            id = session['user']['id']
            ins = session['user']['actual_institution']
            role_id = session['user']['role']
            if not user_institution.check_permission(id, ins, role_id, permission):
                return abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def render_layout(role_id):
    """
        Renderiza el layout de la aplicación acorde al rol del usuario.
        args:
            role_id: id del rol del usuario.
        return:
            layout: nombre del layout.
    """
    layout = {
        0: "layout-user.html",
        1: "layout-root.html",
        2: "layout-owner.html",
        3: "layout-admin.html",
        4: "layout-operator.html",
    }
    
    return layout[role_id]