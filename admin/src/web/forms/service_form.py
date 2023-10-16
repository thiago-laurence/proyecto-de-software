from flask_wtf import FlaskForm
from wtforms import StringField, SelectField
from wtforms.validators import InputRequired, Length
from src.core.models import institution

class ServiceCreateForm(FlaskForm):
    """
        Formulario para crear un servicio.
    """
    name = StringField("Nombre", validators=[InputRequired(), Length(max=50)])     
    info = StringField("Información", validators=[InputRequired(), Length(max=200)])
    type = SelectField("Tipo", choices=[("Analisis", "Análisis"), ("Consultoria", "Consultoría"), ("Desarrollo", "Desarrollo")],validators=[InputRequired(), Length(max=50)])
    key_words = StringField("Palabras clave", validators=[InputRequired(), Length(max=200)])

