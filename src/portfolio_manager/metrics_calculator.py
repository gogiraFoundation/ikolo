import pandas as pd
import numpy as np

class MetricsCalculator:
    """
    Class for calculating financial metrics.

    Metrics Explained:
    - Moving Average: Smooths out stock price data by calculating the average over a rolling window.
    - Volatility: Measures the standard deviation of stock prices over a rolling window.
    - Total Revenue: The total value of goods and services sold by a company.
    - Capital Expenditure (CapEx): Total spending on purchasing or maintaining fixed assets.
    - Total Assets: Total value of capital items owned by a company.
    - Total Liabilities: Total amount of debts and financial obligations of a company.
    - Cash and Cash Equivalents: Liquid assets that are cash or can be quickly converted to cash.
    - Price-to-Earnings (P/E) Ratio: A company's stock price divided by its earnings per share.
    - Debt-to-Equity (D/E) Ratio: Measures financial leverage by comparing total liabilities to total equity.
    - Return on Equity (ROE): Measures a company's profitability relative to shareholders' equity.
    - Net Profit Margin: Percentage of revenue that translates into profit.
    """

    METRICS_EXPLANATION = {
        "calculate_moving_average": "Calculates the rolling average of stock prices over a specified window.",
        "calculate_volatility": "Calculates the standard deviation of stock prices over a rolling window.",
        "calculate_price_to_earnings": "Calculates the Price-to-Earnings (P/E) ratio to evaluate stock valuation.",
        "calculate_debt_to_equity_ratio": "Calculates the Debt-to-Equity (D/E) ratio to assess financial leverage.",
        "calculate_return_on_equity": "Calculates Return on Equity (ROE) to measure profitability relative to shareholders' equity.",
        "calculate_net_profit_margin": "Calculates the percentage of revenue that is retained as net income.",
    }

    @staticmethod
    def calculate_moving_average(data: pd.DataFrame, window: int) -> pd.Series:
        """
        Calculate the moving average of stock prices.

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

    @staticmethod
    def calculate_price_to_earnings(price: float, earnings_per_share: float) -> float:
        """
        Calculate the Price-to-Earnings (P/E) ratio.

        Args:
            price (float): Stock price.
            earnings_per_share (float): Earnings per share (EPS).

        Returns:
            float: P/E ratio.
        """
        try:
            return price / earnings_per_share
        except ZeroDivisionError:
            return np.nan

    @staticmethod
    def calculate_debt_to_equity_ratio(total_liabilities: float, total_equity: float) -> float:
        """
        Calculate the Debt-to-Equity (D/E) ratio.

        Args:
            total_liabilities (float): Total liabilities of the company.
            total_equity (float): Total equity of the company.

        Returns:
            float: D/E ratio.
        """
        try:
            return total_liabilities / total_equity
        except ZeroDivisionError:
            return np.nan

    @staticmethod
    def calculate_return_on_equity(net_income: float, total_equity: float) -> float:
        """
        Calculate Return on Equity (ROE).

        Args:
            net_income (float): Net income of the company.
            total_equity (float): Total equity of the company.

        Returns:
            float: ROE percentage.
        """
        try:
            return (net_income / total_equity) * 100
        except ZeroDivisionError:
            return np.nan

    @staticmethod
    def calculate_net_profit_margin(net_income: float, total_revenue: float) -> float:
        """
        Calculate the net profit margin.

        Args:
            net_income (float): Net income of the company.
            total_revenue (float): Total revenue of the company.

        Returns:
            float: Net profit margin percentage.
        """
        try:
            return (net_income / total_revenue) * 100
        except ZeroDivisionError:
            return np.nan