import os
import sys

# Add the `src` directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))

from handlers.userInteractionHandlers import UserInteractionHandler
from handlers.handlers import PortfolioManager


class PortfolioOperations:
    """Handle Logic that has to do with Portfolio Operations"""
    
    def __init__(self, portfolio_file):
        self.portfolio_manager = PortfolioManager()
        self.portfolio_file = portfolio_file  # Define portfolio file path
    
    
    def _view_portfolio(self):
        """View the portfolio."""
        try:
            portfolio = self.portfolio_manager.load_from_file(self.portfolio_file)
            if not portfolio:
                UserInteractionHandler.display_message("Portfolio is empty.")
                return
            
            # Get user email
            user_email = UserInteractionHandler.get_user_input("Email: ")
            if user_email in portfolio:
                user_portfolio = portfolio[user_email]
                if not user_portfolio:
                    UserInteractionHandler.display_message(f"Portfolio for {user_email} is empty.")
                    return
                UserInteractionHandler.display_message(f"\nPortfolio for {user_email}:")
                for stock in user_portfolio:
                    print(f"  Ticker: {stock['ticker']}, Shares: {stock['shares']}, Purchase Price: {stock['purchase_price']}")
            else:
                UserInteractionHandler.display_message(f"No portfolio found for user {user_email}")
        except Exception as e:
            UserInteractionHandler.display_message(f"Failed to load portfolio: {str(e)}")

    
    def _add_to_portfolio(self):
        """Add a stock to the portfolio."""
        try:
            user_email = UserInteractionHandler.get_user_input("Enter your email: ")
            ticker = UserInteractionHandler.get_user_input("Enter the stock ticker: ").upper()
            shares = float(UserInteractionHandler.get_user_input("Enter the number of shares: "))
            purchase_price = float(UserInteractionHandler.get_user_input("Enter the purchase price: "))
            
            self.portfolio_manager.add_to_portfolio(user_email, ticker, shares, purchase_price)
            UserInteractionHandler.display_message(f"Added {shares} shares of {ticker} at {purchase_price} to the portfolio.")
        except ValueError:
            UserInteractionHandler.display_message("Invalid input. Please enter numeric values for shares and purchase price.")
        except Exception as e:
            UserInteractionHandler.display_message(f"Failed to add to portfolio: {str(e)}")

    def _save_portfolio(self):
        """Save the portfolio."""
        try:
            self.portfolio_manager.save_to_file(self.portfolio_file)
            UserInteractionHandler.display_message(f"Portfolio successfully saved to {self.portfolio_file}.")
        except Exception as e:
            UserInteractionHandler.display_message(f"Failed to save portfolio: {str(e)}")

    def _generate_reports(self):
        """Generate reports from the portfolio."""
        try:
            report = self.portfolio_manager.generate_report(self.portfolio_file)
            UserInteractionHandler.display_message("Portfolio Report:")
            print(report)
            
            # Save report to a file
            save_to_file = UserInteractionHandler.get_user_input("Would you like to save the report to a file? (yes/no): ").lower()
            if save_to_file in ("yes", "y"):
                output_file = UserInteractionHandler.get_user_input("Enter the output file name (e.g., report.json): ")
                with open(output_file, 'w') as f:
                    f.write(report)  # Assuming the report is a string
                UserInteractionHandler.display_message(f"Report saved to {output_file}.")
        except Exception as e:
            UserInteractionHandler.display_message(f"Failed to generate report: {str(e)}")


    def _exit_operations(self):
        confirm_exit = UserInteractionHandler.get_user_input("Are you sure you want to exit? (yes/no): ").lower()
        if confirm_exit in ("yes", "y"):
            UserInteractionHandler.display_message("Exiting portfolio operations.")
        else:
            UserInteractionHandler.display_message("Returning to menu.")

    
    def _invalid_choice(self):
        """Handle invalid menu choices."""
        UserInteractionHandler.display_message("Invalid choice. Please try again.")
    
    def _display_menu(self):
        UserInteractionHandler.display_message("\n=== Portfolio Operations ===")
        UserInteractionHandler.display_message(
            "1. View Portfolio\n2. Add to Portfolio\n3. Save Portfolio\n4. Generate Report\n5. Exit"
        )
    
    def _portfolio_menu(self):
        """Perform portfolio operations."""
        actions = {
            "1": self._view_portfolio,
            "2": self._add_to_portfolio,
            "3": self._save_portfolio,
            "4": self._generate_reports,
            "5": self._exit_operations
        }

        while True:
            self._display_menu()
            choice = UserInteractionHandler.get_user_input("Enter your choice: ")
            action = actions.get(choice, self._invalid_choice)
            action()
            if action == self._exit_operations:
                break


    def _portfolio_operations_run(self):
        """Entry point of App logic."""
        try:
            self._portfolio_menu()
        except Exception as e:
            print(f"Operation failed: {str(e)}")
