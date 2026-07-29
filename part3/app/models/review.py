from app import db
from app.models.base import BaseModel

class Review(BaseModel):
    __tablename__ = 'reviews'

    text = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    place_id = db.Column(db.String(36), nullable=False)
    user_id = db.Column(db.String(36), nullable=False)

    def __init__(self, text, rating, place_id, user_id):
        super().__init__()
        self.text = self.validate_text(text)
        self.rating = self.validate_rating(rating)
        self.place_id = str(place_id)
        self.user_id = str(user_id)

    def validate_text(self, text):
        if not text or not isinstance(text, str) or len(text.strip()) == 0:
            raise ValueError("Review text is required.")
        return text.strip()

    def validate_rating(self, rating):
        try:
            val = int(rating)
        except (ValueError, TypeError):
            raise ValueError("Rating must be an integer between 1 and 5.")
        if not (1 <= val <= 5):
            raise ValueError("Rating must be an integer between 1 and 5.")
        return val

    def to_dict(self):
        return {
            "id": self.id,
            "text": self.text,
            "rating": self.rating,
            "place_id": self.place_id,
            "user_id": self.user_id,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }
