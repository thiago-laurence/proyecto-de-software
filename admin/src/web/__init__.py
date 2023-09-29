# Import built-in modules
import logging
# Import third-party modules
from flask import Flask, redirect, url_for
from flask_session import Session
# Import local modules
from src.core import models
from src.core import database
from src.web import error
from src.web.config import config
from src.web import routes
from src.web.helpers import auth
from src.web import mail
from src.core import seeds

logging.basicConfig()
logging.getLogger("sqlalchemy.engine").setLevel(logging.ERROR)
session = Session()

def create_app(env="development", static_folder="../../static"):
    app = Flask(__name__, static_folder=static_folder)
    
    app.config.from_object(config[env])

    #Configuraciones
    app.config.from_object(config[env])
    mail.init_app(app)
    session.init_app(app)
    database.init_app(app)
    error.register_error_handlers(app)
    routes.register_blueprints(app)
    app.jinja_env.globals.update(is_authenticated=auth.is_authenticated)
    
    #Endpoints
    @app.get("/")
    def home():
        return redirect(url_for("home.index"))
    
    #Comandos
    @app.cli.command(name="resetdb")
    def resetdb():
        database.reset_db()
        
    @app.cli.command(name="seedsdb")
    def seedsdb():
        seeds.run()

    return app