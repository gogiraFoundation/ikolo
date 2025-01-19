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
            self.ensure_directory_exists(file_path)

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