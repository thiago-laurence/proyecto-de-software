def validation_string(key, value):
    """
        Valida que el valor de la clave no sea nulo, no este vacio y sea menor a 50 caracteres.
        
        args:
            key -> Nombre del campo del valor a validar.\n
            value -> Valor del campo a validar.
        
        return:
            value -> Valor validado.\n
            ValueError -> Si el valor es nulo, vacio o supera los 50 caracteres.
    """
    
    if value is None:
        raise ValueError(f"El {key} no puede ser Nulo")
    if not value:
        raise ValueError(f"El {key} no puede estar vacío")
    if len(value) > 50:
        raise ValueError(f"El {key} no puede superar los 50 caracteres")
    
    return value

def validation_identifier(user, id, key):
    """
        Valida que el email/username (key) no este registrado ante un registro o modificacion.
        
        args:
            user -> Usuario existente o no.\n
            id -> ID del usuario a crear o modificar.\n
            key -> Nombre del campo del valor a validar.\n
        
        return:
            value -> Valor validado.\n
            ValueError -> Si la clave ya está registrada para otro usuario.
    """
    if (id is None) and user:
        raise ValueError(f'El {key} ya está registrado, por favor ingresa otro')
        
    if (id is not None) and user and (id != user.id):
        raise ValueError(f'El {key} ya está registrado, por favor ingresa otro')