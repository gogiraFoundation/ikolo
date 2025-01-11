from portfolio_manager.visualizer import Visualizer
from portfolio_manager.metrics_calculator import MetricsCalculator
from portfolio_manager.data_fetcher import DataFetcher
from handlers import is_valid_date, is_valid_ticker, lookup_ticker
from portfolio_manager.technical_analysis import TechnicalAnalysis
from portfolio_manager.fundamental_analysis import FundamentalAnalysis
from portfolio_manager.advisor import Advisor
from user_management_system.login_system import login_system


def perform_analysis():
    """
    Perform stock analysis after user login.
    """
    print("\n=== Portfolio Analysis ===")
    try:
        ticker = input("Enter stock ticker symbol (e.g., AAPL for Apple Inc.): ").upper()

        # Ticker lookup if a company name is entered
        if not is_valid_ticker(ticker):
            print(f"Looking up ticker symbol for company: {ticker}")
            ticker = lookup_ticker(ticker)
            if not ticker:
                print("Ticker not found.")
                return

        print(f"Using ticker: {ticker}")

        # Get start and end date inputs
        start_date = input("Enter start date (YYYY-MM-DD): ")
        end_date = input("Enter end date (YYYY-MM-DD): ")

        # Validate dates
        if not is_valid_date(start_date) or not is_valid_date(end_date):
            print("Error: Invalid date format. Use YYYY-MM-DD.")
            return

        # Moving average and volatility window input
        try:
            moving_avg_window = int(input("Enter moving average window: "))
            volatility_window = int(input("Enter volatility window: "))
            if moving_avg_window <= 0 or volatility_window <= 0:
                print("Error: Window sizes must be greater than zero.")
                return
        except ValueError:
            print("Error: Enter valid integers for moving average and volatility windows.")
            return

        # Fetch data
        fetcher = DataFetcher()
        try:
            data = fetcher.fetch_stock_data(ticker, start_date, end_date)
            if data is None or data.empty:
                print(f"Error: No data found for ticker '{ticker}'. It might be delisted.")
                return
        except Exception as e:
            print(f"Error fetching data: {e}")
            return

        # Calculate metrics and visualize
        calculator = MetricsCalculator()
        visualizer = Visualizer()

        moving_avg = calculator.calculate_moving_average(data, moving_avg_window)
        volatility = calculator.calculate_volatility(data, volatility_window)

        visualizer.plot_stock_data(data, moving_avg, volatility)

        # Perform technical analysis
        ta = TechnicalAnalysis()
        macd, signal = ta.calculate_macd(data)
        rsi = ta.calculate_rsi(data)

        # Perform fundamental analysis
        funda = FundamentalAnalysis()
        ratios = funda.get_financial_ratios(ticker)

        # Generate investment advice
        advisor = Advisor()
        advice = advisor.generate_advice(data, macd, signal, rsi)

        # Display results
        print("\n=== Analysis Results ===")
        print(f"Stock: {ticker}")
        print(f"Advice: {advice}")
        print("\nFundamental Ratios:")
        for key, value in ratios.items():
            print(f"{key}: {value}")

    except Exception as e:
        print(f"Error during analysis: {e}")


def ikolo():
    """
    Main function to manage the app lifecycle.
    """
    print("Welcome to the Portfolio Management App!")
    try:
        if login_system():
            while True:
                print("\n=== Main Menu ===")
                print("1. Perform Stock Analysis")
                print("2. Logout")
                print("3. Exit")
                
                choice = input("Enter your choice (1-3): ")
                if choice == "1":
                    perform_analysis()
                elif choice == "2":
                    print("Logging out...")
                    break
                elif choice == "3":
                    print("Exiting the application. Goodbye!")
                    exit(0)
                else:
                    print("Invalid choice. Please try again.")
        else:
            print("Login failed. Exiting application.")
    except Exception as e:
        print(f"Failed to start app: {e}")


if __name__ == "__main__":
    ikolo()