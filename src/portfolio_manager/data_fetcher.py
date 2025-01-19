import time
import yfinance as yf
import pandas as pd
import os
import sys
from datetime import datetime

# Add the `src` directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))

from file_manager.fileManager import FileManager


class DataFetcher:
    """Class for fetching stock price data with rate limiting and caching."""

    # Rate limit parameters (e.g., max requests per minute)
    RATE_LIMIT_TIME = 60  # Time window in seconds
    MAX_REQUESTS = 10  # Max number of requests in the given time window

    def __init__(self, cache_dir: str = "data/sys_file/cache_dir/"):
        """
        Initialize the DataFetcher instance.

        Args:
            cache_dir (str): Directory to store cache files.
        """
        self.cache_dir = cache_dir
        self.file_manager = FileManager()
        self.file_manager.ensure_directory_exists(self.cache_dir)

    def fetch_stock_data(self, ticker: str, start_date: str, end_date: str) -> pd.DataFrame:
        """
        Fetch historical stock data from Yahoo Finance with caching and rate limiting.

        Args:
            ticker (str): Stock ticker symbol.
            start_date (str): Start date in YYYY-MM-DD format.
            end_date (str): End date in YYYY-MM-DD format.

        Returns:
            pd.DataFrame: DataFrame containing stock price data.
        """
        # Generate cache file path
        cache_file = os.path.join(self.cache_dir, f"{ticker}_{start_date}_{end_date}.pkl")

        # Check if data is already cached
        if self.file_manager.ensure_directory_exists(cache_file):
            cached_data = pd.read_pickle(cache_file)
            print(f"Cache hit: Loaded data for {ticker} from {cache_file}")
            return cached_data

        # If data is not cached, fetch from Yahoo Finance
        try:
            print(f"Cache miss: Fetching data for {ticker} from Yahoo Finance...")
            stock = yf.Ticker(ticker)
            data = stock.history(start=start_date, end=end_date)

            # Rate limiting logic
            time.sleep(self.RATE_LIMIT_TIME / self.MAX_REQUESTS)

            # Save data to cache
            pd.to_pickle(data, cache_file)
            print(f"Data for {ticker} cached at {cache_file}")
            return data.reset_index()  # Return the fetched data

        except Exception as e:
            print(f"Error: {e}")
            return pd.DataFrame()  # Return an empty DataFrame in case of failure