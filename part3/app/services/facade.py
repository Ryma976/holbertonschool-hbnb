from app.models.user import User

class Place:
    def __init__(self, title, description, price, latitude, longitude, owner_id):
        self.id = None
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner_id = owner_id
        self.reviews = []

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "price": self.price,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "owner_id": self.owner_id
        }

class Review:
    def __init__(self, text, rating, place_id, user_id):
        self.id = None
        self.text = text
        self.rating = rating
        self.place_id = place_id
        self.user_id = user_id

    def to_dict(self):
        return {
            "id": self.id,
            "text": self.text,
            "rating": self.rating,
            "place_id": self.place_id,
            "user_id": self.user_id
        }

class HBnBFacade:
    def __init__(self):
        self.user_repo = {}
        self.place_repo = {}
        self.review_repo = {}

    def create_user(self, user_data):
        user = User(
            first_name=user_data.get('first_name'),
            last_name=user_data.get('last_name'),
            email=user_data.get('email'),
            is_admin=user_data.get('is_admin', False),
            password=user_data.get('password')
        )
        for u in self.user_repo.values():
            if u.email == user.email:
                raise ValueError("Email already exists")
                
        user.id = str(len(self.user_repo) + 1)
        self.user_repo[user.id] = user
        return user

    def get_user(self, user_id):
        return self.user_repo.get(str(user_id))

    def get_user_by_email(self, email):
        for user in self.user_repo.values():
            if user.email == email:
                return user
        return None

    def get_all_users(self):
        return list(self.user_repo.values())

    def update_user(self, user_id, user_data):
        user = self.get_user(user_id)
        if not user:
            return None
        if 'first_name' in user_data:
            user.first_name = user.validate_string(user_data['first_name'], "First name")
        if 'last_name' in user_data:
            user.last_name = user.validate_string(user_data['last_name'], "Last name")
        return user

    # Places CRUD
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
        place.id = str(len(self.place_repo) + 1)
        self.place_repo[place.id] = place
        return place

    def get_place(self, place_id):
        return self.place_repo.get(str(place_id))

    def get_all_places(self):
        return list(self.place_repo.values())

    def update_place(self, place_id, place_data, current_user_id):
        place = self.get_place(place_id)
        if not place:
            return None, "Place not found"
        if place.owner_id != str(current_user_id):
            return None, "Unauthorized"
        
        for key in ['title', 'description', 'price', 'latitude', 'longitude']:
            if key in place_data:
                setattr(place, key, place_data[key])
        return place, None

    def delete_place(self, place_id, current_user_id):
        place = self.get_place(place_id)
        if not place:
            return False, "Place not found"
        if place.owner_id != str(current_user_id):
            return False, "Unauthorized"
        del self.place_repo[str(place_id)]
        return True, None

    # Reviews CRUD
    def create_review(self, review_data, user_id):
        place_id = str(review_data.get('place_id'))
        place = self.get_place(place_id)
        if not place:
            raise ValueError("Place not found")
        
        if place.owner_id == str(user_id):
            raise ValueError("You cannot review your own place")

        for rev in self.review_repo.values():
            if rev.place_id == place_id and rev.user_id == str(user_id):
                raise ValueError("You have already reviewed this place")

        review = Review(
            text=review_data.get('text'),
            rating=review_data.get('rating'),
            place_id=place_id,
            user_id=str(user_id)
        )
        review.id = str(len(self.review_repo) + 1)
        self.review_repo[review.id] = review
        return review

    def get_review(self, review_id):
        return self.review_repo.get(str(review_id))

    def get_all_reviews(self):
        return list(self.review_repo.values())

    def update_review(self, review_id, review_data, current_user_id):
        review = self.get_review(review_id)
        if not review:
            return None, "Review not found"
        if review.user_id != str(current_user_id):
            return None, "Unauthorized"
        if 'text' in review_data:
            review.text = review_data['text']
        if 'rating' in review_data:
            review.rating = review_data['rating']
        return review, None

facade = HBnBFacade()
