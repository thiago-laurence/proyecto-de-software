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


@issues_blueprint.get("/<issue_id>")
@auth.permission_required("request_service_show")
def issue_show(issue_id):
    """
        Muestra la información de un issue.
    """
    # issue = Issues.issue_show(issue_id)

    return render_template("issues/info.html", issue=None)

@issues_blueprint.get("/<issue_id>/messages")
@auth.permission_required("request_service_show")
def issue_show_messages(issue_id):
    """
        Muestra los mensajes enviados en el issue.
    """
    # issue = Issues.issue_show(issue_id)

    return render_template("issues/messages.html", issue=None)