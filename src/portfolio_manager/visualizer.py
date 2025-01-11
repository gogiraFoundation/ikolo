import matplotlib.pyplot as plt
import pandas as pd



class Visualizer:
    """Class for visualizing stock data."""
    
    @staticmethod
    def plot_stock_data(data: pd.DataFrame, moving_avg: pd.Series = None, volatility: pd.Series = None) -> None:
        """
        Plot stock prices with optional moving average and volatility.

        Args:
            data (pd.DataFrame): Stock price data with 'Date' and 'Close' columns.
            moving_avg (pd.Series, optional): Moving average series. Defaults to None.
            volatility (pd.Series, optional): Volatility series. Defaults to None.
        """
        plt.figure(figsize=(14, 7))
        plt.plot(data['Date'], data['Close'], label="Close Price", color='blue', alpha=0.6)
        
        if moving_avg is not None:
            plt.plot(data['Date'], moving_avg, label="Moving Average", color='orange', alpha=0.8)
        
        if volatility is not None:
            plt.plot(data['Date'], volatility, label="Volatility", color='red', linestyle='--', alpha=0.8)
        
        plt.title("Stock Price Analysis")
        plt.xlabel("Date")
        plt.ylabel("Price")
        plt.legend()
        plt.grid()
        plt.show()
