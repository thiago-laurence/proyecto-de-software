from flask import Blueprint
from src.web.controllers.api.logged_user import api_logged_user
from src.web.controllers.api.service import api_services
from src.web.controllers.api.institution import api_institutions
from src.web.controllers.api.auth import api_auth
from src.web.controllers.api.data import api_data
from src.web.controllers.api.contact import api_contact

api_blueprint = Blueprint("api", __name__, url_prefix="/api")

api_blueprint.register_blueprint(api_logged_user)
api_blueprint.register_blueprint(api_services)
api_blueprint.register_blueprint(api_institutions)
api_blueprint.register_blueprint(api_auth)
api_blueprint.register_blueprint(api_data)
api_blueprint.register_blueprint(api_contact)