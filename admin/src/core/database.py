from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_app(app):
    """
    Inicializacion de la aplicacion.
    """
    db.init_app(app)
    config_db(app)


def config_db(app):
    """
    Configuracion de la aplicacion.
    """
    @app.teardown_request
    def close_session(exception=None):
        db.session.close()

def reset_db():
    print("Eliminando la base de datos...")
    db.drop_all()
    print("Creando la base de datos...")
    db.create_all()
    print("Finalizado!")