from src.core.models.role.role import Role
from src.core.database import db

def list_roles():
    """
        Retorna todos los roles
    """   
    roles = Role.query.all()
    return roles

def assign_permission(role, permission):
    """
        Asigna un permiso a un rol
    """
    role.permissions.extend(permission)
    db.session.add(role)
    db.session.commit()
    
def create_role(**kwargs):
    """
        Se registra un nuevo rol
    """
    
    role = Role(**kwargs)
    db.session.add(role)
    db.session.commit()
    return role

def get_role_by_name(name):
    """
        Busca un rol por nombre y lo retorna.
    """
    return Role.query.filter_by(name=name).first()

def get_permission_by_role(role):
    """
        Retorna los permisos de un rol
    """
    return role.permissions

def contains_permission (role_id, permission):
    """
        Retorna True si el rol contiene el permiso
        args:
            role_id: id del rol
            permission: nombre del permiso a buscar
    """
    role = Role.query.filter_by(id=role_id).first()
    permissions = [p.name for p in role.permissions]
    return permission in permissions