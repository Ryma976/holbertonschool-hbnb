from flask import Flask
from flask_restx import Api
from config import config

def create_app(config_class="default"):
    app = Flask(__name__)
    
    if isinstance(config_class, str):
        app.config.from_object(config.get(config_class, config['default']))
    else:
        app.config.from_object(config_class)

    api = Api(app, version='1.0', title='HBnB API', description='HBnB Application API')

    return app
