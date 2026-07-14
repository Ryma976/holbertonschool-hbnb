from flask import Flask
from flask_restx import Api
from app.services.facade import HBnBFacade

facade = HBnBFacade()

def create_app():
    app = Flask(__name__)
    api = Api(app, version='1.0', title='HBnB API', description='HBnB Evolution Application API')

    # Register only places namespace for now
    from app.api.v1.places import api as places_ns
    api.add_namespace(places_ns, path='/api/v1/places')

    return app
