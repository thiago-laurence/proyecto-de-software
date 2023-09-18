from flask import Flask
from flask import render_template

from src.core import database

from src.web import error


def create_app(env="development", static_folder="../../static"):
    app = Flask(__name__, static_folder=static_folder)

    #Configuraciones
    database.init_app(app)

    #Endpoints
    @app.get("/")
    def home():
        return render_template("home.html")

    app.register_error_handler(404, error.not_found_error)

    #Comandos
    @app.cli.command(name=resetdb)
    def resetdb():
        database.reset_db()

    return app