from src.web.controllers.users.users import users_blueprint
from src.web.controllers.authentication.auth import auth_blueprint
from src.web.controllers.institutions.institutions import institutions_blueprint

def register_blueprints(app):
    """
    Registra todos los blueprints a la app.
    """
    app.register_blueprint(users_blueprint)
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(institutions_blueprint)