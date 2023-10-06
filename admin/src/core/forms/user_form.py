from flask_wtf import FlaskForm
from wtforms import EmailField, StringField, PasswordField, SubmitField, BooleanField, SelectField, TextAreaField, IntegerField, FileField
from wtforms.validators import InputRequired, Length, Email, EqualTo, ValidationError, NumberRange

class LoginForm(FlaskForm):
    """
        Formulario de inicio de sesión.
    """
    email_username = StringField("Correo electrónico", description="Ingrese su email o nombre de usuario",validators=[InputRequired()])
    password = PasswordField("Contraseña", description="Ingrese su contraseña", validators=[InputRequired()])
    # remember = BooleanField("Recordarme")


class UserRegisterForm(FlaskForm):
    """
        Formulario para el registro de un usuario.
    """
    email = EmailField("Email", validators=[InputRequired(), Email()])
    name = StringField("Nombre", validators=[InputRequired(), Length(max=50)])
    lastname = StringField("Apellido", validators=[InputRequired(), Length(max=50)])

class UserConfirmRegisterForm(FlaskForm):
    """
        Formulario para confirmar registro de usuario.
    """
    email = EmailField("Email", validators=[InputRequired(), Email()])
    username = StringField("Nombre de usuario", validators=[InputRequired(), Length(max=50)])
    password = PasswordField("Contraseña", validators=[InputRequired(), EqualTo("confirm", message="Las contraseñas no coinciden"), Length(min=6, max=20)])
    confirm = PasswordField("Confirmar contraseña", validators=[InputRequired(), Length(min=6, max=20)])

class UserCreateForm(UserRegisterForm):
    """
        Formulario para crear usuario.
    """
    username = StringField("Nombre de usuario", validators=[InputRequired(), Length(max=50)])

class UserUpdateForm(UserCreateForm):
    """
        Formulario para la actualizacion de la informacion de un usuario
    """
    active = SelectField("Estado", choices=[("True", "Activo"), ("False", "Inactivo")])