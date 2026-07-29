from flask import Flask
from flask_restx import Api
from flask_bcrypt import Bcrypt
from config import config

bcrypt = Bcrypt()

def create_app(config_class="default"):
    app = Flask(__name__)
    
    if isinstance(config_class, str):
        app.config.from_object(config.get(config_class, config['default']))
    else:
        app.config.from_object(config_class)

    bcrypt.init_app(app)

    api = Api(app, version='1.0', title='HBnB API', description='HBnB Application API')

    from app.api.v1.users import api as users_ns
    api.add_namespace(users_ns, path='/api/v1/users')

    return app
