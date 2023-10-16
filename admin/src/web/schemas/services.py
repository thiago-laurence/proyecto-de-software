from marshmallow import Schema, fields
from src.web.schemas.institutions import institution_schema

class ServiceSchema(Schema):
    name = fields.Str()
    info = fields.Str()
    institution = fields.Nested(institution_schema, only=['name'])
    key_words = fields.Str()
    is_enabled = fields.Bool()
    
service_schema = ServiceSchema()
services_schema = ServiceSchema(many=True)