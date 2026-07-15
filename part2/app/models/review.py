from app.models.base import BaseModel

class Review(BaseModel):
    def __init__(self, text, rating, place_id, user_id):
        super().__init__()
        self.text = self._validate_text(text)
        self.rating = self._validate_rating(rating)
        self.place_id = place_id  # ربط بالـ Place ID
        self.user_id = user_id    # ربط بالـ User ID

    def _validate_text(self, text):
        if not text or len(text.strip()) == 0:
            raise ValueError("Review text cannot be empty.")
        return text.strip()

    def _validate_rating(self, rating):
        try:
            val = int(rating)
            if not (1 <= val <= 5):
                raise ValueError()
        except (ValueError, TypeError):
            raise ValueError("Rating must be an integer between 1 and 5.")
        return val
