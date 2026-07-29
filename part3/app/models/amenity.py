from app.models.base import BaseModel

class Amenity(BaseModel):
    def __init__(self, name, description=""):
        super().__init__()
        self.name = self._validate_name(name)
        self.description = description

    def _validate_name(self, name):
        if not name or len(name.strip()) > 50:
            raise ValueError("Amenity name must be between 1 and 50 characters.")
        return name.strip()
