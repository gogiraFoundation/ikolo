from flask import Flask, request, jsonify
import sys
import os
import traceback
import json
from pathlib import Path

# Add the `src` directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "src")))

from portfolioManagerApp import PortfolioManagerApp
from logs.logger import Logger


class ControllerClass:
    """
    Controller for handling API calls and interactions with the PortfolioManagerApp.
    """

    def __init__(self, base_dir=None):
        self.logger = Logger("Controller")
        self.base_dir = Path(base_dir or ".").resolve()
        self.portfolio_manager = PortfolioManagerApp(base_dir=self.base_dir)

    def perform_stock_analysis(self, ticker, start_date, end_date):
        try:
            result = self.portfolio_manager.perform_analysis(ticker, start_date, end_date)
            
            if not result:
                self.logger.log_error(f"Analysis returned empty for {ticker}.")
                return {
                    "status": "error",
                    "message": f"No analysis data available for {ticker}.",
                    "data": None
                }, 500
            
            self.logger.log_info(f"Stock analysis for {ticker} completed: {result}")  # Log what is being returned

            return {
                "status": "success",
                "message": f"Stock analysis for {ticker} completed successfully.",
                "data": result  # Ensure this is correctly structured
            }, 200
        except Exception as e:
            return self.handle_error("perform_stock_analysis", e)


    def track_stock(self, ticker, threshold):
        """
        Handle stock tracking request.

        Args:
            ticker (str): Stock ticker symbol.
            threshold (float): Alert threshold.

        Returns:
            tuple: JSON response and HTTP status code.
        """
        try:
            self.portfolio_manager.track_stocks(ticker, threshold)
            return {
                "status": "success",
                "message": f"Tracking {ticker} with a threshold of {threshold}.",
            }, 200
        except Exception as e:
            return self.handle_error("track_stock", e)

    def search_stocks(self, tickers):
        """
        Handle stock search request.

        Args:
            tickers (list): List of stock ticker symbols.

        Returns:
            tuple: JSON response and HTTP status code.
        """
        try:
            stock_metadata = self.portfolio_manager.search_stocks(tickers)
            return {
                "status": "success",
                "message": "Stock metadata retrieved successfully.",
                "data": stock_metadata,
            }, 200
        except Exception as e:
            return self.handle_error("search_stocks", e)

    def portfolio_operations(self):
        """
        Handle portfolio operations request.

        Returns:
            tuple: JSON response and HTTP status code.
        """
        try:
            result = self.portfolio_manager.portfolio_actions()
            return {
                "status": "success",
                "message": "Portfolio operations completed successfully.",
                "data": result
            }, 200
        except Exception as e:
            return self.handle_error("portfolio_operations", e)

    def handle_error(self, function_name, exception):
        """
        Centralized error handler for the controller.

        Args:
            function_name (str): Name of the method where the error occurred.
            exception (Exception): Exception instance.

        Returns:
            tuple: JSON error response and HTTP status code.
        """
        error_message = str(exception)
        self.logger.log_error(f"Error in {function_name}: {error_message}")
        return {
            "status": "error",
            "message": f"Error in {function_name}: {error_message}",
            "trace": traceback.format_exc(),
        }, 400