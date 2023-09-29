from functools import wraps
from flask import session, abort
from src.core.models import role
from src.core.models import system


def is_authenticated(session):
    """
        Verifica si el usuario está autenticado
        return:
            True si está autenticado, False en caso contrario
    """
    return session.get("user") is not None


def is_available(system_name):
    """
        Verifica si el sistema está disponible.
        args:
            system: nombre del sistema a verificar su disponibilidad.
        return:
            True si está disponible.
            False en caso contrario.
    """
    return system.is_available(system_name)


def system_available(system="CIDEPINT"):
    """
        Verifica si el sistema está disponible.
        args:
            system: nombre del sistema a verificar su disponibilidad. Por defecto CINCEPINT.
        return:
            True si está disponible.
            Error 503 en caso contrario.
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not is_available(system):
                return abort(503)
            return f(*args, **kwargs)
        return decorated_function
    return decorator


def login_required(f):
    """
        Decorador para verificar si el usuario está autenticado.
        return:
            Si está autenticado, ejecuta la función decorada.
            Si no está autenticado, retorna un error 401.
    """
    @wraps(f)
    @system_available()
    def decorated_function(*args, **kwargs):
        if not is_authenticated(session):
            return abort(401)
        return f(*args, **kwargs)
    return decorated_function

def session_required(f):
    """
        Decorador para verificar si el usuario está autenticado.
        return:
            Si está autenticado, ejecuta la función decorada.
            Si no está autenticado, retorna un error 401.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not is_authenticated(session):
            return abort(401)
        return f(*args, **kwargs)
    return decorated_function


def permission_required(permission):
    """
        Decorador para verificar si el usuario está autenticado y tiene el permiso requerido.
        args:
            permission: nombre del permiso requerido
        return:
            Si está autenticado y tiene el permiso, ejecuta la función decorada.
            Si no está autenticado retorna error 401
            Si no tiene el permiso retorna error 403.
    """
    def decorator(f):
        @wraps(f)
        @login_required
        def decorated_function(*args, **kwargs):
            if not role.contains_permission(session["user"]["role"], permission):
                return abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator