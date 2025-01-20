from datetime import datetime
import yfinance as yf
import os
import json
import os
import sys

# Add the `src` directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))
from logs.logger import Logger
from file_manager.fileManager import FileManager


def lookup_ticker(company_name):
    """
    Function to lookup the stock ticker symbol for a given company name.
    :param company_name: Name of the company to look up.
    :return: Ticker symbol if found, otherwise None.
    """
    try:
        ticker = yf.Ticker(company_name)
        ticker_info = ticker.info

        return ticker_info.get('symbol', None)
    except Exception as e:
        print(f"Error during ticker lookup for '{company_name}': {e}")
        return None


def is_valid_ticker(ticker):
    """
    Checks if the ticker is valid by ensuring it consists of only uppercase letters.
    :param ticker: Ticker symbol to validate.
    :return: True if valid, False otherwise.
    """
    return ticker.isalpha() and ticker.isupper() and len(ticker) <= 5


def is_valid_date(date_str):
    """
    Checks if the input string is a valid date in the format YYYY-MM-DD.
    :param date_str: Date string to validate.
    :return: True if valid, False otherwise.
    """
    try:
        datetime.strptime(date_str, '%Y-%m-%d')
        return True
    except ValueError:
        return False

class WatchlistManager:
    """
    Class for managing stock watchlists.
    """
    def __init__(self):
        self._file_manager_ = FileManager()
        self.logger = Logger(name="WatchlistManager")
        self.watchlist = []

    def add_to_watchlist(self, ticker, threshold):
        if not is_valid_ticker(ticker):
            self.logger.log_error(f"Invalid ticker symbol '{ticker}'.")
            print(f"Error: Invalid ticker symbol '{ticker}'.")
            return
        self.watchlist.append({'ticker': ticker, 'threshold': threshold})
        self.logger.log_info(f"Added '{ticker}' with threshold '{threshold}' to the watchlist.")
    

    def remove_from_watchlist(self, ticker):
        self.watchlist = [item for item in self.watchlist if item['ticker'] != ticker]
        self.logger.log_info(f"Removed '{ticker}' from the watchlist.")
        print(f"Removed '{ticker}' from the watchlist.")

    def save_to_file(self, file_path):
        """Save the watchlist to a file."""
        try:
            # Ensure the parent directory exists
            parent_dir = os.path.dirname(file_path)
            if not os.path.exists(parent_dir):
                os.makedirs(parent_dir)

            # Save the watchlist to the file
            with open(file_path, 'w') as f:
                for item in self.watchlist:
                    f.write(f"{item['ticker']},{item['threshold']}\n")
            
            self.logger.log_info(f"Watchlist saved to '{file_path}'.")
            print(f"Watchlist saved to '{file_path}'.")

        except PermissionError:
            self.logger.log_error(f"Permission denied when trying to save watchlist to file: {file_path}")
            print(f"Permission denied when trying to save watchlist to file: {file_path}")

        except Exception as e:
            self.logger.log_error(f"Error saving watchlist to file: {e}")
            print(f"Error saving watchlist to file: {e}")


    def load_from_file(self, file_path):
        try:
            full_path = self._file_manager_.ensure_directory_exists(file_path)
            with open(full_path, 'r') as f:
                self.watchlist = [
                    {'ticker': line.split(',')[0], 'threshold': float(line.split(',')[1].strip())}
                    for line in f
                ]
            self.logger.log_info(f"Watchlist loaded from '{full_path}'.")
            print(f"Watchlist loaded from '{full_path}'.")
        except Exception as e:
            self.logger.log_error(f"Error loading watchlist from file: {e}")
            print(f"Error loading watchlist from file: {e}")

    def show_watchlist(self):
        if not self.watchlist:
            self.logger.log_info("Watchlist is empty.")
            print("Watchlist is empty.")
        else:
            self.logger.log_info("Displaying current watchlist.")
            print("Current Watchlist:")
            for item in self.watchlist:
                print(f"Ticker: {item['ticker']}, Threshold: {item['threshold']}")


