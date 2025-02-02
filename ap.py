from flask import Flask, request, jsonify, render_template
import sys
import os
import traceback
import json

# Add the `src` directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "src")))

from logs.logger import Logger
from portfolioManagerApp import PortfolioManagerApp
from controllers import ControllerClass

# Initialize Flask app, logger, and controller
app = Flask(__name__)
logger = Logger("FlaskPortfolioApp")
controller = ControllerClass()

# Helper function for centralized error handling
def handle_error(func):
    """Decorator for error handling."""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.log_error(f"Error: {traceback.format_exc()}")
            print(traceback.format_exc())
            if request.path.startswith("/api") or request.is_json:  # Ensure API routes return JSON
                return jsonify({"status": "error", "message": str(e)}), 500
            else:
                return render_template("error.html", message=str(e)), 500
    wrapper.__name__ = func.__name__  # Preserve the original function name
    return wrapper

# ---------- API Routes ----------

@app.route("/perform_analysis", methods=["POST"])
@handle_error
def perform_analysis():
    """API endpoint for stock analysis."""
    data = request.get_json()
    
    if not data:
        return jsonify({"status": "error", "message": "Invalid JSON payload."}), 400

    ticker = data.get("ticker")
    start_date = data.get("start_date")
    end_date = data.get("end_date")

    if not all([ticker, start_date, end_date]):
        return jsonify({"status": "error", "message": "Missing required fields: ticker, start_date, end_date"}), 400

    analysis_data, status_code = controller.perform_stock_analysis(ticker, start_date, end_date)
    
    if status_code != 200:
        return jsonify({"status": "error", "message": "Failed to analyze stock."}), status_code
    
    return jsonify(analysis_data), 200


@app.route("/track_stock", methods=["POST"])
@handle_error
def track_stock():
    """API endpoint for tracking stocks."""
    data = request.get_json()
    ticker, threshold = data.get("ticker"), data.get("threshold")
    
    if not all([ticker, threshold]):
        return jsonify({"status": "error", "message": "Missing required fields."}), 400

    tracking_data, status_code = controller.track_stock(ticker, float(threshold))
    return jsonify(tracking_data), status_code

@app.route("/search_stocks", methods=["POST"])
@handle_error
def search_stocks():
    """API endpoint for searching stocks."""
    data = request.get_json()
    tickers = data.get("tickers", [])
    
    if not tickers:
        return jsonify({"status": "error", "message": "No tickers provided."}), 400

    search_results, status_code = controller.search_stocks(tickers)
    return jsonify(search_results), status_code

@app.route("/portfolio_operations", methods=["POST"])
@handle_error
def portfolio_operations():
    """API endpoint for portfolio operations."""
    return jsonify(controller.portfolio_operations())

# ---------- Web Interface Routes ----------

@app.route("/")
def home():
    """Render the home page."""
    return render_template("home.html", title="Portfolio Manager")

@app.route("/analyze_stock", methods=["GET", "POST"])
@handle_error
def analyze_stock_form():
    """Web interface for stock analysis."""
    try:
        if request.method == "GET":
            return render_template("stocks_analysis_form.html", title="Analyze Stock")
        
        ticker, start_date, end_date = request.form.get("ticker"), request.form.get("start_date"), request.form.get("end_date")
        
        if not all([ticker, start_date, end_date]):
            return jsonify({"status": "error", "message": "Missing required fields."}), 400
        
        
        analysis_data, status_code = controller.perform_stock_analysis(ticker, start_date, end_date)
        print(json.dumps(analysis_data, indent=4))
        if status_code != 200:
            return jsonify({"status": "error", "message": "Error Analyzing Stock"}),
        
        return render_template("analysis_result.html", data=analysis_data)
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

        
@app.route("/track_stock", methods=["GET", "POST"])
@handle_error
def track_stock_form():
    """Web interface for tracking stocks."""
    if request.method == "GET":
        return render_template("stock_tracking_form.html", title="Track Stocks")
    
    ticker, threshold = request.form.get("trackingTicker"), request.form.get("threshold")
    
    if not all([ticker, threshold]):
       return jsonify({"status": "error", "message": "Missing required fields."}), 400
    
    tracking_data, status_code = controller.track_stock(ticker, float(threshold))
    
    if status_code != 200:
        return render_template("error.html", message=tracking_data.get("message", "Error tracking stock."))
    
    return render_template("tracking_results.html", data=tracking_data)

@app.route("/search_stock", methods=["GET", "POST"])
@handle_error
def search_stock_form():
    """Web interface for searching stocks."""
    if request.method == "GET":
        return render_template("stock_search_form.html", title="Search Stocks")
    
    tickers = [ticker.strip() for ticker in request.form.get("searchTickers", "").split(",") if ticker.strip()]
    
    if not tickers:
        return render_template("error.html", message="No tickers provided.")
    
    search_results, status_code = controller.search_stocks(tickers)
    
    if status_code != 200:
        return render_template("error.html", message=search_results.get("message", "Error searching stocks."))
    
    return render_template("search_results.html", data=search_results)

@app.route("/portfolio_operations", methods=["GET"])
def portfolio_operations_page():
    """Render the portfolio operations page."""
    return render_template("portfolio.html", title="Portfolio Operations")

# ---------- Main Application Entry ----------

if __name__ == "__main__":
    app.run(debug=True)