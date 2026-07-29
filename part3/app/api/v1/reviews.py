from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.facade import facade

api = Namespace('reviews', description='Review operations')

review_model = api.model('Review', {
    'text': fields.String(required=True, description='Text content'),
    'rating': fields.Integer(required=True, description='Rating (1-5)'),
    'place_id': fields.String(required=True, description='Place ID')
})

@api.route('/')
class ReviewList(Resource):
    def get(self):
        """Retrieve all reviews (Public)"""
        reviews = facade.get_all_reviews()
        return [r.to_dict() for r in reviews], 200

    @api.expect(review_model, validate=True)
    @jwt_required()
    def post(self):
        """Create a new review (Authenticated User Only)"""
        current_user_id = get_jwt_identity()
        review_data = api.payload
        try:
            new_review = facade.create_review(review_data, user_id=current_user_id)
            return new_review.to_dict(), 201
        except ValueError as e:
            return {'error': str(e)}, 400

@api.route('/<review_id>')
class ReviewResource(Resource):
    def get(self, review_id):
        """Get review details by ID (Public)"""
        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404
        return review.to_dict(), 200

    @jwt_required()
    def put(self, review_id):
        """Update review (Author Only)"""
        current_user_id = get_jwt_identity()
        review_data = api.payload
        updated_review, error = facade.update_review(review_id, review_data, current_user_id)
        if error == "Review not found":
            return {'error': error}, 404
        if error == "Unauthorized":
            return {'error': 'Unauthorized action'}, 403
        return updated_review.to_dict(), 200
