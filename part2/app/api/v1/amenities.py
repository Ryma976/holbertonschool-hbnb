from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace('amenities', description='Amenity operations')

amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Name of the amenity'),
    'description': fields.String(description='Description of the amenity')
})

@api.route('/')
class AmenityList(Resource):
    @api.expect(amenity_model, validate=True)
    @api.response(201, 'Amenity successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Create a new amenity"""
        amenity_data = api.payload
        try:
            new_amenity = facade.create_amenity(amenity_data)
            return {
                'id': new_amenity.id,
                'name': new_amenity.name,
                'description': new_amenity.description
            }, 201
        except ValueError as e:
            return {'error': str(e)}, 400

    @api.response(200, 'Success')
    def get(self):
        """Retrieve list of all amenities"""
        amenities = facade.get_all_amenities()
        return [{
            'id': a.id,
            'name': a.name,
            'description': a.description
        } for a in amenities], 200

@api.route('/<string:amenity_id>')
@api.response(404, 'Amenity not found')
class AmenityResource(Resource):
    @api.response(200, 'Success')
    def get(self, amenity_id):
        """Get amenity details by ID"""
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {'error': 'Amenity not found'}, 404
        return {
            'id': amenity.id,
            'name': amenity.name,
            'description': amenity.description
        }, 200

    @api.expect(amenity_model, validate=True)
    @api.response(200, 'Amenity successfully updated')
    @api.response(400, 'Invalid input data')
    def put(self, amenity_id):
        """Update amenity details"""
        amenity_data = api.payload
        try:
            facade.update_amenity(amenity_id, amenity_data)
            return {'message': 'Amenity successfully updated'}, 200
        except ValueError as e:
            return {'error': str(e)}, 400
