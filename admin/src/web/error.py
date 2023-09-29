from flask import redirect, url_for, render_template


def not_found_error(e):
    
    kwargs = {
        "error_name": "Error 404 - Not Found",
        "error_description": "La sitio que buscas no existe",
        "error_code": "404",
        "error_image": "/static/img/error404.png"
    }

    return render_template("error.html", **kwargs), 404

def anautorized_error(e):
    
    kwargs = {
        "error_name": "Error 401 - Unauthorized",
        "error_description": "No posee credenciales válidas para acceder a este sitio",
        "error_code": "401"
    }

    return render_template("login/login.html", **kwargs), 401

def forbidden_error(e):
    
    kwargs = {
        "error_name": "Error 403 - Forbidden",
        "error_description": "No tienes permisos para acceder a este sitio",
        "error_code": "403",
        "error_image": "/static/img/error403.jpg"
    }

    return render_template("error.html", **kwargs), 403

def unavailable_error(e):
    
    kwargs = {
        "error_name": "Error 503 - Unavailable",
        "error_description": "El sistema se encuentra en mantenimiento y no está disponible por el momento",
        "error_code": "503",
        "error_image": "/static/img/error503.jpg"
    }

    return render_template("error.html", **kwargs), 503

def register_error_handlers(app):
    app.register_error_handler(404, not_found_error)
    app.register_error_handler(401, anautorized_error)
    app.register_error_handler(403, forbidden_error)
    app.register_error_handler(503, unavailable_error)