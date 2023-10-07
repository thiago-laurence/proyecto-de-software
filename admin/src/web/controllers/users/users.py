from flask import Blueprint, render_template, request, flash, redirect, url_for, session, jsonify
from src.core.models import user as Users
from core.forms import user_form as Forms
from src.web.helpers import auth
from src.web import mail

users_blueprint = Blueprint("users", __name__, url_prefix="/users")

@users_blueprint.get("/sing-up")
def sign_up():
    """
        Redirige al formulario de registro de usuario.
    """
    form = Forms.UserRegisterForm()
    return render_template("users/sign_up.html", form=form)


@users_blueprint.post("/sign-up/register")
def register():
    """
        Registra un nuevo usuario (de forma parcial) obtiendo los datos del formulario.
        args:
            email: email del usuario a registrar.
            name: nombre del usuario a registrar.
            lastname: apellido del usuario a registrar.
    """

    form = Forms.UserRegisterForm()
    user = Users.find_user(form.email.data)
    if user:
        flash("El email ingresado ya está registrado, por favor ingresa otro", "error")
        return render_template("users/sign_up.html", form=form)
    
    user = Users.create_user(**form.data)
    url = request.host_url + "/users/sign-up/confirm"
    body = """
        <p> Bienvenido a CIDEPINT, para completar el registro ingresa al siguiente link: </p>
        <form action=""" + url + """ method="POST">
            <input type="hidden" name="email" value=""" + user.email + """>
            <button type="submit">Confirmar</button>
        </form>
    """
    
    mail.send_mail("Confirmación de registro", form.email.data, body)
    
    flash("Registro parcial exitoso. Se ha enviado un correo de confirmación de registro a la dirección ingresada", "success")
    
    return render_template("users/sign_up.html", form=form)


@users_blueprint.post("/sign-up/confirm")
def confirm_register():
    """
        Confirma el registro de un usuario.
        
        args:
            email: email del usuario a confirmar
            username: nobre de usuario
            password: contraseña del usuario
    """
    
    form = Forms.UserConfirmRegisterForm()
    user = Users.find_user(form.email.data)
    
    if user and user.confirmed:
        return redirect(url_for("auth.login"))
    
    if form.validate_on_submit():
       
        if Users.exists_user(form.username.data):
            flash("El nombre de usuario ingresado ya existe, por favor ingresa otro", "error")
            return render_template("users/sign_up_confirm.html", form=form)
        
        Users.confirm_user(email=form.email.data, username=form.username.data, password=form.password.data)
        
        return redirect(url_for("auth.login"))
    
    if form.password.data != form.confirm.data:
        flash("Las contraseñas no son iguales", "error")
    
    return render_template("users/sign_up_confirm.html", form=form)


@users_blueprint.get("/user-profile/")
@auth.login_required
def user_profile():
    """
        Redirige al perfil del usuario.
    """
    user = Users.user_show(session["user"]["id"])
    
    return render_template("users/profile.html", user=user)


@users_blueprint.get("/")
@auth.permission_required("user_index")
def user_index():
    """
        Redirige a la página que contiene el listado de usuarios.
    """
    users = Users.user_index()
    form = Forms.UserCreateForm()
    
    return render_template("users/index.html", users=users, form=form)


@users_blueprint.get("/user-info/<user_id>")
@auth.permission_required("user_show")
def user_show(user_id):
    """
        Redirige a la página de información de un usuario.
    """
    user = Users.user_show(int(user_id))
    form = Forms.UserUpdateForm()
    
    return render_template("users/info.html", user=user, form=form)



@users_blueprint.post("/user-index/user-create")
@auth.permission_required("user_create")
def user_create():
    """
        Crea un nuevo usuario.
        
        args:
            Datos del usuario a traves de formulario POST.
        
        return:
            Redireccion a la pagina de listado de usuarios.
    """
    form = Forms.UserCreateForm()
    users = Users.user_index()
    
    if form.validate_on_submit():
        if Users.exists_user(form.email.data):
            flash("El email ingresado ya existe, por favor ingresa otro", "error")
            return render_template("users/index.html", users=users, form=form)
        
        if Users.exists_user(form.username.data):
            flash("El nombre de usuario ya existe, por favor ingresa otro", "error")
            return render_template("users/index.html", users=users, form=form)
        
        u = Users.create_user(**form.data)
        users.append(u)
        for input in form:
            input.data = ""
        flash("El usuario fue registrado correctamente", "success")
    
    return render_template("users/index.html", users=users, form=form)


@users_blueprint.post("/users-update/<user_id>")
@auth.permission_required("user_update")
def user_update(user_id):
    """
        Actualiza la información de un usuario.
        
        args:
            usuario_id -> id del usuario a modificar.
            Datos del usuario a traves de formulario POST.
        
        return:
            Redireccion a la pagina de información del usuario.
    """
    form = Forms.UserUpdateForm()
    user_id = int(user_id)
    user = Users.user_show(user_id)
    
    if form.validate_on_submit():
        if not Users.validate_identifier(user_id, form.email.data):
            flash("El email ingresado ya existe, por favor ingresa otro", "error")
            return render_template("users/info.html", user=user, form=form)
        
        if not Users.validate_identifier(user_id, form.username.data):
            flash("El nombre de usuario ya existe, por favor ingresa otro", "error")
            return render_template("users/info.html", user=user, form=form)
        
        form.active.data = True if form.active.data == "True" else False
        user = Users.user_update(user_id, **form.data)
        flash("El usuario fue actualizado correctamente", "success")
    
    return render_template("users/info.html", user=user, form=form)


@users_blueprint.route("/users-delete/<user_id>", methods=["DELETE"])
@auth.permission_required("user_destroy")
def user_destroy(user_id):
    """
        Elimina un usuario del sistema.
        
        args:
            user_id -> ID del usuario a eliminar.
        
        return:
            Redireccion a la pagina de listado de usuarios.
    """
    user_id = int(user_id)
    Users.user_destroy(user_id)
    flash("El usuario fue eliminado correctamente", "success")
    
    return jsonify({"url": "/users/"}), 200