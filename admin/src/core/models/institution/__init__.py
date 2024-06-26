from src.core.models.institution.institution import Institution
from src.core.models.institution.service import Service
from src.core.models.institution.service import TypeService
from src.core.models import system
from src.core.models import role
from src.core.models import user
from src.core.models.user.user import User
from src.core.models.role.role import Role
from src.core.models.user_institution import UserInstitution
from src.core.database import db
from sqlalchemy import or_
from flask import redirect, url_for,render_template

def list_institutions():
    """
    Me devuelve todas las instituciones.
    """   
    institutions = Institution.query.all()
    return institutions

def list_institutions_paginated(page, per_page):
    """
    Me devuelve todas las instituciones.
    """
    institutions = Institution.query.filter(Institution.name != "CIDEPINT").paginate(page=page, per_page=per_page, error_out=False)
    return institutions, institutions.pages

def total_intitutions_pages(per_page):
    """
    Me devuelve la cantidad de paginas que ocupan las instituciones.
    """  # Cantidad de instituciones por página
    total_institutions = Institution.query.count()  # Total de instituciones
    if(total_institutions == 0):
        return 1
    total_pages = (total_institutions + per_page - 1)// per_page  # Cálculo de páginas
    return total_pages
    

def get_institution_by_id(id):
    """
    Me devuelve una institucion por id.
    """   
    institution = Institution.query.filter(Institution.id == id).first()
    return institution

def get_institution_by_name(name):
    """
    Me devuelve una institucion por id.
    """   
    institution = Institution.query.filter(Institution.name.lower() == name.lower()).first()
    return institution

def create_institution(**kwargs):
    """"
    Crear una institucion y almacenarla en la db.
    """
    institution = Institution(**kwargs)
    db.session.add(institution)
    db.session.commit()

    return institution

def delete_institution(institution):
    db.session.delete(institution)
    db.session.commit()
    
def edit_institution(institution, **kwargs):
    for key, value in kwargs.items():
        setattr(institution, key, value) 
        
    db.session.add(institution)
    db.session.commit()
    
    return institution
    
def check_if_institution_exists_by_name(name):
    institution = Institution.query.filter(Institution.name == name).first()
    return institution is not None


def assign_service(institution, service):
    service.institution = institution
    db.session.add(service)
    db.session.commit()

    return service

def list_services():
    """
    Me devuelve todos los servicios
    """   
    services = Service.query.all()
    return services

def list_services_by_institution(institution_id):
    """
    Me devuelve todos los servicios de una institucion
    """   
    services = Service.query.filter(Service.institution_id == institution_id).all()
    
    return services

def list_services_by_intitution_paginated(institution_id, page, per_page):
    """
    Me devuelve todos los servicios de una institucion paginados
    """
    services = Service.query.filter(Service.institution_id == institution_id).paginate(page=page, per_page=per_page, error_out=False)

    return services, services.pages

def total_services_pages(institution_id, per_page):
    """
    Me devuelve la cantidad de paginas que ocupan las instituciones.
    """
    services = Service.query.filter(Service.institution_id == institution_id).all()  # Total de servicios
    total_services = len(services)
    if(total_services == 0):
        return 1
    total_pages = ((total_services + per_page) - 1)// per_page  # Cálculo de páginas
    
    return total_pages

def create_service(**kwargs):
    """"
    Crear un servicio y almacenarla en la db.
    """
    service = Service(**kwargs)
    db.session.add(service)
    db.session.commit()
    return service

def get_service_by_id(id):
    """
    Me devuelve un servicio por id.
    """   
    service = Service.query.filter(Service.id == id).first()
    return service

def delete_service(service):

    institution = Institution.query.filter(Institution.id == service.institution_id).first()
    institution.services.remove(service)
    db.session.delete(service)
    db.session.commit()

def edit_service(service, **kwargs):
    institution = Institution.query.filter(Institution.id == service.institution_id).first()
    institution.services.remove(service)
    
    for key, value in kwargs.items():
        setattr(service, key, value)
    
    institution.services.append(service)
    db.session.add(service)
    db.session.add(institution)
    db.session.commit()
    
    return service

def get_service_by_name_and_institution(name, institution_id):
    """
    Me devuelve un servicio por nombre e institucion.
    """   
    service = Service.query.filter(Service.name == name, Service.institution_id == institution_id).first()
    return service

def get_service_by_name(name):
    """
    Me devuelve un servicio por nombre.
    """   
    service = Service.query.filter(Service.name == name).first()
    return service

def check_if_service_exists_by_name_update(institution_id, name,id):
    service = Service.query.filter(Service.name == name, Service.institution_id == institution_id, Service.id != id).first()
    return service is not None

def check_if_service_exists_by_name_create(institution_id, name):
    service = Service.query.filter(Service.name == name, Service.institution_id == institution_id).first()
    return service is not None

