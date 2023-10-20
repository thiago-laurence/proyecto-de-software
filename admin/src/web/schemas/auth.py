from marshmallow import Schema, fields, validate

class CreateAuthSchema(Schema):
    email = fields.Email(required=True, error_messages={"required": "El email es requerido", "invalid": "El email no posee un formato válido"})
    password = fields.String(required=True, validate=validate.Length(min=6, max=50, error="La contraseña debe tener entre 6 y 50 caracteres"), error_messages={
        "required": "La contraseña es requerida"
        })    
    
create_auth_schema = CreateAuthSchema()