from marshmallow import Schema, fields, validate, EXCLUDE
from src.web.schemas.state_orders import state_order_schema_one
from src.web.schemas.users import UserSchema

class ServiceOrderStatusSchema(Schema):
    """
    Schema para el estado de la orden de servicio
    """
    id = fields.Int(dump_only=True)
    name = fields.Str()

class ServiceOrderStatusChangedSchema(Schema):
    """
    Schema para los cambios de estado de la orden de servicio
    """
    id = fields.Int(dump_only=True)
    service_order_status = fields.Nested(ServiceOrderStatusSchema, only=['name'])
    


class CreateServiceOrderSchema(Schema):
    """
        Schema de orden de servicio para crear uno nuevo
    """
    service_id = fields.Int(dump_only=True) #para saber a que servicio pertenece
    title = fields.Str(required=True, validate=validate.Length(min=1, max=50))
    description = fields.Str(required=True, validate=validate.Length(min=1, max=200))
    creation_date = fields.DateTime() #para saber desde cuando se necesita el servicio
    close_date = fields.DateTime() #para saber hasta cuando
    
create_service_order_schema = CreateServiceOrderSchema(unknown=EXCLUDE)

class CommentSchema(Schema):
    """
        Schema de comentario para retornar su perfil
    """
    id = fields.Int(dump_only=True)
    comment = fields.Str()
    user = fields.Nested(UserSchema, only=['username'])

comment_schema = CommentSchema()

class ServiceOrderSchema(Schema):
    """
        Schema de orden de servicio para retornar su perfil
    """
    id = fields.Int(dump_only=True)
    title = fields.Str()
    creation_date = fields.DateTime()
    close_date = fields.DateTime()
    description = fields.Str()
    status_changes = fields.Nested(ServiceOrderStatusChangedSchema, many=True)
    comments = fields.Nested(CommentSchema, many=True)
    
service_order_schema = ServiceOrderSchema(exclude=['id'])
service_order_schema_with_id = ServiceOrderSchema()
service_orders_schema = ServiceOrderSchema(many=True, exclude=['comments'])

class CreateCommentSchema(Schema):
    """
        Schema de comentario para crear uno nuevo
    """
    comment = fields.Str(required=True, validate=validate.Length(min=1, max=200))
    
create_comment_schema = CreateCommentSchema(unknown=EXCLUDE)
