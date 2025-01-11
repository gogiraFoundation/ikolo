from datetime import datetime
import yfinance as yf


def lookup_ticker(company_name):
    """
    Function to lookup the stock ticker symbol for a given company name.
    :param company_name: Name of the company to look up.
    :return: Ticker symbol if found, otherwise None.
    """
    try:
        # Fetching company data
        ticker = yf.Ticker(company_name)
        ticker_info = ticker.info

        # Check for the symbol key
        if 'symbol' in ticker_info:
            return ticker_info['symbol']
        else:
            print(f"Error: Ticker symbol for '{company_name}' not found.")
            return None
    except Exception as e:
        print(f"Error during ticker lookup for '{company_name}': {e}")
        return None


def is_valid_ticker(ticker):
    """
    Checks if the ticker is valid by ensuring it consists of only uppercase letters.
    :param ticker: Ticker symbol to validate.
    :return: True if valid, False otherwise.
    """
    try:
        return ticker.isalpha() and ticker.isupper() and len(ticker) <= 5
    except Exception as e:
        print(f"Error validating ticker '{ticker}': {e}")
        return False


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


class SaveFunction:
    """
    Class for managing and saving stock watchlists.
    """

    def __init__(self):
        """
        Initializes the SaveFunction with an empty watchlist.
        """
        self.watchlist = []

    def add_to_watchlist(self, ticker, threshold):
        """
        Adds a ticker and its threshold to the watchlist.
        :param ticker: Stock ticker symbol.
        :param threshold: Threshold price for the stock.
        """
        if not is_valid_ticker(ticker):
            print(f"Error: Invalid ticker symbol '{ticker}'.")
            return

        try:
            self.watchlist.append({'ticker': ticker, 'threshold': threshold})
            print(f"Added '{ticker}' with threshold '{threshold}' to the watchlist.")
        except Exception as e:
            print(f"Error adding to watchlist: {e}")

    def remove_from_watchlist(self, ticker):
        """
        Removes a ticker from the watchlist.
        :param ticker: Stock ticker symbol to remove.
        """
        try:
            self.watchlist = [item for item in self.watchlist if item['ticker'] != ticker]
            print(f"Removed '{ticker}' from the watchlist.")
        except Exception as e:
            print(f"Error removing ticker '{ticker}': {e}")

    def save_watchlist_to_file(self, file_path):
        """
        Saves the watchlist to a file.
        :param file_path: File path to save the watchlist.
        """
        try:
            with open(file_path, 'w') as f:
                for item in self.watchlist:
                    f.write(f"{item['ticker']},{item['threshold']}\n")
            print(f"Watchlist saved to '{file_path}'.")
        except Exception as e:
            print(f"Error saving watchlist to file: {e}")

    def load_watchlist_from_file(self, file_path):
        """
        Loads the watchlist from a file.
        :param file_path: File path to load the watchlist from.
        """
        try:
            with open(file_path, 'r') as f:
                self.watchlist = []
                for line in f:
                    ticker, threshold = line.strip().split(',')
                    self.watchlist.append({'ticker': ticker, 'threshold': float(threshold)})
            print(f"Watchlist loaded from '{file_path}'.")
        except Exception as e:
            print(f"Error loading watchlist from file: {e}")

    def show_watchlist(self):
        """
        Displays the current watchlist.
        """
        if not self.watchlist:
            print("Watchlist is empty.")
        else:
            print("Current Watchlist:")
            for item in self.watchlist:
                print(f"Ticker: {item['ticker']}, Threshold: {item['threshold']}")


# Usage
if __name__ == "__main__":
    save_func = SaveFunction()