import time
import yfinance as yf
import pandas as pd
import os
import sys
from datetime import datetime
from typing import Optional

# Add the `src` directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "src")))
from file_manager.fileManager import FileManager
from logs.logger import Logger


class DataFetcher:
    """Class for fetching stock price data with rate limiting and caching."""

    # Rate limit parameters (e.g., max requests per minute)
    RATE_LIMIT_TIME = 60  # Time window in seconds
    MAX_REQUESTS = 10  # Max number of requests in the given time window

    def __init__(self, base_dir: str, cache_dir: str = "data/sys_file/cache_dir/"):
        """
        Initialize the DataFetcher instance.

        Args:
            cache_dir (str): Directory to store cache files.
        """
        self.cache_dir = cache_dir
        self.file_manager = FileManager(base_dir=base_dir)
        self.file_manager.ensure_directory_exists(self.cache_dir)
        self.logger = Logger("DataFetcher")
        self.request_count = 0
        self.start_time = time.time()

    def _check_rate_limit(self):
        """
        Check and enforce the rate limit.
        Delays execution if the rate limit is exceeded.
        """
        self.request_count += 1
        elapsed_time = time.time() - self.start_time

        if elapsed_time > self.RATE_LIMIT_TIME:
            # Reset the timer and request count if the time window has passed
            self.start_time = time.time()
            self.request_count = 1

        elif self.request_count > self.MAX_REQUESTS:
            # Calculate the time to wait before making the next request
            wait_time = self.RATE_LIMIT_TIME - elapsed_time
            self.logger.log_info(f"Rate limit exceeded. Waiting {wait_time:.2f} seconds.")
            time.sleep(wait_time)
            self.start_time = time.time()
            self.request_count = 1

    def fetch_stock_data(self, ticker: str, start_date: str, end_date: str) -> Optional[pd.DataFrame]:
        """
        Fetch historical stock data from Yahoo Finance with caching and rate limiting.

        Args:
            ticker (str): Stock ticker symbol.
            start_date (str): Start date in YYYY-MM-DD format.
            end_date (str): End date in YYYY-MM-DD format.

        Returns:
            Optional[pd.DataFrame]: DataFrame containing stock price data, or None if an error occurs.
        """
        try:
            # Generate cache file path
            cache_file = os.path.join(self.cache_dir, f"{ticker}_{start_date}_{end_date}.pkl")

            # Check if data is already cached
            if os.path.isfile(cache_file):
                self.logger.log_info(f"Cache hit: Loaded data for {ticker} from {cache_file}")
                return pd.read_pickle(cache_file)

            # If data is not cached, fetch from Yahoo Finance
            self.logger.log_info(f"Cache miss: Fetching data for {ticker} from Yahoo Finance...")
            self._check_rate_limit()

            stock = yf.Ticker(ticker)
            data = stock.history(start=start_date, end=end_date)

            if data.empty:
                self.logger.log_warning(f"No data found for ticker '{ticker}' from {start_date} to {end_date}.")
                return None

            # Save data to cache
            pd.to_pickle(data, cache_file)
            self.logger.log_info(f"Data for {ticker} cached at {cache_file}")

            return data.reset_index()

        except Exception as e:
            self.logger.log_error(f"Error fetching data for {ticker}: {e}")
            return None
