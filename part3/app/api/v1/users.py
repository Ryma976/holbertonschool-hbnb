from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.services.facade import facade

api = Namespace('users', description='User operations')

user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name'),
    'last_name': fields.String(required=True, description='Last name'),
    'email': fields.String(required=True, description='Email address'),
    'password': fields.String(required=True, description='User password'),
    'is_admin': fields.Boolean(description='Admin status', default=False)
})

user_output_model = api.model('UserOutput', {
    'id': fields.String(description='User ID'),
    'first_name': fields.String(description='First name'),
    'last_name': fields.String(description='Last name'),
    'email': fields.String(description='Email address'),
    'is_admin': fields.Boolean(description='Admin status')
})

@api.route('/')
class UserList(Resource):
    @api.expect(user_model, validate=True)
    def post(self):
        """Register a new user"""
        user_data = api.payload
        try:
            new_user = facade.create_user(user_data)
            return new_user.to_dict(), 201
        except ValueError as e:
            return {'error': str(e)}, 400

    @api.marshal_list_with(user_output_model)
    def get(self):
        """Retrieve a list of all users"""
        users = facade.get_all_users()
        return [user.to_dict() for user in users], 200

@api.route('/<user_id>')
class UserResource(Resource):
    @api.marshal_with(user_output_model)
    def get(self, user_id):
        """Get user details by ID"""
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        return user.to_dict(), 200

    @api.expect(user_model, validate=False)
    @jwt_required()
    def put(self, user_id):
        """Update user details (Admin or Account Owner)"""
        current_user_id = get_jwt_identity()
        claims = get_jwt()
        is_admin = claims.get('is_admin', False)

        user_data = api.payload
        try:
            updated_user, error = facade.update_user(user_id, user_data, is_admin=is_admin, current_user_id=current_user_id)
            if error == "User not found":
                return {'error': error}, 404
            if error == "Unauthorized action":
                return {'error': 'Admin rights required or unauthorized'}, 403
            return updated_user.to_dict(), 200
        except ValueError as e:
            return {'error': str(e)}, 400
