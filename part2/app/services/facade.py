from app.models.user import User
from app.persistence.repository import InMemoryRepository

class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()

    # --- عمليات المستخدمين (User Operations) ---
    def create_user(self, user_data):
        # التحقق من عدم تكرار البريد الإلكتروني
        for u in self.user_repo.get_all():
            if u.email == user_data['email']:
                raise ValueError("Email already exists.")
        
        user = User(
            first_name=user_data['first_name'],
            last_name=user_data['last_name'],
            email=user_data['email']
        )
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        for u in self.user_repo.get_all():
            if u.email == email:
                return u
        return None

    def get_all_users(self):
        return self.user_repo.get_all()

    def update_user(self, user_id, user_data):
        return self.user_repo.update(user_id, user_data)
