from flask_wtf import FlaskForm
from wtforms import SelectField, TextAreaField, IntegerField
from wtforms.validators import InputRequired, Length, NumberRange

class SystemForm(FlaskForm):
    """
        Fomrulario para la configuracion del sistema.
    """
    element_page = IntegerField("Elementos por página", validators=[InputRequired(), NumberRange(min=1, max=10)])
    activate = SelectField("Activar sistema", choices=[(True, "Activado"), (False, "Desactivado")])
    info = TextAreaField("Información de contacto", validators=[InputRequired(), Length(max=255)])
    message = TextAreaField("Mensaje de mantenimiento", validators=[InputRequired(), Length(max=255)])