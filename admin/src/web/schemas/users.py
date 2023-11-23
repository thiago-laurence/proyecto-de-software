from marshmallow import Schema, fields, validate

class UserSchema(Schema):
    """
        Schema de usuario para retornar su perfil
    """
    id = fields.Integer(dump_only=True)
    username = fields.String()
    email = fields.Email()
    name = fields.String()
    lastname = fields.String()
    active = fields.Boolean(dump_only=True)

user_schema = UserSchema()
users_schema = UserSchema(many=True)

class CreateUserSchema(Schema):
    """
        Schema de usuario para crear uno nuevo
    """
    username = fields.String(required=True, validate=validate.Length(min=1, max=50, error="El nombre de usuario debe tener entre 1 y 50 caracteres"), error_messages={"required": "El nombre de usuario es requerido"})
    email = fields.Email(required=True, error_messages={"required": "El email es requerido", "invalid": "El email no posee un formato válido"})
    name = fields.String(required=True, validate=validate.Length(min=1, max=50, error="El nombre debe tener entre 1 y 50 caracteres"), error_messages={"required": "El nombre es requerido"})
    lastname = fields.String(required=True, validate=validate.Length(min=1, max=50, error="El apellido debe tener entre 1 y 50 caracteres"), error_messages={"required": "El apellido es requerido"})

create_user_schema = CreateUserSchema()

class CreateUserSignUpSchema(Schema):
    """
        Schema de usuario para crear uno nuevo
    """
    email = fields.Email(required=True, error_messages={"required": "El email es requerido", "invalid": "El email no posee un formato válido"})
    name = fields.String(required=True, validate=validate.Length(min=1, max=50, error="El nombre debe tener entre 1 y 50 caracteres"), error_messages={"required": "El nombre es requerido"})
    lastname = fields.String(required=True, validate=validate.Length(min=1, max=50, error="El apellido debe tener entre 1 y 50 caracteres"), error_messages={"required": "El apellido es requerido"})

create_user_signup_schema = CreateUserSignUpSchema()