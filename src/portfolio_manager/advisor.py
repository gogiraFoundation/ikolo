import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))
from portfolio_manager.technical_analysis import TechnicalAnalysis
from portfolio_manager.metrics_calculator import MetricsCalculator
from portfolio_manager.fundamental_analysis import FundamentalAnalysis
import pandas as pd



class Advisor:
    """
    Class for providing stock advice based on technical and fundamental analysis.

    Methods:
    - generate_advice: Generate "Buy", "Sell", or "Hold" advice based on MACD and RSI indicators.
    - generate_combined_advice: Generate advice based on a combination of technical and fundamental indicators.
    """

    @staticmethod
    def generate_advice(data: pd.DataFrame, macd: pd.Series, signal: pd.Series, rsi: pd.Series) -> str:
        """
        Generate advice based on MACD and RSI indicators.

        Args:
            data (pd.DataFrame): Stock data with required columns.
            macd (pd.Series): MACD line values.
            signal (pd.Series): Signal line values.
            rsi (pd.Series): RSI values.

        Returns:
            str: "Buy", "Sell", or "Hold".
        """
        latest_macd = macd.iloc[-1]
        latest_signal = signal.iloc[-1]
        latest_rsi = rsi.iloc[-1]

        if latest_macd > latest_signal and latest_rsi < 30:
            return "Buy"
        elif latest_macd < latest_signal and latest_rsi > 70:
            return "Sell"
        else:
            return "Hold"

    @staticmethod
    def generate_combined_advice(
        data: pd.DataFrame,
        macd: pd.Series,
        signal: pd.Series,
        rsi: pd.Series,
        financial_ratios: dict
    ) -> str:
        """
        Generate advice based on a combination of technical and fundamental indicators.

        Args:
            data (pd.DataFrame): Stock data with required columns.
            macd (pd.Series): MACD line values.
            signal (pd.Series): Signal line values.
            rsi (pd.Series): RSI values.
            financial_ratios (dict): Fundamental ratios (e.g., P/E, EPS, etc.).

        Returns:
            str: "Buy", "Sell", or "Hold".
        """
        latest_macd = macd.iloc[-1]
        latest_signal = signal.iloc[-1]
        latest_rsi = rsi.iloc[-1]

        # Technical analysis advice
        technical_advice = Advisor.generate_advice(data, macd, signal, rsi)

        # Fundamental analysis check
        pe_ratio = financial_ratios.get("P/E Ratio (Trailing)", None)
        dividend_yield = financial_ratios.get("Dividend Yield (%)", None)

        # Determine fundamental indicators' contribution to advice
        fundamental_score = 0
        if pe_ratio and pe_ratio < 20:  # Undervalued stocks
            fundamental_score += 1
        if dividend_yield and dividend_yield > 3:  # Strong dividend yield
            fundamental_score += 1

        # Combine technical and fundamental signals
        if technical_advice == "Buy" and fundamental_score > 0:
            return "Strong Buy"
        elif technical_advice == "Sell" and fundamental_score == 0:
            return "Strong Sell"
        elif technical_advice == "Hold" and fundamental_score > 0:
            return "Accumulate"
        else:
            return technical_advice
