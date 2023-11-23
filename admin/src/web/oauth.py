from authlib.integrations.flask_client import OAuth
from pathlib import Path

oauth = OAuth()

def init_app(app):
    CONF_URL = 'https://accounts.google.com/.well-known/openid-configuration'
    oauth.init_app(app)
    oauth.register(
        name='google',
        server_metadata_url=CONF_URL,
        client_kwargs={
            'scope': 'openid email profile'
        }
    )