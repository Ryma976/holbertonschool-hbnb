from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity
from app.persistence.user_repository import UserRepository
from app.persistence.place_repository import PlaceRepository
from app.persistence.review_repository import ReviewRepository
from app.persistence.amenity_repository import AmenityRepository

class HBnBFacade:
    def __init__(self):
        self.user_repo = UserRepository()
        self.place_repo = PlaceRepository()
        self.review_repo = ReviewRepository()
        self.amenity_repo = AmenityRepository()

    # Users
    def create_user(self, user_data):
        user = User(
            first_name=user_data.get('first_name'),
            last_name=user_data.get('last_name'),
            email=user_data.get('email'),
            is_admin=user_data.get('is_admin', False),
            password=user_data.get('password')
        )
        if self.user_repo.get_by_attribute('email', user.email):
            raise ValueError("Email already exists")

        return self.user_repo.add(user)

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        return self.user_repo.get_by_attribute('email', email)

    def get_all_users(self):
        return self.user_repo.get_all()

    def update_user(self, user_id, user_data, is_admin=False, current_user_id=None):
        user = self.get_user(user_id)
        if not user:
            return None, "User not found"
        
        if not is_admin and str(current_user_id) != str(user_id):
            return None, "Unauthorized action"

        update_fields = {}
        if 'first_name' in user_data:
            update_fields['first_name'] = user.validate_string(user_data['first_name'], "First name")
        if 'last_name' in user_data:
            update_fields['last_name'] = user.validate_string(user_data['last_name'], "Last name")
        
        if is_admin:
            if 'email' in user_data and user_data['email'] != user.email:
                new_email = user_data['email']
                existing = self.user_repo.get_by_attribute('email', new_email)
                if existing and str(existing.id) != str(user_id):
                    raise ValueError("Email already exists")
                update_fields['email'] = user.validate_email(new_email)
            if 'password' in user_data:
                user.hash_password(user_data['password'])
                update_fields['password'] = user.password
            if 'is_admin' in user_data:
                update_fields['is_admin'] = bool(user_data['is_admin'])

        updated_user = self.user_repo.update(user_id, update_fields)
        return updated_user, None

    # Places
    def create_place(self, place_data, owner_id):
        user = self.get_user(owner_id)
        if not user:
            raise ValueError("Owner not found")

        place = Place(
            title=place_data.get('title'),
            description=place_data.get('description'),
            price=place_data.get('price'),
            latitude=place_data.get('latitude'),
            longitude=place_data.get('longitude'),
            owner_id=str(owner_id)
        )
        return self.place_repo.add(place)

    def get_place(self, place_id):
        return self.place_repo.get(place_id)

    def get_all_places(self):
        return self.place_repo.get_all()

    def update_place(self, place_id, place_data, current_user_id, is_admin=False):
        place = self.get_place(place_id)
        if not place:
            return None, "Place not found"
        if not is_admin and str(place.owner_id) != str(current_user_id):
            return None, "Unauthorized action"
        
        updated = self.place_repo.update(place_id, place_data)
        return updated, None

    def delete_place(self, place_id, current_user_id, is_admin=False):
        place = self.get_place(place_id)
        if not place:
            return False, "Place not found"
        if not is_admin and str(place.owner_id) != str(current_user_id):
            return False, "Unauthorized action"
        return self.place_repo.delete(place_id), None

    # Reviews
    def create_review(self, review_data, user_id):
        place_id = str(review_data.get('place_id'))
        place = self.get_place(place_id)
        if not place:
            raise ValueError("Place not found")
        
        if str(place.owner_id) == str(user_id):
            raise ValueError("You cannot review your own place")

        for rev in self.review_repo.get_all():
            if str(rev.place_id) == place_id and str(rev.user_id) == str(user_id):
                raise ValueError("You have already reviewed this place")

        review = Review(
            text=review_data.get('text'),
            rating=review_data.get('rating'),
            place_id=place_id,
            user_id=str(user_id)
        )
        return self.review_repo.add(review)

    def get_review(self, review_id):
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        return self.review_repo.get_all()

    def update_review(self, review_id, review_data, current_user_id, is_admin=False):
        review = self.get_review(review_id)
        if not review:
            return None, "Review not found"
        if not is_admin and str(review.user_id) != str(current_user_id):
            return None, "Unauthorized action"
        updated = self.review_repo.update(review_id, review_data)
        return updated, None

    def delete_review(self, review_id, current_user_id, is_admin=False):
        review = self.get_review(review_id)
        if not review:
            return False, "Review not found"
        if not is_admin and str(review.user_id) != str(current_user_id):
            return False, "Unauthorized action"
        return self.review_repo.delete(review_id), None

    # Amenities
    def create_amenity(self, amenity_data):
        name = amenity_data.get('name')
        if not name:
            raise ValueError("Amenity name is required")
        amenity = Amenity(name=name)
        return self.amenity_repo.add(amenity)

    def get_amenity(self, amenity_id):
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        return self.amenity_repo.update(amenity_id, amenity_data)

facade = HBnBFacade()
