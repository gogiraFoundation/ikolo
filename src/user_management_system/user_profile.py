


print("User module loaded.")


class User:
    """A class that defines a particular user."""

    def __init__(self, username: str, first_name: str, second_name: str, email: str):
        """
        Initializes a User instance.

        :param username: The username of the user.
        :param first_name: The first name of the user.
        :param second_name: The last name of the user.
        :param email: The email address of the user.
        """
        self.username = username
        self.first_name = first_name
        self.second_name = second_name
        self.email = email

    def __str__(self):
        """
        Returns a string representation of the User object.
        """
        return f"User(username={self.username}, first_name={self.first_name}, second_name={self.second_name}, email={self.email})"

    def full_name(self):
        """
        Returns the full name of the user.
        """
        return f"{self.first_name} {self.second_name}"

    def update_email(self, new_email: str):
        """
        Updates the email address of the user.
        :param new_email: The new email address to set.
        """
        self.email = new_email
        print(f"Email updated to {new_email}.")




