from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_restx import Api
from flask_cors import CORS  # 1. أضفنا استدعاء مكتبة CORS

db = SQLAlchemy()
bcrypt = Bcrypt()
jwt = JWTManager()

def create_app(config_class="config.DevelopmentConfig"):
    flask_app = Flask(__name__)
    flask_app.config.from_object(config_class)

    # 2. أضفنا تفعيل الـ CORS لتسمح للفرونت إند بالتواصل مع الباك إند
    CORS(flask_app, supports_credentials=True)

    db.init_app(flask_app)
    bcrypt.init_app(flask_app)
    jwt.init_app(flask_app)

    api = Api(flask_app, version='1.0', title='HBnB API', description='HBnB Application API', doc='/api/v1/endpoints/')

    # Register Namespaces/Blueprints
    from app.api.v1.users import api as users_ns
    from app.api.v1.places import api as places_ns
    from app.api.v1.reviews import api as reviews_ns
    from app.api.v1.amenities import api as amenities_ns
    from app.api.v1.auth import api as auth_ns

    api.add_namespace(users_ns, path='/api/v1/users')
    api.add_namespace(places_ns, path='/api/v1/places')
    api.add_namespace(reviews_ns, path='/api/v1/reviews')
    api.add_namespace(amenities_ns, path='/api/v1/amenities')
    api.add_namespace(auth_ns, path='/api/v1/auth')

    return flask_app
