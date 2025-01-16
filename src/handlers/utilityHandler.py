from portfolio_manager.visualizer import Visualizer
from portfolio_manager.metrics_calculator import MetricsCalculator
from portfolio_manager.data_fetcher import DataFetcher
from portfolio_manager.technical_analysis import TechnicalAnalysis
from portfolio_manager.fundamental_analysis import FundamentalAnalysis
from portfolio_manager.advisor import Advisor
from portfolio_manager.searchStocks import StockSearcher
from portfolio_manager.tracker import Tracker
from login_system_manager.login_system import LoginSystem
from sessionManager.session_manager import SessionManager
from handlers.handlers import is_valid_date, is_valid_ticker, lookup_ticker


class UtilityHandler:
    """Handles utility functions like validations and calculations."""

    @staticmethod
    def validate_ticker(ticker):
        if is_valid_ticker(ticker):
            return ticker
        return lookup_ticker(ticker)

    @staticmethod
    def validate_dates(start_date, end_date):
        if is_valid_date(start_date) and is_valid_date(end_date):
            return start_date, end_date
        return None, None

    @staticmethod
    def validate_window_sizes(moving_avg_window, volatility_window):
        if moving_avg_window > 0 and volatility_window > 0:
            return moving_avg_window, volatility_window
        return None, None