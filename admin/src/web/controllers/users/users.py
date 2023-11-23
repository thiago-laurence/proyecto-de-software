from flask import Blueprint, render_template, request, flash, redirect, url_for, session, jsonify
from src.core.models import user as Users
from src.core.models import user_institution
from src.web.forms import user_form as Forms
from src.web.helpers import auth
from src.web import mail as Mail
from src.web import token as Token
from src.web.oauth import oauth as OAuth

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
        
        args: \n
            email -> email del usuario a registrar. \n
            name -> nombre del usuario a registrar. \n
            lastname -> apellido del usuario a registrar. \n
    """

    form = Forms.UserRegisterForm(request.form)
    user = Users.find_user(form.email.data)
    if user:
        flash("El email ingresado ya está registrado, por favor ingresa otro", "error")
        return render_template("users/sign_up.html", form=form)
    
    user = Users.parcial_register_user(**form.data)
    
    token = Token.generate_confirmation_token(user.email)
    confirm_url = url_for('users.confirm_email', token=token, _external=True)
    html = render_template('users/_email-confirm-account.html', confirm_url=confirm_url)
    subject = "Confirme su cuenta"
    Mail.send_email(user.email, subject, html)
    
    flash("Registro parcial exitoso. Se ha enviado un correo de confirmación de registro a la dirección ingresada", "success")
    
    return render_template("users/sign_up.html", form=form)

@users_blueprint.route("/sign-up/register-google/<email>/<lastname>/<name>")
def register_google(email, lastname, name):
    """
        Registra un nuevo usuario a traves de Google (de forma parcial).
        
        args: \n
            email -> email del usuario a registrar. \n
            name -> nombre del usuario a registrar. \n
            lastname -> apellido del usuario a registrar. \n
    """
    form = Forms.UserRegisterForm()
    user = Users.find_user(email)
    if user:
        flash("El email ingresado ya está registrado, por favor seleccione otra cuenta", "error")
        return render_template("users/sign_up.html", form=form)
    data = {"email": email, "name": name, "lastname": lastname}
    user = Users.parcial_register_user(**data)
    
    token = Token.generate_confirmation_token(user.email)
    confirm_url = url_for('users.confirm_email', token=token, _external=True)
    html = render_template('users/_email-confirm-account.html', confirm_url=confirm_url)
    subject = "Confirme su cuenta"
    Mail.send_email(user.email, subject, html)
    
    flash("Registro parcial exitoso. Se ha enviado un correo de confirmación al gmail seleccionado", "success")
    
    return render_template("users/sign_up.html", form=form)


@users_blueprint.route("/sign-up/register-google")
def authentication_google():
    """
        Autenticacion de usuario a traves de google cloud
    """
    redirect_uri = url_for('users.register_google_callback', _external=True)

    return OAuth.google.authorize_redirect(redirect_uri)

@users_blueprint.route("/sign-up/google-callback")
def register_google_callback():
    """
        URI de callback de google cloud
    """
    token = OAuth.google.authorize_access_token()
    user = token['userinfo']

    return redirect(url_for("users.register_google", email=user["email"], lastname=user["family_name"], name=user["given_name"]))


@users_blueprint.post("/sign-up/confirm-mail/<token>")
def confirm_register(token):
    """
        Confirma el registro de un usuario.
        Valida que el token recibido sea valido, y que coincida con el email del usuario a confirmar.
        
        args:
            token -> token de validacion de email a confirmar \n
            email -> email del usuario a confirmar \n
            username -> nobre de usuario \n
            password -> contraseña del usuario \n
    """
    
    form = Forms.UserConfirmRegisterForm()
    try:
        email = Token.confirm_token(token)
        if (email != form.email.data):
            raise Exception
    except:
        flash("El token de confirmacion es invalido al email del usuario", "error")
        return render_template("users/sign_up_confirm.html", form=form)
    
    user = Users.find_user(form.email.data)
    
    if user and user.confirmed:
        return redirect(url_for("auth.login"))
    
    if form.validate_on_submit():
       
        if Users.exists_user(form.username.data):
            flash("El nombre de usuario ingresado ya existe, por favor ingresa otro", "error")
            return render_template("users/sign_up_confirm.html", form=form)
        
        Users.confirm_user(email=form.email.data, username=form.username.data, password=form.password.data)
        flash('La cuenta ha sido confirmada, por favor inicie sesion', 'success')
        
        return redirect(url_for("auth.login"))
    
    if form.password.data != form.confirm.data:
        flash("Las contraseñas no son iguales", "error")
    
    return render_template("users/sign_up_confirm.html", form=form)


@users_blueprint.get('/sign-up/confirm-mail/<token>')
def confirm_email(token):
    """
        Valida el token de confirmacion de cuenta.
    """
    
    try:
        email = Token.confirm_token(token)
        user = Users.find_user(email)
    except:
        flash('El enlace de confirmacion es invalido o ha exipirado.', 'error')
        return redirect(url_for('auth.login'))
    
    if user.confirmed:
        flash('La cuenta ha sido confirmada, por favor inicie sesion', 'success')
        return redirect(url_for('auth.login'))
    
    form = Forms.UserConfirmRegisterForm()
    form.email.data = user.email
    
    return render_template('users/sign_up_confirm.html', form=form)


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
        Redirige a la página que contiene el listado de usuarios, filtrando por nombre y estado a los mismos.
    """
    form_create = Forms.UserCreateForm()
    page = request.args.get("page", 1, type=int)
    query = request.args.get("query", "", type=str)
    active = request.args.get("active", "", type=str)

    users = Users.list_page_users(page, query, active)
    
    return render_template("users/index.html", form_create=form_create, users=users[0], total_pages=users[1], page=page, query=query, active=active)

@users_blueprint.get("/all-users")
def all_users():
    """
        me retorna una lista con los emails de todos los usuarios
    """
    users = Users.get_users_emails()
    return users
    

@users_blueprint.get("/user-info/<user_id>")
@auth.permission_required("user_show")
def user_show(user_id):
    """
        Redirige a la página de información de un usuario.
    """
    user = Users.user_show(int(user_id))
    if user is None:
        flash("El usuario no existe", "error")
        return redirect(url_for("users.user_index"))
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
    
    if form.validate_on_submit():
        if Users.exists_user(form.email.data):
            flash("El email ingresado ya existe, por favor ingresa otro", "error")
            return redirect(url_for("users.user_index"))
        
        if Users.exists_user(form.username.data):
            flash("El nombre de usuario ya existe, por favor ingresa otro", "error")
            return redirect(url_for("users.user_index"))
        
        u = Users.create_user(**form.data)
        flash("El usuario fue registrado correctamente", "success")
    
    return redirect(url_for("users.user_index"))


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
    if user is None:
        flash("El usuario no existe", "error")
        return redirect(url_for("users.user_index"))
    
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
    if Users.user_show(user_id) is None:
        flash("El usuario no existe", "error")
        return redirect(url_for("users.user_index"))
    
    if (not user_institution.check_unique_owner(user_id)):
        Users.user_destroy(user_id)
        flash("El usuario fue eliminado correctamente", "success")
    else:
        flash("El usuario no se puede eliminar porque es el unico dueño en alguna institución", "error")
    return jsonify({"url": "/users/"}), 200