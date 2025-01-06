import pandas as pd
import numpy as np


class MetricsCalculator:
    """Class for calculating financial metrics."""
    
    @staticmethod
    def calculate_moving_average(data: pd.DataFrame, window: int) -> pd.Series:
        """
        Calculate moving average of stock prices.

        Args:
            data (pd.DataFrame): Stock data with a 'Close' column.
            window (int): Rolling window size.

        Returns:
            pd.Series: Moving average values.
        """
        return data['Close'].rolling(window=window).mean()

    @staticmethod
    def calculate_volatility(data: pd.DataFrame, window: int) -> pd.Series:
        """
        Calculate rolling volatility (standard deviation).

        Args:
            data (pd.DataFrame): Stock data with a 'Close' column.
            window (int): Rolling window size.

        Returns:
            pd.Series: Volatility values.
        """
        return data['Close'].rolling(window=window).std()
