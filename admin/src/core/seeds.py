from src.core.models import users
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


def run():
    print("Creando usuarios...")
    user1 = users.create_user(name="Juan")
    user2 = users.create_user(name="Pedro")
    user3 = users.create_user(name="Ana")
    user4 = users.create_user(name="Maria") 
    print("Usuarios creados!")
    create_institutions_and_services()