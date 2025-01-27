import os
import sys
from datetime import datetime, timedelta
import pickle
from typing import Union
import pandas as pd

# Add the `src` directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))
from file_manager.fileManager import FileManager
from logs.logger import Logger

class CacheData:
    """Handles cached stock data retrieval."""

    CACHE_EXPIRATION_TIME = timedelta(hours=24)  # Cache expiration time (24 hours by default)

    def __init__(self, ticker: str, start_date: str, end_date: str, cache_dir: str = "data/sys_file/cache_dir"):
        self.ticker = ticker
        self.start_date = start_date
        self.end_date = end_date
        self.cache_dir = cache_dir
        self.file_manager = FileManager()
        self.logger = Logger("CacheData")

        # Ensure the cache directory exists
        self.ensure_directories_exist()

    def ensure_directories_exist(self):
        """Ensure the cache directory exists. Create it if necessary."""
        try:
            self.file_manager.ensure_directory_exists(self.cache_dir)
            self.logger.log_info(f"Cache directory ensured: {self.cache_dir}")
        except Exception as e:
            self.logger.log_error(f"Error ensuring cache directory exists: {e}")

    def _get_cache_filename(self) -> str:
        """Generate a unique cache filename based on the ticker and dates."""
        filename = f"{self.ticker}_{self.start_date}_{self.end_date}.pkl"
        return os.path.join(self.cache_dir, filename)

    def _load_cache(self) -> Union[pd.DataFrame, None]:
        """Load cached data from the file, considering expiration time."""
        cache_filename = self._get_cache_filename()
        if self.file_manager.read_file(cache_filename):
            try:
                with open(cache_filename, "rb") as f:
                    cache_data = pickle.load(f)
                    cache_timestamp = cache_data.get('timestamp')
                    if cache_timestamp and datetime.now() - cache_timestamp < self.CACHE_EXPIRATION_TIME:
                        self.logger.log_info(f"Cache hit for {cache_filename}. Data is valid.")
                        return cache_data['data']
                    else:
                        self.logger.log_info(f"Cache expired for {cache_filename}. Fetching new data.")
                        self.file_manager.delete_file(cache_filename)  # Remove expired cache
            except (pickle.UnpicklingError, EOFError) as pickling_error:
                self.logger.log_error(f"Error loading cache file {cache_filename}: {pickling_error}")
            except Exception as e:
                self.logger.log_error(f"Unexpected error loading cache: {e}")
        return None

    def _save_cache(self, data: pd.DataFrame) -> None:
        """Save data to cache with a timestamp."""
        cache_filename = self._get_cache_filename()
        cache_data = {
            'data': data,
            'timestamp': datetime.now()
        }
        try:
            with open(cache_filename, "wb") as f:
                pickle.dump(cache_data, f)
            self.logger.log_info(f"Data cached for {cache_filename}.")
        except Exception as e:
            self.logger.log_error(f"Error saving cache file {cache_filename}: {e}")