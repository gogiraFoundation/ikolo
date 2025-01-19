import time
import yfinance as yf
import pandas as pd
import os
import sys
# Add the `src` directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))

from file_manager.cachedata import CacheData

class DataFetcher:
    """Class for fetching stock price data with rate limiting and caching."""
    
    # Add rate limit parameters (e.g., max requests per minute)
    RATE_LIMIT_TIME = 60  # Time window in seconds
    MAX_REQUESTS = 10  # Max number of requests in the given time window
    
    @staticmethod
    def fetch_stock_data(ticker: str, start_date: str, end_date: str) -> pd.DataFrame:
        """
        Fetch historical stock data from Yahoo Finance with caching and rate limiting.

        Args:
            ticker (str): Stock ticker symbol.
            start_date (str): Start date in YYYY-MM-DD format.
            end_date (str): End date in YYYY-MM-DD format.

        Returns:
            pd.DataFrame: DataFrame containing stock price data.
        """
        
        # Generate cache file name using CacheData class
        file_name = f"{ticker}_{start_date}_{end_date}.pkl"
        cache = CacheData(ticker, start_date, end_date, file_name)
        
        # Check if data is already cached
        cached_data = cache._load_cache()
        if cached_data is not None:
            return cached_data  # Return cached data if available
        
        # If data is not cached, fetch from Yahoo Finance
        try:
            stock = yf.Ticker(ticker)
            data = stock.history(start=start_date, end=end_date)
            
            # Rate limiting logic (we'll pause if necessary)
            time.sleep(DataFetcher.RATE_LIMIT_TIME / DataFetcher.MAX_REQUESTS)
            
            # Save data to cache
            cache._save_cache(data)
            return data.reset_index()  # Return the fetched data
        
        except Exception as e:
            print(f"Error: {e}")
            return pd.DataFrame()  # Return an empty DataFrame in case of failure
