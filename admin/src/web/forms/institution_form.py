from src.core.models import institution
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError, InputRequired, Regexp

class InstitutionForm(FlaskForm):
    name = StringField("Nombre de la institución", validators=[DataRequired(), Length(min=2, max=50)])   
    address = StringField("Dirección", validators=[InputRequired(), Length(min=2, max=100)])
    info = StringField("Información de la institución", validators=[InputRequired(), Length(min=2, max=200)])
    web = StringField("Pagina web", validators=[InputRequired(), Length(min=2, max=100)])
    phone = StringField("Teléfono", validators=[InputRequired(), Length(min=2, max=50),Regexp(r'^[\d-]+$', message="Ingrese un número de teléfono válido")])
    social_networks = StringField("Redes sociales", validators=[InputRequired(), Length(min=2, max=100)])
    localization = StringField("Localización", validators=[InputRequired(), Length(min=2, max=100),Regexp(r'^[\d,]+$', message="Ingrese dos coordenadas separadas por coma")])
    atencion_days = StringField("Días y horarios de atención", validators=[InputRequired(), Length(min=2, max=100)])