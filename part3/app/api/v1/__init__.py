from flask import request
from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace('amenities', description='Amenity operations')

amenity_model = api.model('Amenity', {
    'id': fields.String(readOnly=True, description='The unique identifier'),
    'name': fields.String(required=True, description='Name of the amenity')
})

@api.route('/')
class AmenityList(Resource):
    @api.expect(amenity_model, validate=True)
    @api.marshal_with(amenity_model, code=201)
    def post(self):
        """إنشاء ميزة جديدة"""
        try:
            new_amenity = facade.create_amenity(api.payload)
            return new_amenity, 201
        except ValueError as e:
            return {'error': str(e)}, 400

    @api.marshal_list_with(amenity_model)
    def get(self):
        """جلب كل المميزات"""
        return facade.get_all_amenities(), 200

@api.route('/<string:amenity_id>')
@api.response(404, 'Amenity not found')
class AmenityResource(Resource):
    @api.marshal_with(amenity_model)
    def get(self, amenity_id):
        """جلب ميزة محددة بالـ ID"""
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            api.abort(404, "Amenity not found")
        return amenity, 200

    @api.expect(amenity_model, validate=True)
    @api.marshal_with(amenity_model)
    def put(self, amenity_id):
        """تحديث بيانات ميزة محددة"""
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            api.abort(404, "Amenity not found")
        try:
            updated_amenity = facade.update_amenity(amenity_id, api.payload)
            return updated_amenity, 200
        except ValueError as e:
            return {'error': str(e)}, 400
