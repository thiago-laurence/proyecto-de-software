from src.core.models import user
from src.core.bcrypt import bcrypt
from src.core.models import institution
from src.core.models import user_institution
from src.core.models import role
from src.core.models import permission


def create_institutions_and_services():
    print("----> Creando instituciones...")
    i = institution.create_institution(
        name = "CIDEPINT",
        info = "Centro de Investigación y Desarrollo en Tecnología de Pinturas y Recubrimientos",
        address = "Av. 52 e/ 121 y 122",
        web = "cidepint.ing.unlp.edu.ar",
        phone = "+54 0221 421-2433",
        social_networks = "@cidepint"
    )
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
    print("----> Creando usuarios...")
    hash_default_pass = bcrypt.generate_password_hash("123".encode('utf-8'))
    user.create_user(
        email = "root@gmail.com",
        username = "Root",
        name = "Super",
        lastname = "User",
        password = hash_default_pass.decode('utf-8'),
        active = True,
        confirmed = True
    )
    user.create_user(
        email = "user00@gmail.com",
        username = "User00",
        name = "User",
        lastname = "00",
        password = hash_default_pass.decode('utf-8'),
        active = True,
        confirmed = True
    )
    user.create_user(
        email = "user01@gmail.com",
        username = "User01",
        name = "User",
        lastname = "01",
        password = hash_default_pass.decode('utf-8'),
        active = True,
        confirmed = True
    )
    user.create_user(
        email = "user02@gmail.com",
        username = "User02",
        name = "User",
        lastname = "02",
        password = hash_default_pass.decode('utf-8'),
        active = True,
        confirmed = True
    )
    print("----> Finalizado! <----")

def create_roles():
    print("----> Creando roles...")
    role.create_role(
        name = "SuperAdministrador/a"
    )
    role.create_role(
        name = "Dueño/a"
    )
    role.create_role(
        name = "Administrador/a"
    )
    role.create_role(
        name = "Operador/a"
    )
    print("----> Finalizado! <----")

def create_permissions():
    print("----> Creando permisos...")
    permission.create_permission(
        name = "Index"
    )
    permission.create_permission(
        name = "Show"
    )
    permission.create_permission(
        name = "Update"
    )
    permission.create_permission(
        name = "Create"
    )
    permission.create_permission(
        name = "Destroy"
    )
    permission.create_permission(
        name = "Activate"
    )
    permission.create_permission(
        name = "Deactivate"
    )
    print("----> Finalizado! <----")

def assign_permissions_to_roles():
    print("----> Asignando permisos a roles...")
    # Permisos
    index = permission.get_permission_by_name("Index")
    show = permission.get_permission_by_name("Show")
    update = permission.get_permission_by_name("Update")
    destroy = permission.get_permission_by_name("Destroy")
    create = permission.get_permission_by_name("Create")
    activate = permission.get_permission_by_name("Activate")
    deactivate = permission.get_permission_by_name("Deactivate")
    # SuperAdministrador
    superAdmin = role.get_role_by_name("SuperAdministrador/a")
    role.assign_permission(superAdmin, [index, update, create, show, destroy, activate, deactivate])
    # Dueño
    owner = role.get_role_by_name("Dueño/a")
    role.assign_permission(owner, [index, update, create, show, destroy])
    # Administrador
    admin = role.get_role_by_name("Administrador/a")
    role.assign_permission(admin, [index, update, create, show, destroy])
    # Operador
    operator = role.get_role_by_name("Operador/a")
    role.assign_permission(admin, [index, update, create, show])
    
    print("----> Finalizado! <----")

def assign_roles_to_users():
    print("----> Asignando roles a usuarios...")
    superAdmin = role.get_role_by_name("SuperAdministrador/a")
    owner = role.get_role_by_name("Dueño/a")
    admin = role.get_role_by_name("Administrador/a")
    operator = role.get_role_by_name("Operador/a")
    i0 = institution.get_institution_by_name("CIDEPINT")
    i1 = institution.get_institution_by_name("Alba pinturas")
    root = user.find_user("Root")
    user00 = user.find_user("User00")
    user01 = user.find_user("User01")
    user02 = user.find_user("User02")
    ui_root = user_institution.create_user_institution_role(
        user = root,
        institution = i0,
        role = superAdmin
    )
    ui_user00 = user_institution.create_user_institution_role(
        user = user00,
        institution = i1,
        role = owner
    )
    ui_user01 = user_institution.create_user_institution_role(
        user = user01,
        institution = i1,
        role = admin
    )
    ui_user02 = user_institution.create_user_institution_role(
        user = user02,
        institution = i1,
        role = operator
    )
    user.assign_institution_and_role(root, [ui_root])
    user.assign_institution_and_role(user00, [ui_user00])
    user.assign_institution_and_role(user01, [ui_user01])
    user.assign_institution_and_role(user02, [ui_user02])

def run():
    create_users()
    create_institutions_and_services()
    create_roles()
    create_permissions()
    assign_permissions_to_roles()
    assign_roles_to_users()