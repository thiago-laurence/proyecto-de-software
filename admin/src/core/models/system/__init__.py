from src.core.models.system.system import System
from src.core.database import db

def system_show(system_id):
    """
        Busca y retorna el sistema.
        
        args:
        
            name_system -> nombre del sistema a buscar.
            
        return:
        
            System -> sistema encontrado.
            
            None -> el sistema no existe.
    """
    
    system = System.query.filter(System.id == system_id).first()
    
    return system

def system_update(system_id, **kwargs):
    """
        Actualiza la información del sistema.
        
        args:
            system_id -> id del sistema a modificar.
            
            kwargs -> campos del objeto sistema actualizados.
        
        return:
            System -> el sistema fue actualizado.
            
            None -> el sistema no existe.
    """
    kwargs['activate'] = True if kwargs['activate'] == "True" else False

    system = system_show(system_id)
    if system is None:
        return None
    
    for key, value in kwargs.items():
        setattr(system, key, value)

    db.session.commit()    
    
    return system

def system_create(**kwargs):
    """
        Se registra un nuevo sistema.
        
        args:
            kwargs -> campos del objeto sistema.
        
        return:
            System -> el sistema fue creado.
    """
    
    sys = System(**kwargs)
    db.session.add(sys)
    db.session.commit()
    return sys

def is_available(system_id):
    """
        Verifica si el sistema está disponible.
        
        args:
            name_system: nombre del sistema a verificar.
            
        return:
            True si está disponible.
            
            False en caso contrario.
    """
    system = System.query.filter(System.id == system_id).first()
    if system is None:
        return False
    return system.activate

def pages():
    """
        Retorna la cantidad de elementos por página.
        
        return:
            int -> cantidad de elementos por página.
    """
    system = System.query.first()
    return system.element_page