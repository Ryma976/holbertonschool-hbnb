import re
from app import bcrypt, db
from app.models.base import BaseModel

class User(BaseModel):
    __tablename__ = 'users'

    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    # Relationships
    places = db.relationship('Place', backref='owner', lazy=True, cascade='all, delete-orphan')
    reviews = db.relationship('Review', backref='author', lazy=True, cascade='all, delete-orphan')

    def __init__(self, first_name, last_name, email, password=None, is_admin=False):
        super().__init__()
        self.first_name = self.validate_string(first_name, "First name")
        self.last_name = self.validate_string(last_name, "Last name")
        self.email = self.validate_email(email)
        self.is_admin = is_admin
        if password:
            self.hash_password(password)

    def validate_string(self, value, field_name):
        if not value or not isinstance(value, str) or len(value.strip()) == 0:
            raise ValueError(f"{field_name} is required and must be a non-empty string.")
        if len(value) > 50:
            raise ValueError(f"{field_name} cannot exceed 50 characters.")
        return value.strip()

    def validate_email(self, email):
        if not email or not isinstance(email, str):
            raise ValueError("Email is required.")
        regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(regex, email):
            raise ValueError("Invalid email format.")
        return email.lower().strip()

    def hash_password(self, password):
        if not password or len(password) < 6:
            raise ValueError("Password must be at least 6 characters long.")
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        return bcrypt.check_password_hash(self.password, password)

    def to_dict(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "is_admin": self.is_admin,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }
