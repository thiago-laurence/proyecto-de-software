from flask import Blueprint, render_template
# from src.core.models import issue as Issues
from src.web.helpers import auth

issues_blueprint = Blueprint("issues", __name__, url_prefix="/issues")


@issues_blueprint.get("/")
@auth.permission_required("request_service_index")
def issue_index():
    """
        Muestra el listado de todos los issues.
    """
    # issues = Issues.issues_index()
    
    return render_template("issues/index.html", page=1, query="", active="", total_pages=1)