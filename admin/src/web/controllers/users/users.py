from flask import Blueprint, render_template, request, flash, redirect, url_for, Response, json
from src.core.models import user as Users
from src.web.helpers import auth
from src.web import mail

users_blueprint = Blueprint("users", __name__, url_prefix="/users")

@users_blueprint.get("/sing-up")
def sign_up():
    """
        Redirige al formulario de registro de usuario.
    """
    
    return render_template("users/sign_up.html")

@users_blueprint.post("/sign-up/register")
def register():
    """
        Registra un nuevo usuario (de forma parcial) obtiendo los datos del formulario.
        args:
            email: email del usuario a registrar.
            name: nombre del usuario a registrar.
            lastname: apellido del usuario a registrar.
    """

    params = request.form
    user = Users.find_user(params['email'])
    if user:
        flash("El email ingresado ya está registrado, por favor ingresa otro", "error")
        return redirect(url_for("users.sign_up"))
    
    user = Users.create_user(email=params['email'], name=params['name'], lastname=params['lastname'])
    url = request.host_url + "/users/sign-up/confirm"
    body = """
        <p> Bienvenido a CIDEPINT, para completar el registro ingresa al siguiente link: </p>
        <form action=""" + url + """ method="POST">
            <input type="hidden" name="email" value=""" + user.email + """>
            <button type="submit">Confirmar</button>
        </form>
    """
    mail.send_mail("Confirmación de registro", params['email'], body)
    
    flash("Registro parcial exitoso. Se ha enviado un correo de confirmación de registro a la dirección ingresada", "success")
    
    return redirect(url_for("users.sign_up"))

@users_blueprint.post("/sign-up/confirm")
def confirm_register():
    """
        Confirma el registro de un usuario.
        
        args:
            email: email del usuario a confirmar
            username: nobre de usuario
            password: contraseña del usuario
    """
    
    params = request.form
    user = Users.find_user(params['email'])
    
    if user and user.confirmed:
        return redirect(url_for("auth.login"))
    
    if params.__len__() == 1:
        return render_template("users/confirm.html", email=params['email'])
    
    if params['password'] != params['confirm-password']:
        flash("Las contraseñas ingresadas no coinciden", "error")
        return render_template("users/sign_up_confirm.html", email=params['email'])
    
    user = Users.find_user(params['username'])
    
    if user:
        flash("El nombre de usuario ingresado ya existe", "error")
        return render_template("users/sign_up_confirm.html", email=params['email'])
    
    Users.confirm_user(email=params['email'], password=params['password'], username=params['username'])
    
    return redirect(url_for("auth.login"))


@users_blueprint.get("/user_index")
@auth.permission_required("user_index")
def user_index():
    """
        Retorna todos los usuarios.
            
        return:
            JSON response users 200
            
            JSON response error 400
    """
    users = Users.get_users()
    data = [u.to_json() for u in users]
    response = Response(
        response = json.dumps(data),
        status = 200,
        mimetype = 'application/json'
    )
    
    return render_template("users/index.html", users=response.get_json())

@users_blueprint.get("/user-show/<user_id>")
@auth.permission_required("user_show")
def user_show(user_id):
    """
        Retorna un usuario.
        
        args:

            user_id -> ID del usuario a retornar.
        
        return:
            El usuario fue encontrado -> JSON 200 ok, usuario
            El usuario no existe -> JSON 400 fail
    """
    
    
    user = Users.user_show(user_id)
    if user is None:
        cod = 400
        data = {
            "error": "El usuario no existe"
        }
    else:
        cod = 200
        data = user.to_json()
        
    response = Response(
        response = json.dumps(data),
        status = cod,
        mimetype = 'application/json'
    )
    
    return response.get_json()


@users_blueprint.route("/users-delete/<user_id>", methods=["DELETE"])
@auth.permission_required("user_destroy")
def user_destroy(user_id):
    """
        Metodo para eliminar un usuario del sistema.
        
        args:
            user_id -> ID del usuario a eliminar.
        
        return:
            El usuario fue eliminado con exito -> JSON 200 ok, url de redireccion
            El usuario no existe -> JSON 400 fail
    """
    
    ok = Users.user_destroy(user_id)
    if not ok:
        cod = 400
        data = {
            "error": "El usuario no existe"
        }
    else:
        cod = 200
        data = {
            "ok": "El usuario fue eliminado con exito",
            "url": "/users/user_index"
        }
        
    response = Response(
        response = json.dumps(data),
        status = cod,
        mimetype = 'application/json'
    )
    
    return response.get_json()


@users_blueprint.put("/users-update/<user_id>")
@auth.permission_required("user_update")
def user_update(user_id):
    """
        Actualiza la información de un usuario.
        
        args:
            usuario_id: id del usuario a modificar.
        
        return:
            JSON response user 200
            
            JSON response error 400
    """
    response = Response(mimetype = 'application/json')
    
    user = Users.find_user(request.json['data']['email'])
        
    if user and (user.id != int(user_id)):
        response.set_data(json.dumps({
            "error": "El email ingresado ya existe, por favor ingresa otro",
            "url": "/users/user_index/user-info/"+ str(user_id)
        }))
        flash("El email ingresado ya existe, por favor ingresa otro", "error")
        return response.get_json()
    
    user = Users.find_user(request.json['data']['username'])
    if user and (user.id != int(user_id)):
        response.set_data(json.dumps({
            "error": "El nombre de usuario ingresado ya existe, por favor ingresa otro",
            "url": "/users/user_index/user-info/"+ str(user_id)
        }))
        flash("El nombre de usuario ingresado ya existe, por favor ingresa otro", "error")
        return response.get_json()
    
    user = Users.user_update(user_id, **request.json['data'])
    
    if user is None:
        response.set_data(json.dumps({"error": "El usuario no existe"}))
        return response.json
    
    response.set_data(json.dumps({"url": "/users/user_index/user-info/"+ str(user.id)}))
    response.status_code = 200
    
    flash("La información del usuario ha sido actualizada con exito!", "success")
    
    return response.json


@users_blueprint.get("/user-profile/<user_id>")
@auth.session_required
def user_profile(user_id):
    """
        Redirige al perfil del usuario.
    """
    
    user = user_show(user_id)
    
    return render_template("users/profile.html", user=user)


@users_blueprint.get("/user_index/user-info/<user_id>")
@auth.session_required
def user_info(user_id):
    """
        Redirige a la página de información de un usuario.
    """
    
    user = user_show(user_id)
    
    return render_template("users/info.html", user=user)

@users_blueprint.post("/user_index/user-create")
@auth.permission_required("user_create")
def user_create():
    """
        Registra a un nuevo usuario en el sistema.
        
        args:
            Datos del usuario enviados a traves de un formulario POST.
        
        return:
            JSON response user 200
            
            JSON response error 400
    """
    data = request.form.to_dict()
    
    user = Users.find_user(data["email"])
        
    if user:
        flash("El email ingresado ya existe, por favor ingresa otro", "error")
        return redirect(url_for("users.user_index"))
    
    user = Users.find_user(data["username"])
    if user:
        flash("El nombre de usuario ingresado ya existe, por favor ingresa otro", "error")
        return redirect(url_for("users.user_index"))
    
    user = Users.user_create(**data)
    if user is None:
        flash("Parámetros inválidos", "error")
        return redirect(url_for("users.user_index"))
    
    flash("La información del usuario ha sido actualizada con exito!", "success")
    
    return redirect(url_for("users.user_index"))
    