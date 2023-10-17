from flask import Blueprint, render_template, request, redirect, url_for, session
from src.core.models import service_order as ServiceOrders
from src.core.models import institution as Institutions
from src.core.models import user as Users
from src.web.helpers import auth

issues_blueprint = Blueprint("issues", __name__, url_prefix="/issues")


@issues_blueprint.get("/")
@auth.permission_required("request_service_index")
def issue_index():
    """
        Muestra el listado de todos los issues.
    """
    page = request.args.get("page", 1, type=int)
    user_email = request.args.get("user_email", "", type=str)
    status = request.args.get("status", "", type=str)
    type_service = request.args.get("type_service", "", type=str)
    date_from = request.args.get("date_from", "", type=str)
    date_to = request.args.get("date_to", "", type=str)
    
    orders = ServiceOrders.list_page_service_request(session['user']['actual_institution'], 
        page, type_service, status, date_from, date_to, user_email)
    
    type_list = Institutions.index_type_service()
    status_list = ServiceOrders.index_status()
    return render_template("issues/index.html", 
                           issues=orders[0], 
                           page=page, 
                           total_pages=orders[1],
                           type_list=type_list,
                           status_list=status_list,
                           user_email=user_email, 
                           type_service=type_service,
                           status=status, 
                           date_from=date_from, 
                           date_to=date_to)


@issues_blueprint.get("/<issue_id>")
@auth.permission_required("request_service_show")
def issue_show(issue_id):
    """
        Muestra la información de un issue.
    """
    service_order = ServiceOrders.service_request_show(issue_id)
    list_status = ServiceOrders.index_status()

    return render_template("issues/info.html", issue=service_order, list_status=list_status)

@issues_blueprint.get("/<issue_id>/messages")
@auth.permission_required("request_service_show")
def issue_show_messages(issue_id):
    """
        Muestra los mensajes enviados en el issue.
    """
    # issue = Issues.issue_show(issue_id)

    return render_template("issues/messages.html", issue=None)


@issues_blueprint.post("/create-comment")
@auth.permission_required("request_service_update")
def issue_add_comment():
    """
        Agrega un mensaje al issue.
    """
    user = Users.user_show(request.form.get("user"))
    issue = ServiceOrders.get_order_by_id(request.form.get("issue_id"))
    ServiceOrders.add_comment(
        comment = request.form.get("comment"),
        user = user,
        service_order = issue
    )

    return redirect(url_for("issues.issue_show", issue_id=request.form.get("issue_id")))


@issues_blueprint.post("/change-status")
@auth.permission_required("request_service_update")
def issue_change_status():
    """
        Cambia el estado de una solicitud de servicio.
    """
    issue = ServiceOrders.get_order_by_id(request.form.get("issue_id"))
    status = ServiceOrders.get_order_status_by_name(request.form.get("status"))
    ServiceOrders.change_status_order(
        service_order_status = status,
        service_order = issue,
        note = request.form.get("note")
    )

    return redirect(url_for("issues.issue_show", issue_id=request.form.get("issue_id")))