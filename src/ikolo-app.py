from portfolioManagerApp import PortfolioManagerApp
import sys
import os

# Add the `src` directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))

from logs.logger import Logger

if __name__ == "__main__":
    try:
        logger = Logger('IkoloApp')  # Instantiate the logger
        logger.log_info("Starting PortfolioManagerApp...")  # Log info message before running the app
        
        app = PortfolioManagerApp()
        app.run()  # Assuming run() starts the application logic

    except Exception as e:
        logger.log_error(f"An error occurred while running the Portfolio Manager App: {e}")  # Log the error
        print(f"An error occurred while running the Portfolio Manager App: {e}")