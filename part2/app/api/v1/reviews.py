from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace('reviews', description='Review operations')

review_model = api.model('Review', {
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=True, description='Rating (1-5)'),
    'user_id': fields.String(required=True, description='ID of the user'),
    'place_id': fields.String(required=True, description='ID of the place')
})

@api.route('/')
class ReviewList(Resource):
    @api.expect(review_model)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """إنشاء مراجعة جديدة"""
        try:
            new_review = facade.create_review(api.payload)
            return {
                'id': new_review.id,
                'text': new_review.text,
                'rating': new_review.rating,
                'user_id': new_review.user_id,
                'place_id': new_review.place_id
            }, 201
        except ValueError as e:
            return {'error': str(e)}, 400

    @api.response(200, 'Success')
    def get(self):
        """جلب كل المراجعات"""
        reviews = facade.get_all_reviews()
        return [{
            'id': r.id,
            'text': r.text,
            'rating': r.rating,
            'user_id': r.user_id,
            'place_id': r.place_id
        } for r in reviews], 200

@api.route('/<string:review_id>')
@api.response(404, 'Review not found')
class ReviewResource(Resource):
    @api.response(200, 'Success')
    def get(self, review_id):
        """جلب مراجعة محددة بالـ ID"""
        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404
        return {
            'id': review.id,
            'text': review.text,
            'rating': review.rating,
            'user_id': review.user_id,
            'place_id': review.place_id
        }, 200

    @api.expect(review_model)
    @api.response(200, 'Review successfully updated')
    @api.response(400, 'Invalid input data')
    def put(self, review_id):
        """تحديث بيانات مراجعة"""
        try:
            updated_review = facade.update_review(review_id, api.payload)
            if not updated_review:
                return {'error': 'Review not found'}, 404
            return {'message': 'Review successfully updated'}, 200
        except ValueError as e:
            return {'error': str(e)}, 400

    @api.response(200, 'Review successfully deleted')
    def delete(self, review_id):
        """حذف مراجعة (مطلوب حصراً للمراجعات في هذه المهمة)"""
        if facade.delete_review(review_id):
            return {'message': 'Review successfully deleted'}, 200
        return {'error': 'Review not found'}, 404
