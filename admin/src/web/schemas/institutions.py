from marshmallow import Schema, fields

class InstitutionSchema(Schema):
    name = fields.Str()
    info = fields.Str()
    address = fields.Str()
    web = fields.Str()
    email = fields.Email()
    enabled = fields.Bool()
    
institution_schema = InstitutionSchema()
institutions_schema = InstitutionSchema(many=True)