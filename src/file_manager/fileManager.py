import json
import os
import sys
# Add the `src` directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))
from logs.logger import Logger
import json
import os
import sys



class FileManager:
    """Manager actions that have to do with file and directory interactions."""

    def __init__(self, logger=None):
        self.logger = logger or Logger("FileManager")

    def ensure_directory_exists(self, path):
        """Ensure the directory for a given path exists."""
        try:
            os.makedirs(os.path.dirname(path), exist_ok=True)
            if self.logger:
                self.logger.log_info(f"Verified or created directory: {os.path.dirname(path)}")
        except Exception as e:
            if self.logger:
                self.logger.log_critical(f"Failed to create directory for {path}", e)
            raise

    def load_json_file(self, file_path):
        """Load data from a JSON file."""
        try:
            with open(file_path, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            if self.logger:
                self.logger.log_warning(f"File not found: {file_path}")
            return None
        except json.JSONDecodeError as e:
            if self.logger:
                self.logger.log_error(f"Error decoding JSON file: {file_path}", e)
            raise

    def save_json_file(self, file_path, data, check_existence=False):
        """Save data to a JSON file."""
        try:
            self.ensure_directory_exists(file_path)
            if check_existence and os.path.exists(file_path):
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
