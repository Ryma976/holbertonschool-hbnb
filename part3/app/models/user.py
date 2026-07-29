import re
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

class User:
    def __init__(self, first_name, last_name, email, is_admin=False, password=None):
        self.id = None
        self.first_name = self.validate_string(first_name, "First name")
        self.last_name = self.validate_string(last_name, "Last name")
        self.email = self.validate_email(email)
        self.is_admin = is_admin
        self.password = None
        if password:
            self.hash_password(password)

    def validate_string(self, value, field_name):
        if not value or not isinstance(value, str) or len(value.strip()) == 0:
            raise ValueError(f"{field_name} is required and must be a non-empty string.")
        return value.strip()

    def validate_email(self, email):
        if not email or not isinstance(email, str):
            raise ValueError("Email is required.")
        regex = r'^\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if not re.match(regex, email):
            raise ValueError("Invalid email format.")
        return email

    def hash_password(self, password):
        """Hashes the password using bcrypt"""
        if not password:
            raise ValueError("Password is required.")
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        """Verifies if the provided password matches the hashed password"""
        if not self.password or not password:
            return False
        return bcrypt.check_password_hash(self.password, password)

    def to_dict(self):
        """Returns dictionary representation of User, excluding the password"""
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "is_admin": self.is_admin
        }
