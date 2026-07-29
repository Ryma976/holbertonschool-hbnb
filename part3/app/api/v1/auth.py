from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import create_access_token
from app.services.facade import facade

api = Namespace('auth', description='Authentication operations')

login_model = api.model('Login', {
    'email': fields.String(required=True, description='User email'),
    'password': fields.String(required=True, description='User password')
})

@api.route('/login')
class Login(Resource):
    @api.expect(login_model, validate=True)
    def post(self):
        """Authenticate user and return JWT access token"""
        credentials = api.payload
        email = credentials.get('email')
        password = credentials.get('password')

        user = facade.get_user_by_email(email)
        if not user or not user.verify_password(password):
            return {'error': 'Invalid credentials'}, 401

        # Embed is_admin claim into token
        additional_claims = {'is_admin': user.is_admin}
        access_token = create_access_token(identity=user.id, additional_claims=additional_claims)

        return {'access_token': access_token}, 200
