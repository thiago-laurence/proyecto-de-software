from flask import render_template


def not_found_error(e):
    
    kwargs = {
        "error_name": "Error 404 - Not Found",
        "error_description": "La sitio que buscas no existe o no se encuentra disponible",
        "error_code": "404",
        "error_image": "/static/img/error404.png"
    }

    return render_template("error.html", **kwargs), 404