def get_institution_by_name(name):
    """
        Retorna una institucion por su nombre
    """
    return Institution.query.filter_by(name=name).first()

def list_users_from_institution(institution_id, page, query, active):
    """
    Me devuelve todos los usuarios de una institucion
    """
    role_root = role.get_role_by_name("SuperAdministrador/a")
    user_root = UserInstitution.query.filter(UserInstitution.role_id == role_root.id).first()

    usuarios_en_institucion = UserInstitution.query.filter(UserInstitution.institution_id == institution_id).paginate(page=page, per_page=system.pages(), error_out=False)
    
    users = []
    for ui in usuarios_en_institucion:
            u = User.query.filter(User.id == ui.user_id).first()
            r = Role.query.filter(Role.id == ui.role_id).first()
            users.append({
                "id": ui.user_id,
                "username": u.username,
                "email": u.email,
                "role": r.name,
                "active": u.active,
                "inserted_at": ui.inserted_at
            })

    return users,usuarios_en_institucion.pages

    #return usuarios_en_institucion, usuarios_en_institucion.pages
    

    # if institution:
    #     users = []
    #     # Accede a los usuarios de la institución a través de la relación 'users' en el modelo Institution
    #     for user_institution in institution.users:
    #         user = user_institution.user
    #         role = user_institution.role
            
    #         users.append({
    #             "id": user.id,
    #             "username": user.username,
    #             "email": user.email,
    #             "role": role.name,
    #             "active": user.active,
    #             "inserted_at": user_institution.inserted_at
    #         })
    #     return users
    # return None

def list_users_not_in_institution(institution_id, query, page, active):
    """
    Retorna los usuarios que no están en la institución.
    """
    role_root = role.get_role_by_name("SuperAdministrador/a")
    user_root = UserInstitution.query.filter(UserInstitution.role_id == role_root.id).first()

    # Realiza una consulta para obtener los IDs de los usuarios en la institución
    subquery = db.session.query(UserInstitution.user_id).filter(UserInstitution.institution_id == institution_id).subquery().select()

    # Realiza una consulta para obtener los usuarios que NO están en la institución
    # usuarios_no_en_institucion = User.query.filter(User.id != user_root.id, User.id.notin_(subquery)).paginate(page=page, per_page=system.pages(), error_out=False)
    if active == "":
        usuarios_no_en_institucion = User.query.filter(User.id != user_root.id, User.id.notin_(subquery), or_(User.email.ilike(f"%{query}%"))).paginate(page=page, per_page=system.pages(), error_out=False)
    else:
        usuarios_no_en_institucion = User.query.filter(User.id != user_root.id, User.active == active, User.id.notin_(subquery), or_(User.email.ilike(f"%{query}%"))).paginate(page=page, per_page=system.pages(), error_out=False)

    return usuarios_no_en_institucion, usuarios_no_en_institucion.pages

def services_serch(substr, page, per_page, tipo):
    """
        Retorna los servicios que coincidan con la búsqueda por substring.
    """
    if(tipo != ""):
        tipo = int(tipo)
        services = Service.query.filter( or_(Service.name.ilike(f"%{substr}%"),Service.info.ilike(f"%{substr}%"), Service.key_words.ilike(f"%{substr}%")) , Service.is_enabled , Service.type_service_id == tipo).paginate(page=page, per_page=per_page, error_out=False)
    else:
        services = Service.query.filter( or_(Service.name.ilike(f"%{substr}%"),Service.info.ilike(f"%{substr}%"), Service.key_words.ilike(f"%{substr}%")) , Service.is_enabled).paginate(page=page, per_page=per_page, error_out=False)
    return services


def total_services_pages_for_search(substr, page, per_page,tipo):
    """
    Me devuelve la cantidad de paginas que ocupan los servicios coincidentes con el substr.
    """
    services = services_serch(substr, page, per_page,tipo)  # Total de servicios
    total_services = services.total
    if(total_services == 0):
        return 1
    total_pages = ((total_services + per_page) - 1)// per_page  # Cálculo de páginas
    
    return total_pages

def create_type_service(**kwargs):
    """"
    Crear un tipo de servicio.
    """
    type_service = TypeService(**kwargs)
    db.session.add(type_service)
    db.session.commit()
    return type_service

def index_type_service():
    """
    Me devuelve todos los tipos de servicios
    """   
    types_service = TypeService.query.all()
    return types_service

def get_type_service_by_name(name):
    """
    Me devuelve un tipo de servicio por nombre.
    """   
    type_service = TypeService.query.filter(TypeService.name == name).first()
    return type_service


def get_type_service_by_id(id):
    """
    Me devuelve un tipo de servicio por id.
    """   
    type_service = TypeService.query.filter(TypeService.id == id).first()
    return type_service