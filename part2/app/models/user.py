import re
from app.models.base import BaseModel

class User(BaseModel):
    def __init__(self, first_name, last_name, email, is_admin=False):
        super().__init__()
        self.first_name = self._validate_name(first_name, "First name")
        self.last_name = self._validate_name(last_name, "Last name")
        self.email = self._validate_email(email)
        self.is_admin = is_admin

    def _validate_name(self, name, field_name):
        if not name or len(name.strip()) > 50:
            raise ValueError(f"{field_name} must be between 1 and 50 characters.")
        return name.strip()

    def _validate_email(self, email):
        email_regex = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        if not email or not re.match(email_regex, email):
            raise ValueError("Invalid email format.")
        return email.strip()
