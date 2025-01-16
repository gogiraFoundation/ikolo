import yfinance as yf

class FundamentalAnalysis:
    """
    Class for performing fundamental analysis on stocks.

    Methods:
    - get_financial_ratios: Fetch and return key financial ratios for a given stock ticker.
    """

    @staticmethod
    def get_financial_ratios(ticker: str) -> dict:
        """
        Fetch and return fundamental financial ratios for a stock.

        Args:
            ticker (str): Stock ticker symbol.

        Returns:
            dict: Dictionary of financial ratios.
        """
        try:
            # Fetch stock data
            stock = yf.Ticker(ticker)
            info = stock.info

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
            # Handle errors gracefully
            return {"Error": f"Unable to fetch financial ratios for {ticker}. Reason: {str(e)}"}