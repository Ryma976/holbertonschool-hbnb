from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace('reviews', description='Review operations')

review_request_model = api.model('ReviewRequest', {
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=True, description='Rating (1-5)'),
    'place_id': fields.String(required=True, description='Place ID'),
    'user_id': fields.String(required=True, description='User ID')
})

review_response_model = api.model('ReviewResponse', {
    'id': fields.String(description='The review unique identifier'),
    'text': fields.String(description='Review text'),
    'rating': fields.Integer(description='Rating'),
    'place_id': fields.String(description='Place ID'),
    'user_id': fields.String(description='User ID')
})

@api.route('/')
class ReviewList(Resource):
    @api.expect(review_request_model, validate=True)
    @api.marshal_with(review_response_model, code=201)
    def post(self):
        """إضافة مراجعة وتقييم جديد لمكان"""
        try:
            new_review = facade.create_review(api.payload)
            return new_review, 201
        except ValueError as e:
            return {'error': str(e)}, 400

    @api.marshal_list_with(review_response_model)
    def get(self):
        """جلب كل المراجعات في النظام"""
        return facade.get_all_reviews(), 200

@api.route('/<string:review_id>')
@api.response(404, 'Review not found')
class ReviewResource(Resource):
    @api.marshal_with(review_response_model)
    def get(self, review_id):
        """جلب مراجعة محددة بالـ ID"""
        review = facade.get_review(review_id)
        if not review:
            api.abort(404, "Review not found")
        return review, 200

    @api.expect(review_request_model, validate=True)
    @api.marshal_with(review_response_model)
    def put(self, review_id):
        """تحديث بيانات مراجعة محددة"""
        review = facade.get_review(review_id)
        if not review:
            api.abort(404, "Review not found")
        try:
            updated_review = facade.update_review(review_id, api.payload)
            return updated_review, 200
        except ValueError as e:
            return {'error': str(e)}, 400

    def delete(self, review_id):
        """حذف مراجعة"""
        deleted = facade.delete_review(review_id)
        if not deleted:
            api.abort(404, "Review not found")
        return {'message': 'Review deleted successfully'}, 200
