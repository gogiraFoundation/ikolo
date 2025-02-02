import os
import json
import sys
from pathlib import Path

# Add the `src` directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))


from portfolio_manager.visualizer import Visualizer
from portfolio_manager.metrics_calculator import MetricsCalculator
from portfolio_manager.data_fetcher import DataFetcher
from portfolio_manager.technical_analysis import TechnicalAnalysis
from portfolio_manager.fundamental_analysis import FundamentalAnalysis
from portfolio_manager.advisor import Advisor
from portfolio_manager.portfolio_operations import PortfolioOperations
from portfolio_manager.searchStocks import StockSearcher
from portfolio_manager.tracker import Tracker
from handlers.handlers import WatchlistManager
from handlers.utilityHandler import UtilityHandler
from sessionManager.session_manager import SessionManager
from login_system_manager.login_system import LoginSystem
from logs.logger import Logger
from file_manager.fileManager import FileManager


class PortfolioManagerApp:
    """
    Portfolio Management Application for stock analysis and portfolio tracking.
    """

    def __init__(self, base_dir=None):
        self.logger = Logger("PortfolioManagerApp")
        # Ensure base_dir is properly set
        self.base_dir = Path(base_dir).resolve()
        # Initialize file manager with the correct base directory
        self.file_manager = FileManager(base_dir=self.base_dir)
        self._load_configuration()
        self._initialize_modules()

        

    def _initialize_modules(self):
        """Initialize core modules."""
        self.searcher = StockSearcher(tickers=self.default_tickers,  base_dir=self.base_dir)
        self.tracker = Tracker(base_dir=self.base_dir)
        self.session_manager = SessionManager(base_dir=self.base_dir)
        self.visualizer = Visualizer(base_dir=self.base_dir)
        self.calculator = MetricsCalculator()
        self.fetcher = DataFetcher(base_dir=self.base_dir)
        self.technical_analysis = TechnicalAnalysis()
        self.fundamental_analysis = FundamentalAnalysis()
        self.advisor = Advisor()
        self.watchlist_manager = WatchlistManager(base_dir=self.base_dir)
        self.portfolio_operations = PortfolioOperations(base_dir=self.base_dir, portfolio_file=self.portfolio_file)

    def _load_configuration(self):
        try:
            """Load application configuration from a file, or create defaults."""
            config_path = os.path.join(self.base_dir, "config.json")

            if not os.path.exists(config_path):
                self.logger.log_warning("Config file not found. Creating default config...")
                default_config = {
                    "default_tickers": ["AAPL", "MSFT", "GOOGL"],
                    "data_directory": "./data",
                    "watchlist_subdir": "watchlist",
                    "portfolio_subdir": "portfolio",
                }
                self.file_manager.save_json_file(config_path, default_config)

            # Load settings from config
            config = self.file_manager.load_json_file(config_path)
            self.default_tickers = config.get("default_tickers", ["AAPL", "MSFT", "GOOGL"])
            self.data_directory = os.path.abspath(config.get("data_directory", "./data"))
            self.watchlist_dir = os.path.join(self.data_directory, config.get("watchlist_subdir", "watchlist"))
            self.portfolio_dir = os.path.join(self.data_directory, config.get("portfolio_subdir", "portfolio"))

            os.makedirs(self.data_directory, exist_ok=True)
            os.makedirs(self.watchlist_dir, exist_ok=True)
            os.makedirs(self.portfolio_dir, exist_ok=True)

            self.portfolio_file = os.path.join(self.portfolio_dir, "portfolio.json")
            self.watchlist_file = os.path.join(self.watchlist_dir, "watchlist.json")
            self.logger.log_info(f"Configuration loaded: {config}")

        except Exception as e:
            self.logger.log_error(f"Error loading configuration: {e}")
            raise
    
    def perform_analysis(self, ticker, start_date, end_date):
        """Perform stock analysis."""
        self.logger.log_info(f"Starting stock analysis for {ticker}...")
        try:
            if not UtilityHandler.validate_ticker(ticker):
                raise ValueError(f"Invalid ticker: {ticker}")
            if not UtilityHandler.validate_dates(start_date, end_date):
                raise ValueError(f"Invalid date range: {start_date} - {end_date}")

            return self._analyze_stock(ticker, start_date, end_date)
        except Exception as e:
            self.logger.log_error(f"Error during stock analysis for ticker {ticker}: {e}")
            return {"status": "error", "message": str(e)}

    def _analyze_stock(self, ticker, start_date, end_date):
        """Helper method to analyze a stock."""
        try:
            data = self.fetcher.fetch_stock_data(ticker, start_date, end_date)
            if data.empty:
                self.logger.log_warning(f"No data found for ticker '{ticker}'.")
                return {"status": "error", "message": "No data found."}

            moving_avg = self.calculator.calculate_moving_average(data, 20)
            volatility = self.calculator.calculate_volatility(data, 20)
            macd, signal = self.technical_analysis.calculate_macd(data)
            rsi = self.technical_analysis.calculate_rsi(data)
            ratios = self.fundamental_analysis.get_financial_ratios(ticker)
            advice = self.advisor.generate_advice(data, macd, signal, rsi)

            return {
                "status": "success",
                "message": "Stock analysis completed successfully.",
                "data": {
                    "ticker": ticker,
                    "fundamental_ratios": ratios,
                    "advice": advice
                }
            }
        except Exception as e:
            self.logger.log_error(f"Error during stock analysis for ticker {ticker}: {str(e)}")
            return {"status": "error", "message": str(e)}
    
    def search_stocks(self, tickers):
        """Search for stock metadata."""
        try:
            stock_metadata = {ticker: self.searcher.fetch_metadata(ticker) for ticker in tickers}
            return {"status": "success", "data": stock_metadata}
        except Exception as e:
            #self.logger.log_error(f"Error during stock search: {str{e}}")
            return {"status": "error", "message": str(e)}
        finally:
            self.searcher.close_connection()

    def track_stocks(self, ticker, threshold):
        """Track a stock with a threshold alert."""
        try:
            if not UtilityHandler.validate_ticker(ticker) or not isinstance(threshold, (int, float)):
                return {"status": "error", "message": "Invalid ticker or threshold."}

            threshold = UtilityHandler.validate_threshold(threshold)

            # Ensure the watchlist directory exists
            self.file_manager.ensure_directory_exists(self.watchlist_dir)

            # Add stock to the watchlist
            self.watchlist_manager.add_to_watchlist(ticker, threshold)

            # Save the watchlist to the watchlist file
            self.watchlist_manager.save_to_file(self.watchlist_file)

            self.logger.log_info(f"Tracking {ticker} with a threshold of {threshold}.")
            result = {
                "status": "success",
                "message": f"Tracking {ticker} with a threshold of {threshold}."
            }
            return result
        except ValueError as e:
            self.logger.log_warning(f"Invalid input: {e}")
            raise
        except Exception as e:
            self.logger.log_error(f"Unexpected error while tracking stock: {e}")
            return {"status": "error", "message": str(e)}
            raise


    def portfolio_actions(self):
        """Perform portfolio operations."""
        try:
            self.portfolio_operations._portfolio_operations_run()
        except Exception as e:
            self.logger.log_error(f"Unexpected error while performing portfolio actions: {e}")
            raise

    def run(self):
        """Run the application logic externally controlled."""
        self.logger.log_info("PortfolioManagerApp initialized and ready.")
