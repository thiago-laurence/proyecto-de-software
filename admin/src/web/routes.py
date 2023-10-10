from src.web.controllers.system.system import system_blueprint
from src.web.controllers.users.users import users_blueprint
from src.web.api.users import api_users
from src.web.controllers.authentication.auth import auth_blueprint
from src.web.controllers.institutions.institutions import institutions_blueprint
from src.web.controllers.institutions.services import services_blueprint
from src.web.controllers.issues.issues import issues_blueprint
from src.web.controllers.home.home import home_blueprint
from src.web.controllers.api import api_blueprint

def register_blueprints(app):
    """
        Registra todos los blueprints a la app.
    """
    app.register_blueprint(system_blueprint)
    app.register_blueprint(home_blueprint)
    app.register_blueprint(users_blueprint)
    app.register_blueprint(api_users)
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(institutions_blueprint)
    app.register_blueprint(services_blueprint)
    app.register_blueprint(issues_blueprint)
    app.register_blueprint(api_blueprint)