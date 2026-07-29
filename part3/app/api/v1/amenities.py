from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt
from app.services.facade import facade

api = Namespace('amenities', description='Amenity operations')

amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Name of the amenity')
})

@api.route('/')
class AmenityList(Resource):
    def get(self):
        """Retrieve all amenities (Public)"""
        amenities = facade.get_all_amenities()
        return [a.to_dict() for a in amenities], 200

    @api.expect(amenity_model, validate=True)
    @jwt_required()
    def post(self):
        """Create a new amenity (Admin Only)"""
        claims = get_jwt()
        if not claims.get('is_admin', False):
            return {'error': 'Admin rights required'}, 403

        amenity_data = api.payload
        try:
            new_amenity = facade.create_amenity(amenity_data)
            return new_amenity.to_dict(), 201
        except ValueError as e:
            return {'error': str(e)}, 400

@api.route('/<amenity_id>')
class AmenityResource(Resource):
    def get(self, amenity_id):
        """Get amenity details by ID (Public)"""
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {'error': 'Amenity not found'}, 404
        return amenity.to_dict(), 200

    @api.expect(amenity_model, validate=False)
    @jwt_required()
    def put(self, amenity_id):
        """Update amenity details (Admin Only)"""
        claims = get_jwt()
        if not claims.get('is_admin', False):
            return {'error': 'Admin rights required'}, 403

        amenity_data = api.payload
        updated_amenity = facade.update_amenity(amenity_id, amenity_data)
        if not updated_amenity:
            return {'error': 'Amenity not found'}, 404
        return updated_amenity.to_dict(), 200
