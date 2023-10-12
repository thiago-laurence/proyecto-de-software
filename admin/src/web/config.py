from os import environ

class Config(object):
    """
        Configuracion base
    """
    
    # Configuracion de seguridad de la aplicacion
    SECRET_KEY = "Grupo10-app"
    TESTING = False
    SESSION_TYPE = "filesystem"
    SECURITY_PASSWORD_SALT = "Grupo10-pass"
    
    # Credenciales para servicio de correo
    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USE_TLS = False
    MAIL_USERNAME = "cidepintgrupo10@gmail.com"
    MAIL_PASSWORD = "nhct ysgd jpau uixe"
    MAIL_DEFAULT_SENDER = "CIDEPINT cidepintgrupo10@gmail.com"
    
    # Configuracion de seguridad para formularios WTF
    WTF_CSRF_ENABLED = False
    
class ProductionConfig(Config):
    """ configuracion de prod """
    
    DB_USER = environ.get("DB_USER")
    DB_PASS = environ.get("DB_PASS")
    DB_HOST = environ.get("DB_HOST")
    DB_NAME = environ.get("DB_NAME")
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_DATABASE_URI = (
        f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:5432/{DB_NAME}"
    ) 

class DevelopmentConfig(Config):
    """ configuracion de develop """
    DB_USER = environ.get("DB_USER")
    DB_PASS = environ.get("DB_PASS")
    DB_HOST = environ.get("DB_HOST")
    DB_NAME = environ.get("DB_NAME")
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_DATABASE_URI = (
        f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:5432/{DB_NAME}"
    ) 

class TestingConfig(Config):
    """ configuracion de testing """
    
    TESTING = True
    
config = {
    "development":DevelopmentConfig,
    "production":ProductionConfig,
    "test":TestingConfig,
}