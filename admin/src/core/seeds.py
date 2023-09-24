from src.core.models import users
from src.core.bcrypt import bcrypt
from src.core.models import institution


def create_institutions_and_services():
    print("----> Creando instituciones")
    i1 = institution.create_institution(
        name="Alba pinturas",
        info="Pinturas de máxima calidad",
        address="1 y 122",
        web="albapinturas.com.ar",
        phone="221-35123192",
        social_networks="@albapinturas"
    )
    i2 = institution.create_institution(
        name="Ancaflex",
        info="Malísimas, creo..",
        address="13 y 57",
        web="ancaflex.com.ar",
        phone="221-29812732",
        social_networks="@ancaflex"
    )
    print("----> Creando servicios...")
    s1 = institution.create_service(
        name="Revestimiento",
        info="De grano grueso"
    )
    s2 = institution.create_service(
        name="Alisado",
        info="De muchas capas de masilla"
    )
    s3 = institution.create_service(
        name="Tinta a revear",
        info="Proceso de tintura a revestimiento de grano fino"
    )
    print("----> Asignado servicios...")
    institution.assign_service(i1,s1)
    institution.assign_service(i1,s3)
    institution.assign_service(i2,s2)
    print("----> Finalizado! <----")

def create_users():
    print("----> Creando usuarios")
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
    print("----> Finalizado! <----")

def run():
    create_users()
    create_institutions_and_services()