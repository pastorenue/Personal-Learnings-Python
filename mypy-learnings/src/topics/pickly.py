import pickle
import os
from datetime import datetime, timedelta

class UserDatabase:
    def __init__(self, filename='users.pkl'):
        """
        Initialize a user management system with persistent storage using pickling.
        
        :param filename: File to store pickled user data
        """
        self.filename = filename
        self.users = self.load_users()
    
    def load_users(self):
        """
        Load existing users from pickle file or return empty dictionary.
        π
        :return: Dictionary of users
        """
        try:
            if os.path.exists(self.filename):
                with open(self.filename, 'rb') as f:
                    return pickle.load(f)
            return {}
        except (pickle.UnpicklingError, EOFError):
            print("Error loading user database. Starting with empty database.")
            return {}
    
    def save_users(self):
        """
        Save users to pickle file.
        """
        try:
            with open(self.filename, 'wb') as f:
                pickle.dump(self.users, f)
        except Exception as e:
            print(f"Error saving user database: {e}")
    
    def add_user(self, username, email, role, last_login=None):
        """
        Add a new user to the database.
        
        :param username: Unique username
        :param email: User's email
        :param role: User's role in the system
        :param last_login: Optional last login timestamp
        """
        if username in self.users:
            raise ValueError(f"User {username} already exists.")
        
        user = {
            'email': email,
            'role': role,
            'registration_date': datetime.now(),
            'last_login': last_login or datetime.now(),
            'active_sessions': 0
        }
        
        self.users[username] = user
        self.save_users()
        print(f"User {username} added successfully.")
    
    def update_login(self, username):
        """
        Update login information for a user.
        
        :param username: Username to update
        """
        if username not in self.users:
            raise ValueError(f"User {username} not found.")
        
        self.users[username]['last_login'] = datetime.now()
        self.users[username]['active_sessions'] += 1
        self.save_users()
        print(f"Login updated for {username}")
    
    def get_inactive_users(self, days=30):
        """
        Find users inactive for more than specified days.
        
        :param days: Number of days of inactivity
        :return: List of inactive usernames
        """
        threshold = datetime.now() - timedelta(days=days)
        inactive_users = [
            username for username, user in self.users.items()
            if user['last_login'] < threshold
        ]
        return inactive_users
    
    def delete_user(self, username):
        """
        Remove a user from the database.
        
        :param username: Username to delete
        """
        if username in self.users:
            del self.users[username]
            self.save_users()
            print(f"User {username} deleted successfully.")
        else:
            print(f"User {username} not found.")

# Example usage
def main():
    # Create or load existing user database
    user_db = UserDatabase()
    
    # Add some users
    user_db.add_user('alice', 'alice@example.com', 'admin')
    user_db.add_user('bob', 'bob@example.com', 'user')
    
    # Update login
    user_db.update_login('alice')
    
    # Check inactive users
    inactive = user_db.get_inactive_users()
    print("Inactive users:", inactive)

if __name__ == '__main__':
    main()