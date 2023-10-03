from src.core.models.institution.institution import Institution
from src.core.models.institution.service import Service
from src.core.database import db

def list_institutions():
    """
    Me devuelve todas las instituciones.
    """   
    institutions = Institution.query.all()
    return institutions

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
    institution.name = kwargs.get("name")
    institution.info = kwargs.get("info")
    institution.address = kwargs.get("address")
    institution.web = kwargs.get("web")
    institution.social_networks = kwargs.get("social_networks")
    institution.phone = kwargs.get("phone")
    
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
    print(services)
    return services

def list_services_by_institution(institution_id):
    """
    Me devuelve todos los servicios de una institucion
    """   
    services = Service.query.filter(Service.institution_id == institution_id).all()
    print(services)
    return services

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
    
    service.name = kwargs.get("name")
    service.info = kwargs.get("info")
    service.type = kwargs.get("type")
    service.key_words = kwargs.get("key_words")
    
    institution.services.append(service)
    db.session.add(service)
    db.session.add(institution)
    db.session.commit()
    
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