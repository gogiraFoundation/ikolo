import yfinance as yf


class FundamentalAnalysis:
    """Class for performing fundamental analysis."""
    
    @staticmethod
    def get_financial_ratios(ticker: str):
        """
        Fetch and display fundamental financial ratios.

        Args:
            ticker (str): Stock ticker symbol.

        Returns:
            dict: Dictionary of financial ratios.
        """
        stock = yf.Ticker(ticker)
        info = stock.info
        
        ratios = {
            "P/E Ratio": info.get("trailingPE"),
            "EPS": info.get("trailingEps"),
            "Market Cap": info.get("marketCap"),
            "Beta": info.get("beta"),
            "Dividend Yield": info.get("dividendYield")
        }
        return ratios
