from src.core.models import institution
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError, InputRequired, Regexp

class InstitutionForm(FlaskForm):
    name = StringField("Nombre de la institución", validators=[DataRequired(), Length(min=2, max=50,message="El campo nombre tiene un máximo de 50 caracteres")])   
    address = StringField("Dirección", validators=[InputRequired(), Length(min=2, max=100,message="El campo dirección tiene un máximo de 100 caracteres")])
    info = StringField("Información de la institución", validators=[InputRequired(), Length(min=2, max=200,message="El campo descripción tiene un máximo de 200 caracteres")])
    web = StringField("Pagina web", validators=[InputRequired(), Length(min=2, max=100,message="El campo página web tiene un máximo de 100 caracteres")])
    phone = StringField("Teléfono", validators=[InputRequired(), Length(min=2, max=50,message="El campo de teléfono tiene un máximo de 50 caracteres"),Regexp(r'^[\d-]+$', message="Ingrese un número de teléfono válido")])
    social_networks = StringField("Redes sociales", validators=[InputRequired(), Length(min=2, max=100,message="El campo de redes sociales tiene un máximo de 100 caracteres")])
    localization = StringField("Localización", validators=[InputRequired(), Length(min=2, max=100, message="El campo localización tiene un máximo de 100 caracteres"),Regexp(r'^[\d,]+$', message="Ingrese dos coordenadas separadas por coma")])
    atencion_days = StringField("Días y horarios de atención", validators=[InputRequired(), Length(min=2, max=100, message="El campo de días y horarios de atención tiene un máximo de 100 caracteres")])
    