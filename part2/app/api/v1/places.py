from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace('places', description='Place operations')

amenity_model = api.model('PlaceAmenity', {
    'id': fields.String(description='Amenity ID'),
    'name': fields.String(description='Name of the amenity')
})

owner_model = api.model('PlaceOwner', {
    'id': fields.String(description='Owner ID'),
    'first_name': fields.String(description='First name'),
    'last_name': fields.String(description='Last name'),
    'email': fields.String(description='Email address')
})

place_model = api.model('Place', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude coordinate'),
    'longitude': fields.Float(required=True, description='Longitude coordinate'),
    'owner_id': fields.String(required=True, description='ID of the owner (User)'),
    'amenity_ids': fields.List(fields.String, description='List of Amenity IDs')
})

@api.route('/')
class PlaceList(Resource):
    @api.expect(place_model)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Create a new place"""
        data = api.payload
        try:
            new_place = facade.create_place(data)
            return {
                'id': new_place.id,
                'title': new_place.title,
                'description': new_place.description,
                'price': new_place.price,
                'latitude': new_place.latitude,
                'longitude': new_place.longitude,
                'owner_id': new_place.owner_id
            }, 201
        except ValueError as e:
            return {'error': str(e)}, 400

    @api.response(200, 'Success')
    def get(self):
        """List all places"""
        places = facade.get_all_places()
        return [{
            'id': p.id,
            'title': p.title,
            'price': p.price,
            'latitude': p.latitude,
            'longitude': p.longitude
        } for p in places], 200

@api.route('/<string:place_id>')
@api.response(404, 'Place not found')
class PlaceResource(Resource):
    @api.response(200, 'Success')
    def get(self, place_id):
        """Get place details by ID with owner and amenities details"""
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404

        owner = facade.get_user(place.owner_id)
        amenities_list = [facade.get_amenity(aid) for aid in place.amenities]

        return {
            'id': place.id,
            'title': place.title,
            'description': place.description,
            'price': place.price,
            'latitude': place.latitude,
            'longitude': place.longitude,
            'owner': {
                'id': owner.id,
                'first_name': owner.first_name,
                'last_name': owner.last_name,
                'email': owner.email
            } if owner else None,
            'amenities': [{
                'id': am.id,
                'name': am.name,
                'description': am.description
            } for am in amenities_list if am]
        }, 200

    @api.expect(place_model)
    @api.response(200, 'Place successfully updated')
    @api.response(400, 'Invalid input data')
    def put(self, place_id):
        """Update place details"""
        data = api.payload
        try:
            updated_place = facade.update_place(place_id, data)
            return {'message': 'Place successfully updated'}, 200
        except ValueError as e:
            return {'error': str(e)}, 400
