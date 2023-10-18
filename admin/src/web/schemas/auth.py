from marshmallow import Schema, fields, validate

class CreateAuthSchema(Schema):
    email = fields.Email()
    password = fields.String()    
    
create_auth_schema = CreateAuthSchema()