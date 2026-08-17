# =====================================================================
# MEMBERS MODULE
# This module demonstrates OOPS Concepts: Inheritance & Encapsulation.
# 'User' is a parent class, and 'Admin' and 'Member' subclass from it.
# =====================================================================

from file_handler import read_json_file, write_json_file

USERS_FILE = 'users.json'

# === OOP Concept: Class, Objects & Encapsulation ===


class User:
    """
    Base definition of a User.
    This class encapsulates user properties like ID, username, and password.
    """
    def __init__(self, user_id, username, password, role, last_login="Never"):
        self.user_id = user_id
        self.username = username
        self.password = password  # In a production app, we would encrypt/hash this!
        self.role = role
        self.last_login = last_login

    def to_dict(self):
        """
        Converts the User instance properties into a plain Python dictionary.
        """
        return {
            "user_id": self.user_id,
            "username": self.username,
            "password": self.password,
            "role": self.role,
            "last_login": self.last_login
        }

# === OOP Concept: Inheritance ===
# Both Admin and Member inherit (receive) all attributes and methods 
# of their parent 'User' class, but they pass a fixed role type.

class Admin(User):
    """
    Admin user class that inherits from User.
    An Admin can manage books, view loan logs, etc.
    """
    def __init__(self, user_id, username, password, last_login="Never"):
        # super() lets us call the parent class __init__ method
        super().__init__(user_id, username, password, role="Admin", last_login=last_login)

class Member(User):
    """
    Member user class that inherits from User.
    A Member is a standard reader who can borrow and return books.
    """
    def __init__(self, user_id, username, password, last_login="Never"):
        super().__init__(user_id, username, password, role="Member", last_login=last_login)


class UserManager:
    """
    Handles registering new members, loading users from JSON files,
    saving changes, and authenticating user credentials.
    """
    def __init__(self):
        self.users = []
        self.load_users()

    def load_users(self):
        """
        Loads all accounts from the users file. 
        If the file is empty, a default Admin account (admin/admin) is created.
        """
        raw_data = read_json_file(USERS_FILE)
        self.users = []
        
        for item in raw_data:
            user_id = item.get("user_id")
            username = item.get("username", "")
            password = item.get("password", "")
            role = item.get("role", "Member")
            last_login = item.get("last_login", "Never")
            
            # Using OOPS: instantiate the correct subclass based on user role
            if role == "Admin":
                user = Admin(user_id, username, password, last_login)
            else:
                user = Member(user_id, username, password, last_login)
            self.users.append(user)
        
        # Self-starts default admin account for a fresh setup
        if not self.users:
            self.add_user("admin", "admin", "Admin")

    def save_users(self):
        """
        Saves all user accounts back to users.json.
        """
        data_to_save = []
        for user in self.users:
            data_to_save.append(user.to_dict())
        write_json_file(USERS_FILE, data_to_save)

    def generate_next_id(self):
        """
        Generates the next unique numeric ID for a new user account.
        """
        if not self.users:
            return 1
        
        highest_id = 0
        for user in self.users:
            if user.user_id > highest_id:
                highest_id = user.user_id
        return highest_id + 1

    def add_user(self, username, password, role="Member"):
        """
        Registers a new user username/password, checking for username duplicates.
        """
        if not username or not password:
            return False, "Error: Username and password cannot be empty!"
            
        # Check if the username is already registered (case insensitive)
        for user in self.users:
            if user.username.lower() == username.lower():
                return False, "Error: Username is already taken."
        
        next_id = self.generate_next_id()
        
        if role == "Admin":
            new_user = Admin(next_id, username, password)
        else:
            new_user = Member(next_id, username, password)
            
        self.users.append(new_user)
        self.save_users()
        return True, f"User '{username}' registered successfully."

    def find_user_by_username(self, username):
        """
        Traces a user in the loaded user list by their username string.
        """
        for user in self.users:
            if user.username == username:
                return user
        return None

    def authenticate(self, username, password):
        """
        Verifies if username exists and the password matches.
        Returns the User object on success, or None on failure.
        """
        from datetime import datetime
        user = self.find_user_by_username(username)
        if user and user.password == password:
            # Login successful and record last login time
            user.last_login = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.save_users()
            return user
        # Wrong username or wrong password
        return None

    def get_all_members(self):
        """
        Returns a list of all User objects that are Members (not Admins).
        """
        return [user for user in self.users if user.role == "Member"]

    def search_members(self, query):
        """
        Searches for members (excluding admins) matching username or ID.
        """
        results = []
        query_str = str(query).lower()
        for user in self.get_all_members():
            if query_str in user.username.lower() or query_str == str(user.user_id):
                results.append(user)
        return results

    def find_user_by_id(self, user_id):
        """
        Retrieves a user object by ID.
        """
        for user in self.users:
            if user.user_id == user_id:
                return user
        return None

if __name__ == "__main__":
    from main import main
    main()
