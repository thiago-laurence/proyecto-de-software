from functools import wraps
from flask import session, abort


def is_authenticated(session):
    return session.get("user") is not None

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not is_authenticated(session):
            return abort(401)
        return f(*args, **kwargs)
    return decorated_function

def roles_required(roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not set(roles).intersection(session["user"]["roles"]):
                return abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator