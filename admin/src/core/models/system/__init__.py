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