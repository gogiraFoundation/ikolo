import time
import schedule
from data_fetcher import DataFetcher
from datetime import datetime


class Tracker:
    """Class for tracking stock prices."""

    def __init__(self, ticker: str, threshold: float):
        """
        Initialize the Tracker instance.
        :param ticker: Stock ticker symbol.
        :param threshold: Price threshold for alerts.
        """
        self.ticker = ticker.upper()
        self.threshold = threshold
        self.fetcher = DataFetcher()
        self.watchlist = []

    def check_price(self):
        """Fetch the latest stock price and check against the threshold."""
        try:
            # Use the current date for fetching data
            current_date = datetime.now().strftime('%Y-%m-%d')
            data = self.fetcher.fetch_stock_data(self.ticker, current_date, current_date)
            
            if data is None or data.empty:
                print(f"No data available for {self.ticker} on {current_date}.")
                return

            latest_price = data['Close'].iloc[-1]

            if latest_price > self.threshold:
                print(f"Alert: {self.ticker} has crossed the threshold! Latest Price: {latest_price}")
            else:
                print(f"{self.ticker} is below the threshold. Latest Price: {latest_price}")

        except Exception as e:
            print(f"Error while checking price for {self.ticker}: {e}")

    def start_tracking(self, interval_minutes: int):
        """
        Start tracking the stock price at regular intervals.
        :param interval_minutes: Interval in minutes for checking the price.
        """
        schedule.every(interval_minutes).minutes.do(self.check_price)
        print(f"Started tracking {self.ticker} every {interval_minutes} minutes.")

        try:
            while True:
                schedule.run_pending()
                time.sleep(1)
        except KeyboardInterrupt:
            print("Stopped tracking.")

    def add_to_watchlist(self, ticker: str, threshold: float):
        """
        Add a stock to the watchlist for tracking.
        :param ticker: Stock ticker symbol.
        :param threshold: Price threshold for alerts.
        """
        self.watchlist.append((ticker.upper(), threshold))
        print(f"Added {ticker.upper()} with threshold {threshold} to the watchlist.")

    def show_watchlist(self):
        """Display the list of stocks being tracked."""
        if not self.watchlist:
            print("No stocks in the watchlist.")
        else:
            print("Current watchlist:")
            for ticker, threshold in self.watchlist:
                print(f"Ticker: {ticker}, Threshold: {threshold}")


if __name__ == "__main__": 
    tracker.start_tracking(interval_minutes)