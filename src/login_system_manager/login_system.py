import sys
import os

# Add the `src` directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))


from user_management_system.register_user import RegisterUser
from handlers.userInteractionHandlers import UserInteractionHandler

#E:\Users\gogir\gogira\ikolo\ikolo\src\user_management_system

class LoginSystem:
    """Manages the login process and user actions."""

    def __init__(self):
        self.reg_user = RegisterUser()

    def register_user(self):
        """Registers a new user."""
        username = UserInteractionHandler.get_user_input("Enter a username: ")
        first_name = UserInteractionHandler.get_user_input("Enter your first name: ")
        second_name = UserInteractionHandler.get_user_input("Enter your last name: ")
        email = UserInteractionHandler.get_user_input("Enter your email address: ")
        password = UserInteractionHandler.get_password("Enter a password: ")

        result = self.reg_user.register(username, first_name, second_name, email, password)
        UserInteractionHandler.display_message(result)

    def login(self):
        """Logs in a user."""
        username = UserInteractionHandler.get_user_input("Enter your username: ")
        password = UserInteractionHandler.get_user_input("Enter your password: ")

        result = self.reg_user.login(username, password)
        if result is True:
            UserInteractionHandler.display_message("Login successful!")
            return True
        else:
            UserInteractionHandler.display_message(result)
            return False

    def list_users(self):
        """Displays all registered users."""
        users = self.reg_user.list_users()
        if isinstance(users, list) and users:
            UserInteractionHandler.display_message("\nRegistered Users:")
            for user in users:
                UserInteractionHandler.display_message(user)
        else:
            UserInteractionHandler.display_message("No registered users found.")

    def update_user_details(self):
        """Updates a user's details."""
        username = UserInteractionHandler.get_user_input("Enter the username to update: ")
        first_name = UserInteractionHandler.get_user_input("Enter new first name (leave blank to keep current): ")
        second_name = UserInteractionHandler.get_user_input("Enter new last name (leave blank to keep current): ")
        email = UserInteractionHandler.get_user_input("Enter new email address (leave blank to keep current): ")
        password = UserInteractionHandler.get_password("Enter new password (leave blank to keep current): ")

        result = self.reg_user.update_user_details(
            username,
            first_name if first_name else None,
            second_name if second_name else None,
            email if email else None,
            password if password else None
        )
        UserInteractionHandler.display_message(f"Update status: {result}")

    def reset_password(self):
        """Resets a user's password."""
        username = UserInteractionHandler.get_user_input("Enter the username for password reset: ")
        new_password = UserInteractionHandler.get_password("Enter the new password: ")

        result = self.reg_user.reset_password(username, new_password)
        UserInteractionHandler.display_message(f"Password reset status: {result}")

    def main_menu(self):
        """Displays the main menu and processes user choices."""
        while True:
            UserInteractionHandler.display_message("\nMain Menu:")
            UserInteractionHandler.display_message(
                "1. Register a new user\n"
                "2. Login\n"
                "3. List all users\n"
                "4. Update user details\n"
                "5. Reset password\n"
                "6. Exit"
            )
            choice = UserInteractionHandler.get_user_input("Enter your choice (1-6): ")

            if choice == "1":
                self.register_user()
            elif choice == "2":
                if self.login():
                    return True  # Exit after successful login
            elif choice == "3":
                self.list_users()
            elif choice == "4":
                self.update_user_details()
            elif choice == "5":
                self.reset_password()
            elif choice == "6":
                UserInteractionHandler.display_message("Exiting the system. Goodbye!")
                return False
            else:
                UserInteractionHandler.display_message("Invalid choice. Please try again.")
    
    def run_login():
        """Runs the login system."""
        system = LoginSystem()
        return system.main_menu()


# Run the login system
if __name__ == "__main__":
    login = LoginSystem.run_login()