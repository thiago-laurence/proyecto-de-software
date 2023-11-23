from marshmallow import Schema, fields
from src.web.schemas.institutions import institution_schema

class ServiceSchema(Schema):
    id = fields.Int()
    name = fields.Str()
    info = fields.Str()
    institution = fields.Nested(institution_schema)
    key_words = fields.Str()
    is_enabled = fields.Bool()
    
service_schema = ServiceSchema()
services_schema = ServiceSchema(many=True)

class TypesServicesSchema(Schema):
    id = fields.Int()
    name = fields.Str()
    
types_services_schema = TypesServicesSchema(many=True)