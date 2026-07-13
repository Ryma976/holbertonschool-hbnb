from app.models.base import BaseModel

class Review(BaseModel):
    def __init__(self, text, rating, place_id, user_id):
        super().__init__()
        if not text or len(text.strip()) == 0:
            raise ValueError("Review text cannot be empty.")
        if not (1 <= rating <= 5):
            raise ValueError("Rating must be between 1 and 5.")
        if not place_id or not user_id:
            raise ValueError("Review must be linked to a valid Place and User.")

        self.text = text.strip()
        self.rating = rating
        self.place_id = place_id
        self.user_id = user_id
