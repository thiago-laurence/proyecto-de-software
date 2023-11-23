from marshmallow import Schema, fields

class StateOrderSchema(Schema):
    """
        Schema de estado de orden de servicio para retornar su perfil
    """
    id = fields.Int(dump_only=True)
    name = fields.Str()
    
state_order_schema_one = StateOrderSchema()
state_order_schema = StateOrderSchema(many=True)