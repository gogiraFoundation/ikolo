

import os
import json
from portfolio_manager.visualizer import Visualizer
from portfolio_manager.metrics_calculator import MetricsCalculator
from portfolio_manager.data_fetcher import DataFetcher
from portfolio_manager.technical_analysis import TechnicalAnalysis
from portfolio_manager.fundamental_analysis import FundamentalAnalysis
from portfolio_manager.advisor import Advisor
from portfolio_manager.searchStocks import StockSearcher
from portfolio_manager.tracker import Tracker
from handlers.handlers import WatchlistManager, PortfolioManager
from handlers.utilityHandler import UtilityHandler
from handlers.userInteractionHandlers import UserInteractionHandler
from sessionManager.session_manager import SessionManager
from login_system_manager.login_system import LoginSystem
from logs.logger import Logger
from file_manager.fileManager import FileManager


class PortfolioManagerApp:
    """
    Portfolio Management Application for stock analysis and portfolio tracking.
    """

    def __init__(self):
        self.logger = Logger("PortfolioManagerApp")
        self.file_manager = FileManager()
        self._load_configuration()
        self._initialize_modules()
        

    def _initialize_modules(self):
        """Initialize core modules."""
        self.searcher = StockSearcher(tickers=self.default_tickers)
        self.tracker = Tracker()
        self.session_manager = SessionManager()
        self.visualizer = Visualizer()
        self.calculator = MetricsCalculator()
        self.fetcher = DataFetcher()
        self.technical_analysis = TechnicalAnalysis()
        self.fundamental_analysis = FundamentalAnalysis()
        self.advisor = Advisor()
        self.watchlist_manager = WatchlistManager()
        self.portfolio_manager = PortfolioManager()

    def _load_configuration(self):
        """Load application configuration from a file."""
        config_path = os.path.join(os.getcwd(), "config.json")
        config = self.file_manager.load_json_file(config_path)
        if config:
            self.default_tickers = config.get("default_tickers", ["AAPL", "MSFT", "GOOGL"])
            self.data_directory = config.get("data_directory", os.path.join(os.getcwd(), "data"))
        else:
            self.logger.log_warning("Config file not found. Using default settings.")
            self.default_tickers = ["AAPL", "MSFT", "GOOGL"]
            self.data_directory = os.path.join(os.getcwd(), "data")


    def ensure_directories_exist(self):
        """Ensure required directories exist."""
        # Define file paths before usage
        self.watchlist_file = os.path.join(self.data_directory, "watchlist", "watchlist.txt")
        self.portfolio_file = os.path.join(self.data_directory, "portfolio", "portfolio.txt")
        
        # Ensure directories exist
        self.file_manager.ensure_directory_exists(os.path.dirname(self.watchlist_file))
        self.file_manager.ensure_directory_exists(os.path.dirname(self.portfolio_file))
        self.logger.log_info("Required directories verified or created.")
    
    def perform_analysis(self):
        """Perform stock analysis."""
        self.logger.log_info("Starting stock analysis...")
        try:
            ticker = UserInteractionHandler.get_ticker()
            if not UtilityHandler.validate_ticker(ticker):
                UserInteractionHandler.display_message("Invalid ticker.")
                self.logger.log_warning("Invalid ticker entered.")
                return

            start_date, end_date = UserInteractionHandler.get_dates()
            if not UtilityHandler.validate_dates(start_date, end_date):
                UserInteractionHandler.display_message("Invalid dates.")
                self.logger.log_warning("Invalid date range provided.")
                return

            self._analyze_stock(ticker, start_date, end_date)
            self.logger.log_info("Stock analysis completed successfully.")
        except Exception as e:
            self.logger.log_error("Error during stock analysis", e)
            raise

    def _analyze_stock(self, ticker, start_date, end_date):
        """Helper method to analyze a stock."""
        data = self.fetcher.fetch_stock_data(ticker, start_date, end_date)

        if data.empty:
            UserInteractionHandler.display_message(f"No data found for ticker '{ticker}'.")
            return

        # Perform analysis
        moving_avg = self.calculator.calculate_moving_average(data, 20)
        volatility = self.calculator.calculate_volatility(data, 20)
        self.visualizer.run_visualizer(data)
        self.visualizer.plot_stock_data(data, moving_avg, volatility)
        macd, signal = self.technical_analysis.calculate_macd(data)
        rsi = self.technical_analysis.calculate_rsi(data)
        ratios = self.fundamental_analysis.get_financial_ratios(ticker)
        advice = self.advisor.generate_advice(data, macd, signal, rsi)

        self._display_analysis_results(ticker, advice, ratios)

    def _display_analysis_results(self, ticker, advice, ratios):
        """Display analysis results to the user."""
        UserInteractionHandler.display_message("\n=== Analysis Results ===")
        UserInteractionHandler.display_message(f"Stock: {ticker}")
        UserInteractionHandler.display_message(f"Advice: {advice}")
        UserInteractionHandler.display_message("\nFundamental Ratios:")
        for key, value in ratios.items():
            UserInteractionHandler.display_message(f"{key}: {value}")

    def search_stocks(self, tickers):
        """Search for stock metadata."""
        try:
            for ticker in tickers:
                metadata = self.searcher.fetch_metadata(ticker)
                print(metadata)
        except Exception as e:
            UserInteractionHandler.display_message(f"Error during stock search: {e}")
        finally:
            self.searcher.close_connection()

    def track_stocks(self):
        """Track a stock with a threshold alert."""
        ticker = UserInteractionHandler.get_ticker()

        if not UtilityHandler.validate_ticker(ticker):
            UserInteractionHandler.display_message("Invalid ticker.")
            return

        try:
            threshold = UtilityHandler.validate_threshold(UserInteractionHandler.get_user_input("Enter price threshold: "))
            self.watchlist_manager.add_to_watchlist(ticker, threshold)
            self.watchlist_manager.save_to_file(self.watchlist_file)
            UserInteractionHandler.display_message(f"Tracking {ticker} with a threshold of {threshold}.")
        except ValueError:
            UserInteractionHandler.display_message("Invalid input for threshold.")

    def portfolio_operations(self):
        """Perform portfolio operations."""
        actions = {
            "1": self._view_portfolio,
            "2": self.track_stocks,
            "3": self._save_portfolio,
            "4": self._exit_operations
        }

        while True:
            UserInteractionHandler.display_message("\n=== Portfolio Operations ===")
            UserInteractionHandler.display_message("1. View Portfolio\n2. Add to Portfolio\n3. Save Portfolio\n4. Exit")
            choice = UserInteractionHandler.get_user_input("Enter your choice: ")

            action = actions.get(choice, self._invalid_choice)
            if action == self._exit_operations:
                break
            action()

    def _view_portfolio(self):
        """View the portfolio."""
        self.portfolio_manager.load_from_file(self.portfolio_file)

    def _save_portfolio(self):
        """Save the portfolio."""
        self.portfolio_manager.save_to_file(self.portfolio_file)

    def _exit_operations(self):
        """Exit portfolio operations."""
        UserInteractionHandler.display_message("Exiting portfolio operations.")

    def _invalid_choice(self):
        """Handle invalid menu choices."""
        UserInteractionHandler.display_message("Invalid choice. Please try again.")

    def _prompt_and_search_stocks(self):
        """Prompt the user for tickers and search stocks."""
        tickers_input = UserInteractionHandler.get_user_input(
            "Enter comma-separated tickers to search (e.g., AAPL,MSFT): "
        )
        tickers = [ticker.strip().upper() for ticker in tickers_input.split(",") if ticker.strip()]
        if not tickers:
            UserInteractionHandler.display_message("No valid tickers provided.")
            return
        self.search_stocks(tickers)

    def get_actions(self):
        return {
            "1": {"description": "Perform Analysis", "action": self.perform_analysis},
            "2": {"description": "Track Stocks", "action": self.track_stocks},
            "3": {"description": "Search Stocks", "action": self._prompt_and_search_stocks},
            "4": {"description": "Portfolio Operations", "action": self.portfolio_operations},
            "5": {"description": "Exit", "action": self._exit_application},
        }

    def execute_action(self, choice):
        actions = self.get_actions()
        action = actions.get(choice, {}).get("action")
        if action:
            action()
            return True
        self.logger.log_warning(f"Invalid choice entered: {choice}")
        UserInteractionHandler.display_message("Invalid choice. Please select a valid option from the menu.")
        return False

    def show_menu(self, menu_options):
        try:
            for key, value in menu_options.items():
                print(f"{key}. {value['description']}")
            choice = UserInteractionHandler.get_user_input("Enter your choice: ").strip()
            if choice not in menu_options:
                raise ValueError(f"Invalid menu choice: {choice}")

            return choice
        except ValueError as e:
            self.logger.log_warning(str(e))
            UserInteractionHandler.display_message("Invalid input. Please try again.")
            return None


    def main_menu(self):
        user_id = UserInteractionHandler.get_user_input("Enter your user ID: ")
        session_data = self.session_manager.load_session(user_id)
        welcome_message = f"Welcome {'back, ' if session_data else ''}{user_id}!"
        UserInteractionHandler.display_message(welcome_message)

        while True:
            choice = self.show_menu(self.get_actions())
            if not self.execute_action(choice):
                break

    def run(self):
        """Run the application."""
        try:
            self.ensure_directories_exist()
            UserInteractionHandler.display_message("Welcome to the Portfolio Management App!")
            if LoginSystem.run_login():
                self.main_menu()
            else:
                UserInteractionHandler.display_message("Exiting the application.")
        except Exception as e:
            self.logger.log_critical("Unhandled exception occurred", e)

    def _exit_application(self):
        """Exit the application."""
        UserInteractionHandler.display_message("Exiting the application.")
        self.searcher.close_connection()


if __name__ == "__main__":
    app = PortfolioManagerApp()
    app.run()