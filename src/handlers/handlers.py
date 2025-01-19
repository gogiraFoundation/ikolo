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


def ensure_directory_exists(file_path):
    """
    Ensures that the directory for the given file path exists.
    Creates the directory if it does not exist.
    :param file_path: File path whose directory needs to be checked.
    :return: The full file path with the ensured directory.
    """
    # Define base directory for data
    base_directory = os.path.join(os.getcwd(), "data")

    # Create the full path for the file
    full_path = os.path.join(base_directory, file_path)

    # Extract directory from the full path
    directory = os.path.dirname(full_path)

    # Create the directory if it doesn't exist
    if not os.path.exists(directory):
        os.makedirs(directory)
        print(f"Directory '{directory}' created.")
    else:
        print(f"Directory '{directory}' already exists.")

    return full_path



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


class PortfolioManager:
    """
    Class for managing stock portfolios.
    """
    def __init__(self):
        self._file_manager_ = FileManager()
        self.logger = Logger(name="PortfolioManager")
        self.portfolio = []

    def add_to_portfolio(self, ticker, shares, purchase_price):
        if not is_valid_ticker(ticker):
            self.logger.log_error(f"Invalid ticker symbol '{ticker}'.")
            print(f"Error: Invalid ticker symbol '{ticker}'.")
            return
        self.portfolio.append({'ticker': ticker, 'shares': shares, 'purchase_price': purchase_price})
        self.logger.log_info(f"Added {shares} shares of '{ticker}' at ${purchase_price:.2f} to the portfolio.")
        print(f"Added {shares} shares of '{ticker}' at ${purchase_price:.2f} to the portfolio.")

    def save_to_file(self, file_path):
        try:
            full_path = self._file_manager_.ensure_directory_exists(file_path)
            with open(full_path, 'w') as f:
                for item in self.portfolio:
                    f.write(f"{item['ticker']},{item['shares']},{item['purchase_price']}\n")
            self.logger.log_info(f"Portfolio saved to '{full_path}'.")
            print(f"Portfolio saved to '{full_path}'.")
        except Exception as e:
            self.logger.log_error(f"Error saving portfolio to file: {e}")
            print(f"Error saving portfolio to file: {e}")

    def load_from_file(self, file_path):
        try:
            full_path = self._file_manager_.ensure_directory_exists(file_path)
            with open(full_path, 'r') as f:
                self.portfolio = [
                    {'ticker': line.split(',')[0], 'shares': int(line.split(',')[1]), 'purchase_price': float(line.split(',')[2].strip())}
                    for line in f
                ]
            self.logger.log_info(f"Portfolio loaded from '{full_path}'.")
            print(f"Portfolio loaded from '{full_path}'.")
        except Exception as e:
            self.logger.log_error(f"Error loading portfolio from file: {e}")
            print(f"Error loading portfolio from file: {e}")



class PortfolioManager:
    """
    Class for managing stock portfolios.
    """
    def __init__(self):
        self._file_manager_ = FileManager()
        self.logger = Logger(name="PortfolioManager")
        self.portfolio = []

    def add_to_portfolio(self, ticker, shares, purchase_price):
        if not is_valid_ticker(ticker):
            self.logger.log_error(f"Invalid ticker symbol '{ticker}'.")
            print(f"Error: Invalid ticker symbol '{ticker}'.")
            return
        self.portfolio.append({'ticker': ticker, 'shares': shares, 'purchase_price': purchase_price})
        self.logger.log_info(f"Added {shares} shares of '{ticker}' at ${purchase_price:.2f} to the portfolio.")
        print(f"Added {shares} shares of '{ticker}' at ${purchase_price:.2f} to the portfolio.")

    def save_to_file(self, file_path):
        try:
            full_path = self._file_manager_.ensure_directory_exists(file_path)
            with open(full_path, 'w') as f:
                for item in self.portfolio:
                    f.write(f"{item['ticker']},{item['shares']},{item['purchase_price']}\n")
            self.logger.log_info(f"Portfolio saved to '{full_path}'.")
            print(f"Portfolio saved to '{full_path}'.")
        except Exception as e:
            self.logger.log_error(f"Error saving portfolio to file: {e}")
            print(f"Error saving portfolio to file: {e}")

    def load_from_file(self, file_path):
        try:
            full_path = self._file_manager_.ensure_directory_exists(file_path)
            with open(full_path, 'r') as f:
                self.portfolio = [
                    {'ticker': line.split(',')[0], 'shares': int(line.split(',')[1]), 'purchase_price': float(line.split(',')[2].strip())}
                    for line in f
                ]
            self.logger.log_info(f"Portfolio loaded from '{full_path}'.")
            print(f"Portfolio loaded from '{full_path}'.")
        except Exception as e:
            self.logger.log_error(f"Error loading portfolio from file: {e}")
            print(f"Error loading portfolio from file: {e}")