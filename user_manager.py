import json
import os

class UserManager:
    def __init__(self):
        self.users_file = 'data/users.json'
        self.ensure_data_file()
    
    def ensure_data_file(self):
        if not os.path.exists('data'):
            os.makedirs('data')
        if not os.path.exists(self.users_file):
            with open(self.users_file, 'w') as f:
                json.dump({}, f)
    
    def register_user(self, user_id, phone, emergency_contacts):
        users = self.load_users()
        users[user_id] = {
            'phone': phone,
            'emergency_contacts': emergency_contacts,
            'registered_at': str(datetime.now())
        }
        self.save_users(users)
        return True
    
    def get_user(self, user_id):
        users = self.load_users()
        return users.get(user_id)
    
    def load_users(self):
        try:
            with open(self.users_file, 'r') as f:
                return json.load(f)
        except:
            return {}
    
    def save_users(self, users):
        with open(self.users_file, 'w') as f:
            json.dump(users, f, indent=2)