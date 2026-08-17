from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.services.facade import facade

api = Namespace('places', description='Place operations')

place_model = api.model('Place', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude'),
    'longitude': fields.Float(required=True, description='Longitude')
})

@api.route('/')
class PlaceList(Resource):
    def get(self):
        """Retrieve all places (Public)"""
        places = facade.get_all_places()
        return [p.to_dict() for p in places], 200

    @api.expect(place_model, validate=True)
    @jwt_required()
    def post(self):
        """Create a new place (Authenticated User)"""
        current_user_id = get_jwt_identity()
        place_data = api.payload
        try:
            new_place = facade.create_place(place_data, owner_id=current_user_id)
            return new_place.to_dict(), 201
        except ValueError as e:
            return {'error': str(e)}, 400

@api.route('/<place_id>')
class PlaceResource(Resource):
    def get(self, place_id):
        """Get place details by ID (Public)"""
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404
        return place.to_dict(), 200

    @api.expect(place_model, validate=False)
    @jwt_required()
    def put(self, place_id):
        """Update place details (Owner or Admin)"""
        current_user_id = get_jwt_identity()
        claims = get_jwt()
        is_admin = claims.get('is_admin', False)

        place_data = api.payload
        updated_place, error = facade.update_place(place_id, place_data, current_user_id, is_admin=is_admin)
        if error == "Place not found":
            return {'error': error}, 404
        if error == "Unauthorized action":
            return {'error': 'Unauthorized action'}, 403
        return updated_place.to_dict(), 200

    @jwt_required()
    def delete(self, place_id):
        """Delete place (Owner or Admin)"""
        current_user_id = get_jwt_identity()
        claims = get_jwt()
        is_admin = claims.get('is_admin', False)

        success, error = facade.delete_place(place_id, current_user_id, is_admin=is_admin)
        if error == "Place not found":
            return {'error': error}, 404
        if error == "Unauthorized action":
            return {'error': 'Unauthorized action'}, 403
        return {'message': 'Place deleted successfully'}, 200
