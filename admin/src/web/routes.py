from src.web.controllers.users.users import users_blueprint
from src.web.controllers.authentication.auth import auth_blueprint

def register_blueprints(app):
    app.register_blueprint(users_blueprint)
    app.register_blueprint(auth_blueprint)