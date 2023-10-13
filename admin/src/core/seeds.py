from src.core.models import user
from src.core.bcrypt import bcrypt
from src.core.models import institution
from src.core.models import user_institution
from src.core.models import role
from src.core.models import permission
from src.core.models import system


def create_system():
    system.system_create(
        name = "CIDEPINT",
        element_page = 10,
        info = "Centro de Investigación y Desarrollo en Tecnología de Pinturas y Recubrimientos",
        message = "El sistema está en mantenimiento, por favor vuelva más tarde.",
        activate = True
    )

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
        info="De grano grueso",
        type="Consultoria",
        key_words="Revestimiento, grano grueso, paredes"
    )
    s2 = institution.create_service(
        name="Alisado",
        info="De muchas capas de masilla",
        type="Desarrollo",
        key_words="Alisado, masilla, paredes"
    )
    s3 = institution.create_service(
        name="Tinta a revear",
        info="Proceso de tintura a revestimiento de grano fino",
        type="Analisis",
        key_words="Tinta, revear, grano fino"
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
        username = "root",
        name = "Super",
        lastname = "User",
        password = hash_default_pass.decode('utf-8'),
        active = True,
        confirmed = True
    )
    user.create_user(
        email = "user00@gmail.com",
        username = "user00",
        name = "User",
        lastname = "00",
        password = hash_default_pass.decode('utf-8'),
        active = True,
        confirmed = True
    )
    user.create_user(
        email = "user01@gmail.com",
        username = "user01",
        name = "User",
        lastname = "01",
        password = hash_default_pass.decode('utf-8'),
        active = True,
        confirmed = True
    )
    user.create_user(
        email = "user02@gmail.com",
        username = "user02",
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
        name = "user_index"
    )
    permission.create_permission(
        name = "user_create"
    )
    permission.create_permission(
        name = "user_destroy"
    )
    permission.create_permission(
        name = "user_update"
    )
    permission.create_permission(
        name = "user_show"
    )
    permission.create_permission(
        name = "ui_index"
    )
    permission.create_permission(
        name = "ui_create"
    )
    permission.create_permission(
        name = "ui_destroy"
    )
    permission.create_permission(
        name = "ui_update"
    )
    permission.create_permission(
        name = "institution_index"
    )
    permission.create_permission(
        name = "institution_create"
    )
    permission.create_permission(
        name = "institution_destroy"
    )
    permission.create_permission(
        name = "institution_update"
    )
    permission.create_permission(
        name = "institution_show"
    )
    permission.create_permission(
        name = "institution_activate"
    )
    permission.create_permission(
        name = "institution_deactivate"
    )
    permission.create_permission(
        name = "service_index"
    )
    permission.create_permission(
        name = "service_create"
    )
    permission.create_permission(
        name = "service_destroy"
    )
    permission.create_permission(
        name = "service_update"
    )
    permission.create_permission(
        name = "service_show"
    )
    permission.create_permission(
        name = "request_service_index"
    )
    permission.create_permission(
        name = "request_service_create"
    )
    permission.create_permission(
        name = "request_service_destroy"
    )
    permission.create_permission(
        name = "request_service_update"
    )
    permission.create_permission(
        name = "request_service_show"
    )
    permission.create_permission(
        name = "system_show"
    )
    permission.create_permission(
        name = "system_update"
    )
    print("----> Finalizado! <----")

def assign_permissions_to_roles():
    print("----> Asignando permisos a roles...")
    # Permisos
    users_permission = permission.get_permission_by_prefix("user")
    users_institution_permission = permission.get_permission_by_prefix("ui")
    institution_permission = permission.get_permission_by_prefix("institution")
    service_permission = permission.get_permission_by_prefix("service")
    request_service_permission = permission.get_permission_by_prefix("request")
    system_permission = permission.get_permission_by_prefix("system")
    
    # SuperAdministrador
    superAdmin = role.get_role_by_name("SuperAdministrador/a")
    permission_superAdmin = []
    for lista in [users_permission, institution_permission, service_permission, system_permission]:
        permission_superAdmin += lista
    role.assign_permission(superAdmin, permission_superAdmin)
    
    # Dueño
    permission_owner = []
    for lista in [users_institution_permission,
                  service_permission,
                  [p for p in request_service_permission if p.name != "request_service_create"]]:
        permission_owner += lista
    owner = role.get_role_by_name("Dueño/a")
    role.assign_permission(owner, permission_owner)
    
    # Administrador
    admin = role.get_role_by_name("Administrador/a")
    permission_admin = []
    for lista in [service_permission, request_service_permission]:
        permission_admin += lista
    role.assign_permission(admin, permission_admin)
    
    # Operador
    operator = role.get_role_by_name("Operador/a")
    permission_operator = []
    for lista in [[p for p in service_permission if p.name != "service_destroy"],
                  [p for p in request_service_permission if p.name != "request_service_destroy"]]:
        permission_operator += lista
    role.assign_permission(operator, permission_operator)
    
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
    ui_user021 = user_institution.create_user_institution_role(
        user = user02,
        institution = i0,
        role = operator
    )
    
    user.assign_institution_and_role(root, [ui_root])
    user.assign_institution_and_role(user00, [ui_user00])
    user.assign_institution_and_role(user01, [ui_user01])
    user.assign_institution_and_role(user02, [ui_user02])
    user.assign_institution_and_role(user02, [ui_user021])
    print("----> Finalizado! <----")

def run():
    create_system()
    create_users()
    create_institutions_and_services()
    create_roles()
    create_permissions()
    assign_permissions_to_roles()
    assign_roles_to_users()