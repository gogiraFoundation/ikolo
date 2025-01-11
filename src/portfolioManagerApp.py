from portfolio_manager.visualizer import Visualizer
from portfolio_manager.metrics_calculator import MetricsCalculator
from portfolio_manager.data_fetcher import DataFetcher
from handlers import is_valid_date, is_valid_ticker, lookup_ticker
from portfolio_manager.technical_analysis import TechnicalAnalysis
from portfolio_manager.fundamental_analysis import FundamentalAnalysis
from portfolio_manager.advisor import Advisor
from login_system import login_system


class PortfolioManagerApp:
    """
    Portfolio Management Application for stock analysis.
    """

    def __init__(self):
        self.visualizer = Visualizer()
        self.calculator = MetricsCalculator()
        self.fetcher = DataFetcher()
        self.technical_analysis = TechnicalAnalysis()
        self.fundamental_analysis = FundamentalAnalysis()
        self.advisor = Advisor()

    def get_ticker(self):
        """
        Get and validate the stock ticker symbol.
        """
        ticker = input("Enter stock ticker symbol (e.g., AAPL for Apple Inc.): ").upper()
        if not is_valid_ticker(ticker):
            print(f"Looking up ticker symbol for company: {ticker}")
            ticker = lookup_ticker(ticker)
            if not ticker:
                print("Error: Ticker not found.")
                return None
        return ticker

    def get_dates(self):
        """
        Get and validate start and end dates.
        """
        start_date = input("Enter start date (YYYY-MM-DD): ")
        end_date = input("Enter end date (YYYY-MM-DD): ")
        if not is_valid_date(start_date) or not is_valid_date(end_date):
            print("Error: Invalid date format. Use YYYY-MM-DD.")
            return None, None
        return start_date, end_date

    def get_window_sizes(self):
        """
        Get and validate window sizes for moving average and volatility calculations.
        """
        try:
            moving_avg_window = int(input("Enter moving average window: "))
            volatility_window = int(input("Enter volatility window: "))
            if moving_avg_window <= 0 or volatility_window <= 0:
                print("Error: Window sizes must be greater than zero.")
                return None, None
        except ValueError:
            print("Error: Enter valid integers for moving average and volatility windows.")
            return None, None
        return moving_avg_window, volatility_window

    def perform_analysis(self):
        """
        Perform stock analysis and display results.
        """
        print("\n=== Portfolio Analysis ===")

        # Ticker lookup if a company name is entered
        ticker = self.get_ticker()
        if not ticker:
            return

        # Get start and end date inputs
        start_date, end_date = self.get_dates()
        if not start_date or not end_date:
            return

        # Moving average and volatility window input
        moving_avg_window, volatility_window = self.get_window_sizes()
        if not moving_avg_window or not volatility_window:
            return

        try:
            # Fetch stock data
            data = self.fetcher.fetch_stock_data(ticker, start_date, end_date)
            if data is None or data.empty:
                print(f"Error: No data found for ticker '{ticker}'. It might be delisted.")
                return

            # Calculate metrics
            moving_avg = self.calculator.calculate_moving_average(data, moving_avg_window)
            volatility = self.calculator.calculate_volatility(data, volatility_window)

            # Visualize data
            self.visualizer.plot_stock_data(data, moving_avg, volatility)

            # Technical analysis
            macd, signal = self.technical_analysis.calculate_macd(data)
            rsi = self.technical_analysis.calculate_rsi(data)

            # Fundamental analysis
            ratios = self.fundamental_analysis.get_financial_ratios(ticker)

            # Generate advice
            advice = self.advisor.generate_advice(data, macd, signal, rsi)

            # Display results
            print("\n=== Analysis Results ===")
            print(f"Stock: {ticker}")
            print(f"Advice: {advice}")
            print("\nFundamental Ratios:")
            for key, value in ratios.items():
                print(f"{key}: {value}")

        except Exception as e:
            print(f"Error during analysis: {e}")

    def main_menu(self):
        """
        Display the main menu and handle user choices.
        """
        while True:
            print("\n=== Main Menu ===")
            print("1. Perform Analysis")
            print("2. Logout")
            print("3. Exit")
            choice = input("Enter your choice (1-3): ")

            if choice == "1":
                self.perform_analysis()
            elif choice == "2":
                print("Logging out...")
                break
            elif choice == "3":
                print("Exiting the application. Goodbye!")
                exit()
            else:
                print("Invalid choice. Please try again.")

    def run(self):
        """
        Run the application with user login and menu navigation.
        """
        print("Welcome to the Portfolio Management App!")
        while True:
            login = login_system()
            if login == True:
                self.main_menu()
            else:
                print("Exiting the application. Goodbye!")
                break
