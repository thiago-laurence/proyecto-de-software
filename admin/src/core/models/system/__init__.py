from flask import Response, json
from src.core.models.system.system import System
from src.core.database import db

def system_show(name_system):
    """
        Busca y retorna el sistema.
        
        args:
        
            name_system -> nombre del sistema a buscar.
            
        return:
        
            System -> sistema encontrado.
            
            None -> el sistema no existe.
    """
    
    system = System.query.filter(System.name == name_system).first()
    
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
    system = System.query.filter(System.id == system_id).first()
    
    if system is None:
        return None
    
    data = System(**kwargs)
    system.element_page = data.element_page
    system.message = data.message
    system.info = data.info
    system.activate = True if data.activate == "True" else False
    
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

def is_available(name_system):
    """
        Verifica si el sistema está disponible.
        
        args:
            name_system: nombre del sistema a verificar.
            
        return:
            True si está disponible.
            
            False en caso contrario.
    """
    system = System.query.filter(System.name == name_system).first()
    if system is None:
        return False
    return system.activate