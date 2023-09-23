from src.core.models import users

def run():
    print("Creando usuarios...")
    user1 = users.create_user(name="Juan")
    user2 = users.create_user(name="Pedro")
    user3 = users.create_user(name="Ana")
    user4 = users.create_user(name="Maria") 
    print("Usuarios creados!")