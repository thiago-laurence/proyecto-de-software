from src.core.models.user import User
from src.core.database import db

def list_all_users():
    """
    Listar todos los usuarios de la base de datos.
    """
    users = User.query.all()
    return users

def create_user(**kwargs):
    """"
    Crear un usuario y almacenarlo en la db.
    """
    user = User(**kwargs)
    db.session.add(user)
    db.session.commit()

    return user