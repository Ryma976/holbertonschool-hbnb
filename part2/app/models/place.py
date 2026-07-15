from app.models.base import BaseModel

class Place(BaseModel):
    def __init__(self, title, description, price, latitude, longitude, owner_id):
        super().__init__()
        self.title = self._validate_title(title)
        self.description = description  # اختياري
        self.price = self._validate_price(price)
        self.latitude = self._validate_latitude(latitude)
        self.longitude = self._validate_longitude(longitude)
        self.owner_id = owner_id  # ربط بالـ User ID
        self.amenities = []       # قائمة تحتوي على الـ Amenity IDs المضافة للمكان

    def _validate_title(self, title):
        if not title or len(title.strip()) > 100:
            raise ValueError("Title must be between 1 and 100 characters.")
        return title.strip()

    def _validate_price(self, price):
        try:
            val = float(price)
            if val < 0:
                raise ValueError()
        except (ValueError, TypeError):
            raise ValueError("Price must be a positive number.")
        return val

    def _validate_latitude(self, lat):
        try:
            val = float(lat)
            if not (-90.0 <= val <= 90.0):
                raise ValueError()
        except (ValueError, TypeError):
            raise ValueError("Latitude must be between -90.0 and 90.0.")
        return val

    def _validate_longitude(self, lon):
        try:
            val = float(lon)
            if not (-180.0 <= val <= 180.0):
                raise ValueError()
        except (ValueError, TypeError):
            raise ValueError("Longitude must be between -180.0 and 180.0.")
        return val

    def add_amenity(self, amenity_id):
        if amenity_id not in self.amenities:
            self.amenities.append(amenity_id)
