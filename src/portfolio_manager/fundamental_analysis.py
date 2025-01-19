import yfinance as yf
import logging

class FundamentalAnalysis:
    """
    Class for performing fundamental analysis on stocks.
    
    Methods:
    - get_financial_ratios: Fetch and return key financial ratios for a given stock ticker.
    """

    def __init__(self):
        self.logger = logging.getLogger("FundamentalAnalysis")
        logging.basicConfig(level=logging.INFO)

    @staticmethod
    def get_financial_ratios(ticker: str) -> dict:
        """
        Fetch and return fundamental financial ratios for a stock.

        Args:
            ticker (str): Stock ticker symbol.

        Returns:
            dict: Dictionary of financial ratios or error message if unable to fetch.
        """
        try:
            # Fetch stock data
            stock = yf.Ticker(ticker)
            info = stock.info
            
            # Check if 'info' contains valid data
            if not info or "symbol" not in info or info["symbol"] != ticker:
                return {"Error": f"Invalid ticker symbol or data unavailable for {ticker}."}

            # Extract key financial ratios
            ratios = {
                "P/E Ratio (Trailing)": info.get("trailingPE", "N/A"),
                "EPS (Trailing)": info.get("trailingEps", "N/A"),
                "Market Cap": info.get("marketCap", "N/A"),
                "Beta": info.get("beta", "N/A"),
                "Dividend Yield (%)": (
                    round(info.get("dividendYield", 0) * 100, 2)
                    if info.get("dividendYield") is not None
                    else "N/A"
                ),
                "Price-to-Book Ratio (P/B)": info.get("priceToBook", "N/A"),
                "PEG Ratio": info.get("pegRatio", "N/A"),
                "Revenue (TTM)": info.get("totalRevenue", "N/A"),
                "Gross Margin (%)": (
                    round(info.get("grossMargins", 0) * 100, 2)
                    if info.get("grossMargins") is not None
                    else "N/A"
                ),
                "Operating Margin (%)": (
                    round(info.get("operatingMargins", 0) * 100, 2)
                    if info.get("operatingMargins") is not None
                    else "N/A"
                ),
                "Net Profit Margin (%)": (
                    round(info.get("profitMargins", 0) * 100, 2)
                    if info.get("profitMargins") is not None
                    else "N/A"
                ),
            }
            
            return ratios

        except Exception as e:
            logging.error(f"Error while fetching financial ratios for {ticker}: {e}")
            return {"Error": f"Unable to fetch financial ratios for {ticker}. Reason: {str(e)}"}