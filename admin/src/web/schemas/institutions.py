from marshmallow import Schema, fields

class InstitutionSchema(Schema):
    name = fields.Str()
    info = fields.Str()
    address = fields.Str()
    localization = fields.Str()
    web = fields.Str()
    atencion_days = fields.Str()
    email = fields.Email()
    is_enabled = fields.Bool()
    
institution_schema = InstitutionSchema()
institutions_schema = InstitutionSchema(many=True)