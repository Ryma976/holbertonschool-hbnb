from app.models.base import BaseModel

class Place(BaseModel):
    def __init__(self, title, description, price, latitude, longitude, owner_id):
        super().__init__()
        if not title or len(title.strip()) == 0:
            raise ValueError("Title cannot be empty.")
        if price <= 0:
            raise ValueError("Price must be a positive number.")
        if not (-90.0 <= latitude <= 90.0):
            raise ValueError("Latitude must be between -90.0 and 90.0.")
        if not (-180.0 <= longitude <= 180.0):
            raise ValueError("Longitude must be between -180.0 and 180.0.")
        if not owner_id:
            raise ValueError("Place must have a valid owner ID.")

        self.title = title.strip()
        self.description = description.strip()
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner_id = owner_id
        self.amenities = []
        self.reviews = []

    def add_amenity(self, amenity_id):
        if amenity_id not in self.amenities:
            self.amenities.append(amenity_id)

    def add_review(self, review_id):
        if review_id not in self.reviews:
            self.reviews.append(review_id)
