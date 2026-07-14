from flask import request
from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace('users', description='User operations')

# تعريف شكل البيانات (Serialization Model) لعرضها بشكل منظم في السواجر وإرجاعها للمستخدم
user_model = api.model('User', {
    'id': fields.String(readOnly=True, description='The user unique identifier'),
    'first_name': fields.String(required=True, description='User first name'),
    'last_name': fields.String(required=True, description='User last name'),
    'email': fields.String(required=True, description='User email address')
})

@api.route('/')
class UserList(Resource):
    @api.expect(user_model, validate=True)
    @api.marshal_with(user_model, code=201)
    def post(self):
        """إنشاء مستخدم جديد"""
        user_data = api.payload
        try:
            new_user = facade.create_user(user_data)
            return new_user, 201
        except ValueError as e:
            return {'error': str(e)}, 400

    @api.marshal_list_with(user_model)
    def get(self):
        """جلب قائمة بجميع المستخدمين"""
        return facade.get_all_users(), 200


@api.route('/<string:user_id>')
@api.response(404, 'User not found')
class UserResource(Resource):
    @api.marshal_with(user_model)
    def get(self, user_id):
        """جلب مستخدم محدد بواسطة معرف الـ ID"""
        user = facade.get_user(user_id)
        if not user:
            api.abort(404, "User not found")
        return user, 200

    @api.expect(user_model, validate=True)
    @api.marshal_with(user_model)
    def put(self, user_id):
        """تحديث بيانات مستخدم محدد"""
        user_data = api.payload
        user = facade.get_user(user_id)
        if not user:
            api.abort(404, "User not found")
        
        try:
            updated_user = facade.update_user(user_id, user_data)
            return updated_user, 200
        except ValueError as e:
            return {'error': str(e)}, 400
