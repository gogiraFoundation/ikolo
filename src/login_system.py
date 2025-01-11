from user_management_system.register_user import RegisterUser


def login_system():
    """
    Handles user management actions and login process.
    Returns True if the user successfully logs in, False if the user exits without logging in.
    """
    print("Login")
    reg_user = RegisterUser()
    logged_in = False  # Flag to manage loop exit

    while not logged_in:
        print("\nMain Menu:")
        print("1. Register a new user")
        print("2. Login")
        print("3. List all users")
        print("4. Update user details")
        print("5. Reset password")
        print("6. Exit")
        
        choice = input("Enter your choice (1-6): ")

        if choice == "1":
            username = input("Enter a username: ")
            first_name = input("Enter your first name: ")
            second_name = input("Enter your last name: ")
            email = input("Enter your email address: ")
            password = input("Enter a password: ")

            result = reg_user.register(username, first_name, second_name, email, password)
            print(f"Registration status: {result}")

        elif choice == "2":
            username = input("Enter your username: ")
            password = input("Enter your password: ")

            result = reg_user.login(username, password)  
            
            if result == True:
                logged_in = False  # Set flag to exit loop
                break
            else:
                print(result)

        elif choice == "3":
            print("\nRegistered Users:")
            users = reg_user.list_users()
            if isinstance(users, list) and users:
                for user in users:
                    print(user)
            else:
                print("No registered users found.")

        elif choice == "4":
            username = input("Enter the username to update: ")
            first_name = input("Enter new first name (leave blank to keep current): ")
            second_name = input("Enter new last name (leave blank to keep current): ")
            email = input("Enter new email address (leave blank to keep current): ")
            password = input("Enter new password (leave blank to keep current): ")

            result = reg_user.update_user_details(
                username,
                first_name if first_name else None,
                second_name if second_name else None,
                email if email else None,
                password if password else None
            )
            print(f"Update status: {result}")

        elif choice == "5":
            username = input("Enter the username for password reset: ")
            new_password = input("Enter the new password: ")

            result = reg_user.reset_password(username, new_password)
            print(f"Password reset status: {result}")

        elif choice == "6":
            print("Exiting the system. Goodbye!")
            return False

        else:
            print("Invalid choice. Please try again.")

    print("Continuing with post-login operations...")
    return True




login_system()