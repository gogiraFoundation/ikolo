import json
import os
import hashlib
import re
import getpass


class RegisterUser:
    def __init__(self, db_file="data/user_database.json"):
        """
        Initialize the RegisterUser class with a specified JSON database file.
        Creates the database directory if it doesn't exist.
        """
        self.db_file = db_file
        os.makedirs(os.path.dirname(self.db_file), exist_ok=True)
        self.user_database = self.load_database()

    def load_database(self):
        """
        Load the user database from the JSON file.
        Returns an empty list if the file is not found.
        """
        try:
            with open(self.db_file, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return []

    def save_database(self):
        """
        Save the current user database to the JSON file.
        """
        try:
            with open(self.db_file, 'w') as file:
                json.dump(self.user_database, file, indent=4)
        except IOError as e:
            print(f"Error saving database: {e}")

    @staticmethod
    def hash_password(password: str):
        """
        Hash a password using SHA-256.
        """
        return hashlib.sha256(password.encode()).hexdigest()

    @staticmethod
    def validate_email(email: str):
        """
        Validate the format of an email address.
        """
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(email_regex, email))

    def register(self, username, first_name, second_name, email, password):
        """
        Register a new user and save them to the database.
        """
        username = username.lower()

        # Check for duplicate username or email
        if any(user['username'] == username for user in self.user_database):
            return f"Error: Username '{username}' is already taken."
        if any(user['email'] == email for user in self.user_database):
            return "Error: Email is already registered."
        if not self.validate_email(email):
            return "Error: Invalid email format."

        # Hash the password and save the user
        hashed_password = self.hash_password(password)
        new_user = {
            "username": username,
            "first_name": first_name,
            "second_name": second_name,
            "email": email,
            "password": hashed_password,
        }
        self.user_database.append(new_user)
        self.save_database()
        return f"User '{username}' registered successfully."

    def login(self, username: str, password: str):
        """
        Log in a user by validating their credentials.
        """
        username = username.lower()
        user = next((user for user in self.user_database if user["username"] == username), None)
        if not user:
            print("Error: User not found.")
            return False

        if user["password"] == self.hash_password(password):
            print(f"Welcome back, {user['first_name']}!")
            return True
        else:
            print("Error: Incorrect password.")
            return False

    def update_user_details(self, username, first_name=None, second_name=None, email=None, password=None):
        """
        Update user details and save changes to the database.
        """
        username = username.lower()
        user = next((user for user in self.user_database if user["username"] == username), None)
        if not user:
            return "Error: User not found."

        # Update user details
        if first_name:
            user["first_name"] = first_name
        if second_name:
            user["second_name"] = second_name
        if email:
            if self.validate_email(email):
                user["email"] = email
            else:
                return "Error: Invalid email format."
        if password:
            user["password"] = self.hash_password(password)

        self.save_database()  # Save changes
        return f"User '{username}' details updated successfully."

    def reset_password(self, username: str, new_password: str):
        """
        Reset a user's password and save changes to the database.
        """
        username = username.lower()
        user = next((user for user in self.user_database if user["username"] == username), None)
        if not user:
            return "Error: User not found."

        user["password"] = self.hash_password(new_password)
        self.save_database()
        return f"Password for '{username}' has been reset successfully."

    def list_users(self):
        """
        List all registered users.
        """
        if not self.user_database:
            return "No users are registered."
        return [f"{user['username']} ({user['email']})" for user in self.user_database]
