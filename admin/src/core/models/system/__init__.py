from src.core.models.system.system import System
from src.core.database import db

def system_show():
    """
        Busca y retorna el sistema.
            
        return:
        
            System -> sistema encontrado.
            
            None -> el sistema no existe.
    """
    
    system = System.query.filter(System.id == 1).first()
    
    return system

def system_update(**kwargs):
    """
        Actualiza la información del sistema.
        
        args:
            kwargs -> campos del objeto sistema actualizados.
        
        return:
            System -> el sistema fue actualizado.
            
            None -> el sistema no existe.
    """
    system = system_show()
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

def is_available():
    """
        Verifica si el sistema está disponible.
            
        return:
            True si está disponible.
            
            False en caso contrario.
    """
    system = System.query.filter(System.id == 1).first()
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