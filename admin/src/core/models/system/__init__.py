from src.core.models.system.system import System
from src.core.database import db

def system_show(name_system):
    """
        Retorna la informacion del sistema
        return:
            name_system: nombre del sistema a mostrar
    """   
    return System.query.filter(System.name == name_system).first()

def system_create(**kwargs):
    """
        Se registra un nuevo sistema
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