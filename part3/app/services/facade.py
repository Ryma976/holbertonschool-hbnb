from app.models.user import User

class HBnBFacade:
    def __init__(self):
        self.user_repo = {}

    def create_user(self, user_data):
        user = User(
            first_name=user_data.get('first_name'),
            last_name=user_data.get('last_name'),
            email=user_data.get('email'),
            is_admin=user_data.get('is_admin', False),
            password=user_data.get('password')
        )
        for u in self.user_repo.values():
            if u.email == user.email:
                raise ValueError("Email already exists")
                
        user.id = str(len(self.user_repo) + 1)
        self.user_repo[user.id] = user
        return user

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        for user in self.user_repo.values():
            if user.email == email:
                return user
        return None

    def get_all_users(self):
        return list(self.user_repo.values())

    def update_user(self, user_id, user_data):
        user = self.get_user(user_id)
        if not user:
            return None
        if 'first_name' in user_data:
            user.first_name = user.validate_string(user_data['first_name'], "First name")
        if 'last_name' in user_data:
            user.last_name = user.validate_string(user_data['last_name'], "Last name")
        if 'email' in user_data:
            user.email = user.validate_email(user_data['email'])
        if 'password' in user_data:
            user.hash_password(user_data['password'])
        return user

facade = HBnBFacade()
