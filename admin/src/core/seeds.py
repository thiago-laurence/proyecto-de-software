from src.core.models import users
from src.core.bcrypt import bcrypt

def run():
    print("Creando usuarios...")
    hash_default_pass = bcrypt.generate_password_hash("123".encode('utf-8'))
    users.create_user(
        email = "root@gmail.com",
        username = "Root",
        name = "Super",
        lastname = "User",
        password = hash_default_pass.decode('utf-8'),
        active = True,
        confirmed = True
    )
    users.create_user(
        email = "user@gmail.com",
        username = "MyUser",
        name = "User",
        lastname = "1",
        password = hash_default_pass.decode('utf-8'),
        active = True,
        confirmed = True
    )
    print("Usuarios creados!")