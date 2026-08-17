from app import db
from app.models.base import BaseModel

# Intermediate table for Many-to-Many relationship between Place and Amenity
place_amenity = db.Table(
    'place_amenity',
    db.Column('place_id', db.String(36), db.ForeignKey('places.id'), primary_key=True),
    db.Column('amenity_id', db.String(36), db.ForeignKey('amenities.id'), primary_key=True)
)

class Place(BaseModel):
    __tablename__ = 'places'

    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    
    # Foreign Key
    owner_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)

    # Relationships
    reviews = db.relationship('Review', backref='place', lazy=True, cascade='all, delete-orphan')
    amenities = db.relationship('Amenity', secondary=place_amenity, backref='places', lazy='subquery')

    def __init__(self, title, description, price, latitude, longitude, owner_id):
        super().__init__()
        self.title = self.validate_title(title)
        self.description = description
        self.price = self.validate_price(price)
        self.latitude = self.validate_latitude(latitude)
        self.longitude = self.validate_longitude(longitude)
        self.owner_id = str(owner_id)

    def validate_title(self, title):
        if not title or not isinstance(title, str) or len(title.strip()) == 0:
            raise ValueError("Title is required.")
        if len(title) > 100:
            raise ValueError("Title cannot exceed 100 characters.")
        return title.strip()

    def validate_price(self, price):
        try:
            val = float(price)
        except (ValueError, TypeError):
            raise ValueError("Price must be a valid number.")
        if val <= 0:
            raise ValueError("Price must be greater than zero.")
        return val

    def validate_latitude(self, lat):
        try:
            val = float(lat)
        except (ValueError, TypeError):
            raise ValueError("Latitude must be a valid number.")
        if not (-90.0 <= val <= 90.0):
            raise ValueError("Latitude must be between -90 and 90.")
        return val

    def validate_longitude(self, lon):
        try:
            val = float(lon)
        except (ValueError, TypeError):
            raise ValueError("Longitude must be a valid number.")
        if not (-180.0 <= val <= 180.0):
            raise ValueError("Longitude must be between -180 and 180.")
        return val

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "price": self.price,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "owner_id": self.owner_id,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }
