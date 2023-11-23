from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired


class LoginForm(FlaskForm):
    """
        Formulario de inicio de sesión.
    """
    email_username = StringField("Usuario", description="Ingrese su email o nombre de usuario",validators=[InputRequired()])
    password = PasswordField("Contraseña", description="Ingrese su contraseña", validators=[InputRequired()])
    # remember = BooleanField("Recordarme")