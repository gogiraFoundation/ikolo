import time
import schedule
import json
from portfolio_manager.data_fetcher import DataFetcher
from datetime import datetime
import logging


# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')


class Tracker:
    """Class for tracking stock prices."""

    def __init__(self):
        """
        Initialize the Tracker instance.
        """
        self.fetcher = DataFetcher()
        self.watchlist = []

    def check_price(self):
        """Fetch the latest stock prices and check against thresholds."""
        for ticker, threshold in self.watchlist:
            try:
                current_date = datetime.now().strftime('%Y-%m-%d')
                current_time = datetime.now().strftime('%H:%M:%S')  # Add timestamp
                data = self.fetcher.fetch_stock_data(ticker, current_date, current_date)

                if data is None or data.empty:
                    logging.warning(f"No data available for {ticker} on {current_date}.")
                    continue

                latest_price = data['Close'].iloc[-1]

                if latest_price > threshold:
                    logging.info(f"Alert: {ticker} crossed the threshold! Latest Price: {latest_price} at {current_time}")
                else:
                    logging.info(f"{ticker} is below the threshold. Latest Price: {latest_price} at {current_time}")

            except Exception as e:
                logging.error(f"Error while checking price for {ticker}: {e}")

    def start_tracking(self, interval_minutes: int):
        """
        Start tracking the stock prices at regular intervals.
        :param interval_minutes: Interval in minutes for checking the prices.
        """
        schedule.every(interval_minutes).minutes.do(self.check_price)
        logging.info(f"Started tracking stocks every {interval_minutes} minutes.")

        try:
            while True:
                schedule.run_pending()
                time.sleep(1)
        except KeyboardInterrupt:
            logging.info("Stopped tracking.")
