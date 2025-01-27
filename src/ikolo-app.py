import sys
import os
import traceback

# Add the `src` directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))

from logs.logger import Logger
from portfolioManagerApp import PortfolioManagerApp



def run():
    """Run the main application."""
    app = PortfolioManagerApp()
    try:
        logger.log_info("Application is running...")
        app.run()
    finally:
        logger.log_info("Application shutdown complete.")

if __name__ == "__main__":
    logger = Logger("IkoloApp")
    try:
        logger.log_info("Starting PortfolioManagerApp...")
        run()
        logger.log_info("PortfolioManagerApp exited successfully.")
    except FileNotFoundError as e:
        logger.log_error(f"Configuration file missing: {e}")
        sys.exit(2)
    except Exception as e:
        error_message = f"An error occurred while running the Portfolio Manager App: {e}"
        logger.log_error(f"{error_message}\n{traceback.format_exc()}")
        print(error_message)
        sys.exit(1)
