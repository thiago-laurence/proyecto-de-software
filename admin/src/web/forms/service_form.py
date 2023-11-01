from flask_wtf import FlaskForm
from wtforms import StringField, SelectField
from wtforms.validators import InputRequired, Length, ValidationError

class ServiceCreateForm(FlaskForm):
    """
        Formulario para crear un servicio.
    """  
    name = StringField("Nombre", validators=[InputRequired(), Length(max=50,message="El campo nombre tiene un máximo de 50 caracteres")])     
    info = StringField("Información", validators=[InputRequired(), Length(max=200,message="El campo descripción tiene un máximo de 200 caracteres")])
    type_service_id = SelectField(
        "Tipo", 
        choices=[("1", "Análisis"), ("2", "Consultoría"), ("3", "Desarrollo")],
        validators=[InputRequired(),Length(max=50)])
        
    key_words = StringField("Palabras clave", validators=[InputRequired(), Length(max=200,message="El campo palabras clave tiene un máximo de 200 caracteres")])

