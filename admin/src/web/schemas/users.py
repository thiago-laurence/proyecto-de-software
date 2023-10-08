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
    username = fields.String(required=True, validate=validate.Length(min=1, max=50))
    email = fields.Email(required=True, validate=validate.Length(min=1, max=50))
    name = fields.String(required=True, validate=validate.Length(min=1, max=50))
    lastname = fields.String(required=True, validate=validate.Length(min=1, max=50))

create_user_schema = CreateUserSchema()