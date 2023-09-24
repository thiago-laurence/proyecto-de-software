from flask import redirect, url_for, render_template


def not_found_error(e):
    
    kwargs = {
        "error_name": "Error 404 - Not Found",
        "error_description": "La sitio que buscas no existe o no se encuentra disponible",
        "error_code": "404",
        "error_image": "/static/img/error404.png"
    }

    return render_template("error.html", **kwargs), 404

def anautorized_error(e):
    
    kwargs = {
        "error_name": "Error 401 - Unauthorized",
        "error_description": "No tienes permisos para acceder a este sitio",
        "error_code": "401"
    }

    return render_template("login/login.html", **kwargs), 401

def register_error_handlers(app):
    app.register_error_handler(404, not_found_error)
    app.register_error_handler(401, anautorized_error)