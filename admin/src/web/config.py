from os import environ

class Config(object):
    """
        configuracion base.
        
    """
    SECRET_KEY = "secret"
    TESTING = False
    SESSION_TYPE = "filesystem"
    
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