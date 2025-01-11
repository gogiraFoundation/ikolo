import yfinance as yf
import pandas as pd


class DataFetcher:
    """Class for fetching stock price data."""
    
    @staticmethod
    def fetch_stock_data(ticker: str, start_date: str, end_date: str) -> pd.DataFrame:
        """
        Fetch historical stock data from Yahoo Finance.

        Args:
            ticker (str): Stock ticker symbol.
            start_date (str): Start date in YYYY-MM-DD format.
            end_date (str): End date in YYYY-MM-DD format.

        Returns:
            pd.DataFrame: DataFrame containing stock price data.
        """
        try:
            stock = yf.Ticker(ticker)
            data = stock.history(start=start_date, end=end_date)
            return data.reset_index()
        except Exception as e:
            print(f"Error: {e}")
