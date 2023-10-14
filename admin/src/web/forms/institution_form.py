from src.core.models import institution
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError

class InstitutionForm(FlaskForm):
    name = StringField("Nombre de la institución", validators=[DataRequired(), Length(min=2, max=50)])
    # def validate_name(self,name):
    #     if institution.check_if_institution_exists_by_name(name.data):
    #         raise ValidationError("La institución ya existe.")
        
    address = StringField("Dirección", validators=[DataRequired(), Length(min=2, max=100)])
    info = StringField("Información de la institución", validators=[DataRequired(), Length(min=2, max=200)])
    web = StringField("Pagina web", validators=[DataRequired(), Length(min=2, max=100)])
    phone = StringField("Telefono", validators=[DataRequired(), Length(min=2, max=50)])
    social_networks = StringField("Redes sociales", validators=[DataRequired(), Length(min=2, max=100)])