import json
import os
import sys

# Add the `src` directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))
from logs.logger import Logger
class FileManager:
    """Manages actions related to file and directory interactions."""

    def __init__(self, logger=None):
        self.logger = logger or Logger("FileManager")

    def ensure_directory_exists(self, path):
        """Ensure the directory for a given path exists."""
        try:
            directory = os.path.dirname(path)
            if directory:
                os.makedirs(directory, exist_ok=True)
            return directory
            if self.logger:
                self.logger.log_info(f"Verified or created directory: {directory}")
        except Exception as e:
            if self.logger:
                self.logger.log_critical(f"Failed to create directory for {path}", e)
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
                self.logger.log_error(f"Error decoding JSON file: {file_path}", e)
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
                self.logger.log_error(f"Failed to save data to file: {file_path}", e)
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
                self.logger.log_error(f"Failed to delete file: {file_path}", e)
            raise

    def list_files_in_directory(self, directory, extension=None):
        """List all files in a directory with an optional filter by extension."""
        try:
            if not os.path.isdir(directory):
                if self.logger:
                    self.logger.log_warning(f"Directory does not exist: {directory}")
                return []

            files = [
                os.path.join(directory, file)
                for file in os.listdir(directory)
                if os.path.isfile(os.path.join(directory, file))
                and (extension is None or file.endswith(extension))
            ]

            if self.logger:
                self.logger.log_info(f"Listed {len(files)} files in directory: {directory}")

            return files
        except Exception as e:
            if self.logger:
                self.logger.log_error(f"Failed to list files in directory: {directory}", e)
            raise

    def read_file(self, file_path):
        """Read the contents of a file as text."""
        try:
            with open(file_path, "r") as file:
                content = file.read()
                if self.logger:
                    self.logger.log_info(f"Successfully read file: {file_path}")
                return content
        except FileNotFoundError:
            if self.logger:
                self.logger.log_warning(f"File not found: {file_path}")
            return None
        except Exception as e:
            if self.logger:
                self.logger.log_error(f"Failed to read file: {file_path}", e)
            raise

    def write_file(self, file_path, content, overwrite=True):
        """Write content to a file."""
        try:
            self.ensure_directory_exists(file_path)

            if not overwrite and os.path.exists(file_path):
                if self.logger:
                    self.logger.log_warning(f"File already exists: {file_path}. Skipping write.")
                return

            with open(file_path, "w") as file:
                file.write(content)

            if self.logger:
                self.logger.log_info(f"Written content to file: {file_path}")
        except Exception as e:
            if self.logger:
                self.logger.log_error(f"Failed to write to file: {file_path}", e)
            raise


    
    
    def generate_report(self, portfolio_path, output_file="data/portfolio/reports/portfolio_report.xlsx"):
        """
        Generate and save a report from a portfolio JSON file.
        :param portfolio_path: Path to the portfolio JSON file.
        :param output_file: Path to save the Excel report.
        """
        try:
            # Ensure the portfolio JSON file exists
            if not os.path.exists(portfolio_path):
                self.logger.log_warning(f"No portfolio file found at '{portfolio_path}'. Cannot generate report.")
                print(f"Warning: No portfolio file found at '{portfolio_path}'. Cannot generate report.")
                return

            # Load portfolio data
            portfolio_data = self.load_json_file(portfolio_path)
            if not portfolio_data:
                raise ValueError("Portfolio data is empty or file not found.")

            # Generate the report content
            report_content = []
            for user_email, stocks in portfolio_data.items():
                report_content.append(f"Portfolio Report for: {user_email}")
                report_content.append("=" * 50)
                for stock in stocks:
                    ticker = stock.get("ticker")
                    shares = stock.get("shares")
                    purchase_price = stock.get("purchase_price")
                    stock_data = yf.Ticker(ticker)

                    # Fetch current price and dividend yield
                    current_price = stock_data.info.get("regularMarketPrice", 0)
                    dividend_yield = stock_data.info.get("dividendYield", 0) * 100 if stock_data.info.get("dividendYield") else 0

                    stock_return = (current_price - purchase_price) * shares
                    dividend_income = (dividend_yield / 100) * current_price * shares

                    report_content.append(
                        f"Ticker: {ticker}\n"
                        f"  Shares: {shares}\n"
                        f"  Purchase Price: ${purchase_price:.2f}\n"
                        f"  Current Price: ${current_price:.2f}\n"
                        f"  Total Return: ${stock_return:.2f}\n"
                        f"  Dividend Income: ${dividend_income:.2f}\n"
                    )
                report_content.append("\n")

            # Write the report to the output file as plain text
            self.ensure_directory_exists(output_file)
            with open(output_file, "w") as output:
                output.write("\n".join(report_content))

            self.logger.log_info(f"Portfolio report generated and saved to '{output_file}'.")
            print(f"Portfolio report generated and saved to '{output_file}'.")

        except Exception as e:
            self.logger.log_error(f"Error generating portfolio report: {e}")
            print(f"Error generating portfolio report: {e}")
            raise