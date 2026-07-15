from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace('places', description='Place operations')

# موديلات مخصصة لعرض البيانات بشكل متداخل متكامل (Nested Serialization)
user_sub_model = api.model('PlaceOwner', {
    'id': fields.String(description='Owner ID'),
    'first_name': fields.String(description='First name'),
    'last_name': fields.String(description='Last name'),
    'email': fields.String(description='Email')
})

amenity_sub_model = api.model('PlaceAmenity', {
    'id': fields.String(description='Amenity ID'),
    'name': fields.String(description='Amenity name')
})

place_request_model = api.model('PlaceRequest', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude'),
    'longitude': fields.Float(required=True, description='Longitude'),
    'owner_id': fields.String(required=True, description='ID of the owner')
})

place_response_model = api.model('PlaceResponse', {
    'id': fields.String(description='The place unique identifier'),
    'title': fields.String(description='Title'),
    'description': fields.String(description='Description'),
    'price': fields.Float(description='Price per night'),
    'latitude': fields.Float(description='Latitude'),
    'longitude': fields.Float(description='Longitude'),
    'owner': fields.Nested(user_sub_model, description='Owner details'),
    'amenities': fields.List(fields.Nested(amenity_sub_model), description='List of amenities')
})

@api.route('/')
class PlaceList(Resource):
    @api.expect(place_request_model, validate=True)
    def post(self):
        """إنشاء مكان جديد"""
        try:
            new_place = facade.create_place(api.payload)
            # دمج تفاصيل المالك ديناميكياً لإرجاع البيانات كاملة
            owner = facade.get_user(new_place.owner_id)
            response_data = {
                'id': new_place.id, 'title': new_place.title, 'description': new_place.description,
                'price': new_place.price, 'latitude': new_place.latitude, 'longitude': new_place.longitude,
                'owner': {'id': owner.id, 'first_name': owner.first_name, 'last_name': owner.last_name, 'email': owner.email},
                'amenities': []
            }
            return response_data, 201
        except ValueError as e:
            return {'error': str(e)}, 400

    def get(self):
        """جلب كل الأماكن مع تفاصيل الملاك والمميزات"""
        all_places = facade.get_all_places()
        results = []
        for p in all_places:
            owner = facade.get_user(p.owner_id)
            amenities = [facade.get_amenity(am_id) for am_id in p.amenities if facade.get_amenity(am_id)]
            results.append({
                'id': p.id, 'title': p.title, 'description': p.description, 'price': p.price,
                'latitude': p.latitude, 'longitude': p.longitude,
                'owner': {'id': owner.id, 'first_name': owner.first_name, 'last_name': owner.last_name, 'email': owner.email} if owner else None,
                'amenities': [{'id': am.id, 'name': am.name} for am in amenities]
            })
        return results, 200

@api.route('/<string:place_id>')
@api.response(404, 'Place not found')
class PlaceResource(Resource):
    def get(self, place_id):
        """جلب تفاصيل مكان محدد بالتفصيل مع المميزات والمراجعات"""
        p = facade.get_place(place_id)
        if not p:
            api.abort(404, "Place not found")
        owner = facade.get_user(p.owner_id)
        amenities = [facade.get_amenity(am_id) for am_id in p.amenities if facade.get_amenity(am_id)]
        response_data = {
            'id': p.id, 'title': p.title, 'description': p.description, 'price': p.price,
            'latitude': p.latitude, 'longitude': p.longitude,
            'owner': {'id': owner.id, 'first_name': owner.first_name, 'last_name': owner.last_name, 'email': owner.email} if owner else None,
            'amenities': [{'id': am.id, 'name': am.name} for am in amenities]
        }
        return response_data, 200

    @api.expect(place_request_model, validate=True)
    def put(self, place_id):
        """تحديث بيانات مكان محدد"""
        p = facade.get_place(place_id)
        if not p:
            api.abort(404, "Place not found")
        try:
            updated_place = facade.update_place(place_id, api.payload)
            owner = facade.get_user(updated_place.owner_id)
            response_data = {
                'id': updated_place.id, 'title': updated_place.title, 'description': updated_place.description,
                'price': updated_place.price, 'latitude': updated_place.latitude, 'longitude': updated_place.longitude,
                'owner': {'id': owner.id, 'first_name': owner.first_name, 'last_name': owner.last_name, 'email': owner.email} if owner else None,
                'amenities': []
            }
            return response_data, 200
        except ValueError as e:
            return {'error': str(e)}, 400
