from portfolioManagerApp import PortfolioManagerApp
import sys
import os

# Add the `src` directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))





if __name__ == "__main__":
    app = PortfolioManagerApp()
    app.run()