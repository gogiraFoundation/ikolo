from src.data_fetcher import DataFetcher
from src.metrics_calculator import MetricsCalculator
from src.visualizer import Visualizer


def main():
    # User input
    ticker = input("Enter stock ticker (e.g., AAPL): ").upper()
    start_date = input("Enter start date (YYYY-MM-DD): ")
    end_date = input("Enter end date (YYYY-MM-DD): ")
    moving_avg_window = int(input("Enter moving average window: "))
    volatility_window = int(input("Enter volatility window: "))
    
    # Fetch data
    fetcher = DataFetcher()
    data = fetcher.fetch_stock_data(ticker, start_date, end_date)
    
    # Calculate metrics
    calculator = MetricsCalculator()
    moving_avg = calculator.calculate_moving_average(data, moving_avg_window)
    volatility = calculator.calculate_volatility(data, volatility_window)
    
    # Visualize
    visualizer = Visualizer()
    visualizer.plot_stock_data(data, moving_avg, volatility)


if __name__ == "__main__":
    main()
