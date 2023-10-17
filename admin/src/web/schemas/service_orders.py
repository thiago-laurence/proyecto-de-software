from marshmallow import Schema, fields, validate, EXCLUDE

class ServiceOrderSchema(Schema):
    """
        Schema de orden de servicio para retornar su perfil
    """
    id = fields.Int(dump_only=True)
    title = fields.Str()
    creation_date = fields.DateTime()
    close_date = fields.DateTime()
    status = fields.Str()
    description = fields.Str()
    
service_order_schema = ServiceOrderSchema(exclude=['id'])
service_order_schema_with_id = ServiceOrderSchema()
service_orders_schema = ServiceOrderSchema(many=True, exclude=['id'])

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

comment_schema = CommentSchema()

class CreateCommentSchema(Schema):
    """
        Schema de comentario para crear uno nuevo
    """
    comment = fields.Str(required=True, validate=validate.Length(min=1, max=200))
    
create_comment_schema = CreateCommentSchema(unknown=EXCLUDE)