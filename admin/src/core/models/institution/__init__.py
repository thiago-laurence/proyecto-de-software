from src.core.models.institution.institution import Institution
from src.core.models.institution.service import Service
from src.core.database import db

def list_institutions():
    """
    Me devuelve todas las instituciones.
    """   
    institutions = Institution.query.all()
    return institutions

def create_institution(**kwargs):
    """"
    Crear una institucion y almacenarla en la db.
    """
    institution = Institution(**kwargs)
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

def create_service(**kwargs):
    """"
    Crear un servicio y almacenarla en la db.
    """
    service = Service(**kwargs)
    db.session.add(service)
    db.session.commit()
    return service

def get_institution_by_name(name):
    """
        Retorna una institucion por su nombre
    """
    return Institution.query.filter_by(name=name).first()