from src.core.models.permission.permission import Permission
from src.core.database import db

def list_permissions():
    """
        Retorna todos los permisos
    """   
    permissions = Permission.query.all()
    return permissions

def assign_permission(role, permission):
    """
        Asigna un permiso a un rol
    """
    permission.add_role(role)
    db.session.commit()

def create_permission(**kwargs):
    """
        Se registra un nuevo permiso
    """
    
    permission = Permission(**kwargs)
    db.session.add(permission)
    db.session.commit()
    return permission

def get_permission_by_name(name):
    """
        Retorna un permiso por su nombre
    """
    return Permission.query.filter_by(name=name).first()

def get_permission_by_prefix(prefix):
    """
        Retorna un permiso por su prefijo
    """
    return Permission.query.filter(Permission.name.startswith(prefix)).all()