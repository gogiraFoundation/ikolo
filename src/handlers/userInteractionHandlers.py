
class UserInteractionHandler:
    """Manages all user interactions."""

    @staticmethod
    def get_user_input(prompt):
        return input(prompt).strip()
    
    @staticmethod
    def get_password(prompt):
        return input(prompt).strip()

    @staticmethod
    def display_message(message):
        print(message)

    @staticmethod
    def get_ticker():
        return UserInteractionHandler.get_user_input("Enter stock ticker symbol (e.g., AAPL): ").upper()

    @staticmethod
    def get_dates():
        start_date = UserInteractionHandler.get_user_input("Enter start date (YYYY-MM-DD): ")
        end_date = UserInteractionHandler.get_user_input("Enter end date (YYYY-MM-DD): ")
        return start_date, end_date

    @staticmethod
    def get_window_sizes():
        try:
            moving_avg_window = int(UserInteractionHandler.get_user_input("Enter moving average window: "))
            volatility_window = int(UserInteractionHandler.get_user_input("Enter volatility window: "))
            return moving_avg_window, volatility_window
        except ValueError:
            return None, None

