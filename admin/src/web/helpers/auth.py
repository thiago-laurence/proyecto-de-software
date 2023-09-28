from functools import wraps
from flask import session, abort
from src.core.models import role


def is_authenticated(session):
    return session.get("user") is not None

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not is_authenticated(session):
            return abort(401)
        return f(*args, **kwargs)
    return decorated_function

def permission_required(permission):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not role.contains_permission(session["user"]["role"], permission):
                return abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator