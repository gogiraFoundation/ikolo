import pandas as pd

class TechnicalAnalysis:
    """
    Class for performing technical analysis.

    Methods:
    - calculate_rsi: Calculates the Relative Strength Index (RSI).
    - calculate_macd: Calculates the MACD line and Signal line.
    """

    @staticmethod
    def calculate_rsi(data: pd.DataFrame, window: int = 14) -> pd.Series:
        """
        Calculate Relative Strength Index (RSI).

        Args:
            data (pd.DataFrame): Stock data with a 'Close' column.
            window (int): Period for RSI calculation (default: 14).

        Returns:
            pd.Series: RSI values.
        """
        if 'Close' not in data:
            raise ValueError("Input DataFrame must contain a 'Close' column.")

        # Calculate price changes
        delta = data['Close'].diff()

        # Separate gains and losses
        gain = delta.where(delta > 0, 0)
        loss = -delta.where(delta < 0, 0)

        # Calculate rolling averages
        avg_gain = gain.rolling(window=window, min_periods=1).mean()
        avg_loss = loss.rolling(window=window, min_periods=1).mean()

        # Calculate Relative Strength (RS)
        rs = avg_gain / avg_loss

        # Calculate RSI
        rsi = 100 - (100 / (1 + rs))
        return rsi

    @staticmethod
    def calculate_macd(
        data: pd.DataFrame,
        fast_period: int = 12,
        slow_period: int = 26,
        signal_period: int = 9
    ) -> tuple:
        """
        Calculate Moving Average Convergence Divergence (MACD) and Signal Line.

        Args:
            data (pd.DataFrame): Stock data with a 'Close' column.
            fast_period (int): Short-term EMA period (default: 12).
            slow_period (int): Long-term EMA period (default: 26).
            signal_period (int): Signal line EMA period (default: 9).

        Returns:
            tuple: MACD line and Signal line as pd.Series.
        """
        if 'Close' not in data:
            raise ValueError("Input DataFrame must contain a 'Close' column.")

        # Calculate EMAs
        ema_fast = data['Close'].ewm(span=fast_period, adjust=False).mean()
        ema_slow = data['Close'].ewm(span=slow_period, adjust=False).mean()

        # Calculate MACD line and Signal line
        macd = ema_fast - ema_slow
        signal = macd.ewm(span=signal_period, adjust=False).mean()

        return macd, signal