class PortfolioManager:
    """
    Class for managing stock portfolios.
    """
    def __init__(self):
        self._file_manager_ = FileManager()
        self.logger = Logger(name="PortfolioManager")
        self.portfolio = {}

    def add_to_portfolio(self, user_email, ticker, shares, purchase_price):
        try:
            if not isinstance(shares, (int, float)) or shares <= 0:
                raise ValueError("Shares must be a positive number.")
            if not isinstance(purchase_price, (int, float)) or purchase_price <= 0:
                raise ValueError("Purchase price must be a positive number.")
            if not is_valid_ticker(ticker):
                self.logger.log_error(f"Invalid ticker symbol '{ticker}'.")
                print(f"Error: Invalid ticker symbol '{ticker}'.")
                return

            if user_email not in self.portfolio:
                self.portfolio[user_email] = []

            self.portfolio[user_email].append({
                'ticker': ticker,
                'shares': shares,
                'purchase_price': purchase_price
            })
            self.logger.log_info(
                f"Added {shares} shares of '{ticker}' at ${purchase_price:.2f} to {user_email}'s portfolio.")
            print(f"Added {shares} shares of '{ticker}' at ${purchase_price:.2f} to {user_email}'s portfolio.")
        except Exception as e:
            self.logger.log_error(f"Error adding to portfolio: {e}")
            raise

    def calculate_performance(self, user_email):
        try:
            if user_email not in self.portfolio:
                raise ValueError(f"No portfolio found for user: {user_email}")

            portfolio = self.portfolio[user_email]
            total_return = 0
            total_dividends = 0
            details = []

            for stock in portfolio:
                ticker = stock["ticker"]
                shares = stock["shares"]
                purchase_price = stock["purchase_price"]

                try:
                    stock_data = yf.Ticker(ticker)
                    current_price = stock_data.info.get("regularMarketPrice", 0) or 0
                    dividend_yield = stock_data.info.get("dividendYield", 0) * 100 if stock_data.info.get(
                        "dividendYield") else 0
                except Exception as e:
                    self.logger.log_error(f"Error fetching data for ticker '{ticker}': {e}")
                    current_price = 0
                    dividend_yield = 0

                stock_return = (current_price - purchase_price) * shares
                stock_dividends = (dividend_yield / 100) * current_price * shares

                total_return += stock_return
                total_dividends += stock_dividends

                details.append({
                    "Ticker": ticker,
                    "Shares": shares,
                    "Purchase Price": purchase_price,
                    "Current Price": current_price,
                    "Return": stock_return,
                    "Dividend Income": stock_dividends
                })

            return {
                "total_return": total_return,
                "total_dividends": total_dividends,
                "details": details
            }
        except Exception as e:
            self.logger.log_critical(f"Operation Failed: {e}")
            raise

    def save_to_file(self, file_path):
        try:
            full_path = self._file_manager_.ensure_directory_exists(file_path)
            with open(full_path, 'w') as f:
                json.dump(self.portfolio, f)
            self.logger.log_info(f"Portfolio saved to '{full_path}'.")
        except Exception as e:
            self.logger.log_error(f"Error saving portfolio: {e}")

    def load_from_file(self, file_path):
        try:
            full_path = self._file_manager_.ensure_directory_exists(file_path)
            if os.path.exists(full_path):
                with open(full_path, 'r') as f:
                    self.portfolio = json.load(f)
                self.logger.log_info(f"Portfolio loaded from '{full_path}'.")
            else:
                self.logger.log_warning(f"No portfolio file found at '{full_path}'. Starting with an empty portfolio.")
                self.portfolio = {}
        except Exception as e:
            self.logger.log_error(f"Error loading portfolio: {e}")

    
    def portfolio_report_generator(self, file_path, output_file):
        """
        Generates an Excel report for the portfolio data.
        :param file_path: Path to the portfolio JSON file.
        :param output_file: Path to save the Excel report.
        """
        try:
            # Ensure the directory and file exist
            full_path = self._file_manager_.ensure_directory_exists(file_path)

            # Check if the file exists before attempting report generation
            if not os.path.exists(full_path):
                self.logger.log_warning(f"Portfolio file '{full_path}' does not exist. Cannot generate report.")
                print(f"Warning: Portfolio file '{full_path}' does not exist. Cannot generate report.")
                return

            # Generate the report using FileManager's method
            self._file_manager_.generate_report(full_path, output_file)

            self.logger.log_info(f"Portfolio report generated and saved to '{output_file}'.")
            print(f"Portfolio report generated and saved to '{output_file}'.")

        except Exception as e:
            self.logger.log_error(f"Error generating portfolio report: {e}")
            print(f"Error generating portfolio report: {e}")
            raise
