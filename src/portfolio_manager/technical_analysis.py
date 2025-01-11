import pandas as pd

class TechnicalAnalysis:
    """Class for performing technical analysis."""


    @staticmethod
    
    
    def calculate_rsi(data: pd.DataFrame, window: int=14) -> pd.Series:

        """
        Calculate Relative Strength Index (RSI).

        Args:
            data (pd.DataFrame): Stock data with a 'Close' column.
            window (int): Period for RSI calculation.

        Returns:
            pd.Series: RSI values.
        """

        delta = data['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
        loss = (-delta.where(delta < 0, )).rolling(window=window).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi
    

    @staticmethod
    
    def calculate_macd(data: pd.DataFrame, fast_period: int = 12, slow_period: int = 26, signal_period: int = 9):
        """
        Calculate MACD and Signal Line.

        Args:
            data (pd.DataFrame): Stock data with a 'Close' column.
            fast_period (int): Short-term EMA period.
            slow_period (int): Long-term EMA period.
            signal_period (int): Signal line EMA period.

        Returns:
            tuple: MACD line and Signal line as pd.Series.
        """
        ema_fast = data['Close'].ewm(span=fast_period, adjust=False).mean()
        ema_slow = data['Close'].ewm(span=slow_period, adjust=False).mean()
        macd = ema_fast - ema_slow
        signal = macd.ewm(span=signal_period, adjust=False).mean()
        return macd, signal
