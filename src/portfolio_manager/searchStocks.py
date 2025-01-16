import yfinance as yf
import sqlite3
import os
from datetime import datetime, timedelta


class StockSearcher:
    """Class for searching stocks with caching and API integration."""

    CACHE_EXPIRY = timedelta(days=1)  # Cache expiry time

    def __init__(self, tickers: list, db_path: str = "data/cache.db"):
        """
        Initialize the StockSearcher instance.

        Args:
            tickers (list): List of stock ticker symbols.
            db_path (str): Path to the SQLite database for caching.
        """
        self.tickers = tickers
        self.db_path = db_path
        self.connection = None
        self._initialize_cache()

    def _initialize_cache(self):
        """Initialize the SQLite cache database."""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self.connection = sqlite3.connect(self.db_path)
        cursor = self.connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS cache (
                ticker TEXT PRIMARY KEY,
                data TEXT,
                timestamp DATETIME
            )
        """)
        self.connection.commit()

    def _is_cache_valid(self, timestamp: str) -> bool:
        """
        Check if cached data is still valid.

        Args:
            timestamp (str): Timestamp string from the cache.

        Returns:
            bool: True if the cache is valid, False otherwise.
        """
        try:
            cache_time = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
            return datetime.now() - cache_time < self.CACHE_EXPIRY
        except ValueError:
            return False

    def fetch_metadata(self, ticker: str) -> dict:
        """
        Fetch stock metadata using Yahoo Finance, with caching.

        Args:
            ticker (str): Stock ticker symbol.

        Returns:
            dict: Metadata for the stock.
        """
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT data, timestamp FROM cache WHERE ticker = ?", (ticker,))
            row = cursor.fetchone()

            if row:
                cached_data, cached_time = row
                if self._is_cache_valid(cached_time):
                    print(f"Cache hit for {ticker}")
                    return eval(cached_data)  # Convert cached string back to dictionary

            print(f"Cache miss for {ticker}, fetching from API...")
            stock = yf.Ticker(ticker)
            info = stock.info
            metadata = {
                "ticker": ticker,
                "name": info.get("longName"),
                "industry": info.get("industry"),
                "sector": info.get("sector"),
                "dividend_yield": info.get("dividendYield", 0) * 100 if info.get("dividendYield") else None,
                "market_cap": info.get("marketCap")
            }

            # Update cache
            cursor.execute(
                "REPLACE INTO cache (ticker, data, timestamp) VALUES (?, ?, ?)",
                (ticker, str(metadata), datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            )
            self.connection.commit()
            return metadata
        except Exception as e:
            print(f"Error fetching metadata for {ticker}: {e}")
            return {}

    def close_connection(self):
        """Close the SQLite database connection."""
        if self.connection:
            self.connection.close()


