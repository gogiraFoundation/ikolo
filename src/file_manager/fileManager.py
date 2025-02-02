import json
import os
import sys
from pathlib import Path
import yfinance as yf  # Required for fetching stock data

# Add the `src` directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))
from logs.logger import Logger


class FileManager:
    """Manages actions related to file and directory interactions."""

    def __init__(self, base_dir, logger=None):
        self.logger = logger or Logger("FileManager")
        self.base_dir = Path(base_dir).resolve()
        self.data_dir = self.base_dir / "data"
        self.watchlist_dir = self.data_dir / "watchlist"
        self.portfolio_dir = self.data_dir / "portfolio"

        # Create required directories
        self.data_dir.mkdir(exist_ok=True)
        self.watchlist_dir.mkdir(exist_ok=True)
        self.portfolio_dir.mkdir(exist_ok=True)

    def ensure_directory_exists(self, path):
        """Ensure the directory for a given path exists."""
        try:
            directory = os.path.dirname(path)
            if directory:
                os.makedirs(directory, exist_ok=True)
                if self.logger:
                    self.logger.log_info(f"Verified or created directory: {directory}")
            return directory
        except Exception as e:
            if self.logger:
                self.logger.log_critical(f"Failed to create directory for {path}. Exception: {e}")
            raise

    def load_json_file(self, file_path):
        """Load data from a JSON file."""
        try:
            with open(file_path, "r") as file:
                data = json.load(file)
                if self.logger:
                    self.logger.log_info(f"Successfully loaded JSON file: {file_path}")
                return data
        except FileNotFoundError:
            if self.logger:
                self.logger.log_warning(f"File not found: {file_path}")
            return None
        except json.JSONDecodeError as e:
            if self.logger:
                self.logger.log_error(f"Error decoding JSON file: {file_path}. Exception: {e}")
            raise

    def save_json_file(self, file_path, data, overwrite=True):
        """Save data to a JSON file."""
        try:
            if not overwrite and os.path.exists(file_path):
                if self.logger:
                    self.logger.log_warning(f"File already exists: {file_path}. Skipping save.")
                return

            with open(file_path, "w") as file:
                json.dump(data, file, indent=4)

            if self.logger:
                self.logger.log_info(f"Saved data to file: {file_path}")
        except Exception as e:
            if self.logger:
                self.logger.log_error(f"Failed to save data to file: {file_path}. Exception: {e}")
            raise

    def delete_file(self, file_path):
        """Delete a file if it exists."""
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                if self.logger:
                    self.logger.log_info(f"Deleted file: {file_path}")
            else:
                if self.logger:
                    self.logger.log_warning(f"File not found for deletion: {file_path}")
        except Exception as e:
            if self.logger:
                self.logger.log_error(f"Failed to delete file: {file_path}. Exception: {e}")
            raise

    def generate_report(self, portfolio_path, output_file="data/portfolio/reports/portfolio_report.txt"):
        """
        Generate and save a portfolio report.
        :param portfolio_path: Path to the portfolio JSON file.
        :param output_file: Path to save the report.
        """
        try:
            # Ensure portfolio JSON file exists
            if not os.path.exists(portfolio_path):
                self.logger.log_warning(f"No portfolio file found at '{portfolio_path}'. Cannot generate report.")
                return

            # Load portfolio data
            portfolio_data = self.load_json_file(portfolio_path)
            if not isinstance(portfolio_data, dict):
                self.logger.log_error(f"Invalid portfolio data format in {portfolio_path}.")
                return

            # Generate report content
            report_content = []
            for user_email, stocks in portfolio_data.items():
                report_content.append(f"Portfolio Report for: {user_email}")
                report_content.append("=" * 50)

                for stock in stocks:
                    ticker = stock.get("ticker")
                    shares = stock.get("shares", 0)
                    purchase_price = stock.get("purchase_price", 0.0)

                    stock_data = yf.Ticker(ticker)
                    current_price = stock_data.info.get("regularMarketPrice", 0)
                    dividend_yield = (stock_data.info.get("dividendYield", 0) or 0) * 100

                    stock_return = (current_price - purchase_price) * shares
                    dividend_income = (dividend_yield / 100) * current_price * shares

                    report_content.append(
                        f"Ticker: {ticker}\n"
                        f"  Shares: {shares}\n"
                        f"  Purchase Price: ${purchase_price:.2f}\n"
                        f"  Current Price: ${current_price:.2f}\n"
                        f"  Total Return: ${stock_return:.2f}\n"
                        f"  Dividend Yield: {dividend_yield:.2f}%\n"
                        f"  Dividend Income: ${dividend_income:.2f}\n"
                    )
                report_content.append("\n")

            # Write report to output file
            self.ensure_directory_exists(output_file)
            with open(output_file, "w") as output:
                output.write("\n".join(report_content))

            self.logger.log_info(f"Portfolio report generated and saved to '{output_file}'.")

        except Exception as e:
            self.logger.log_error(f"Error generating portfolio report: {e}")
            raise