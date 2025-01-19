import logging
import os
from datetime import datetime
import sys

# Add the `src` directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))
from file_manager.fileManager import FileManager


class Logger:
    """
    A logger class that handles all logs for optimal operation.
    """

    def __init__(self, name: str, log_dir: str = "logs/logs_dir/"):
        """
        Initialize the logger with a specific name and configure logging to console and file.

        Args:
            name (str): The name of the logger, typically the module or class name.
            log_dir (str): The directory where log files will be saved.
        """
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)

        # Ensure the log directory exists
        base_directory = FileManager.ensure_directories_exist(log_dir)

        # Create a log file with a timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        log_file = os.path.join(base_directory, f"{name}_{timestamp}.log")

        # Configure console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        console_handler.setFormatter(console_formatter)

        # Configure file handler
        file_handler = logging.FileHandler(log_file, mode="a")
        file_handler.setLevel(logging.INFO)
        file_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        file_handler.setFormatter(file_formatter)

        # Add handlers to the logger
        self.logger.addHandler(console_handler)
        self.logger.addHandler(file_handler)

    def log_info(self, message: str):
        """
        Log an info message.

        Args:
            message (str): The message to log.
        """
        self.logger.info(message)

    def log_warning(self, message: str):
        """
        Log a warning message.

        Args:
            message (str): The message to log.
        """
        self.logger.warning(message)

    def log_error(self, message: str, exception: Exception = None):
        """
        Log an error message, optionally with an exception.

        Args:
            message (str): The error message to log.
            exception (Exception, optional): The exception to log.
        """
        if exception:
            self.logger.error(f"{message}: {exception}")
        else:
            self.logger.error(message)

    def log_debug(self, message: str):
        """
        Log a debug message.

        Args:
            message (str): The message to log.
        """
        self.logger.debug(message)

    def log_critical(self, message: str, exception=None):
        """
        Log a critical message.

        Args:
            message (str): The message to log.
            exception (Exception, optional): The exception to log.
        """
        self.logger.critical(message)
        if exception:
            print(f"Exception: {exception}")
