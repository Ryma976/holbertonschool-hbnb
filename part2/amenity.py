from app.models.base import BaseModel

class Amenity(BaseModel):
    def __init__(self, name, description=""):
        super().__init__()
        if not name or len(name.strip()) == 0:
            raise ValueError("Amenity name cannot be empty.")
        self.name = name.strip()
        self.description = description.strip()
