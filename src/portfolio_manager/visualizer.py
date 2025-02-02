import matplotlib.pyplot as plt
import pandas as pd
import mplfinance as mpf
from handlers.userInteractionHandlers import UserInteractionHandler
from file_manager.fileManager import FileManager
import os
import sys


class Visualizer:
    """Class for visualizing stock data."""

    def __init__(self, base_dir: str, save_dir: str = "data/plots/"):
        """
        Initialize the Visualizer with a save directory for plots.

        Args:
            save_dir (str): Directory to save plot files.
        """
        self.save_dir = save_dir
        self.file_manager = FileManager(base_dir=base_dir)
        self.file_manager.ensure_directory_exists(self.save_dir)

    def _save_plot(self, save_path: str) -> str:
        """
        Save the plot to the specified path.

        Args:
            save_path (str): File name for saving the plot.

        Returns:
            str: Full path to the saved plot.
        """
        full_path = os.path.join(self.save_dir, save_path)
        full_path = os.path.abspath(full_path)  # Ensure it's the absolute path
        plt.savefig(full_path)
        print(f"Plot saved at: {full_path}")
        return full_path

    def plot_stock_data(
        self,
        data: pd.DataFrame,
        moving_avg: pd.Series = None,
        volatility: pd.Series = None,
        title: str = "Stock Price Analysis",
        save_name: str = None,
        show_grid: bool = True,
        figure_size: tuple = (14, 7),
    ) -> None:
        """Plot stock prices with optional moving average and volatility."""
        if data.empty or 'Date' not in data.columns or 'Close' not in data.columns:
            raise ValueError("Data must be non-empty and contain 'Date' and 'Close' columns.")

        plt.figure(figsize=figure_size)
        plt.plot(data['Date'], data['Close'], label="Close Price", color='blue', alpha=0.6)

        if moving_avg is not None:
            plt.plot(data['Date'], moving_avg, label="Moving Average", color='orange', alpha=0.8)

        if volatility is not None:
            plt.plot(data['Date'], volatility, label="Volatility", color='red', linestyle='--', alpha=0.8)

        plt.title(title)
        plt.xlabel("Date")
        plt.ylabel("Price")
        plt.legend()
        if show_grid:
            plt.grid()

        if save_name:
            self._save_plot(save_name)
        plt.show()

    def plot_volume(self, data: pd.DataFrame, save_name: str = None) -> None:
        """Plot the stock volume over time."""
        if data.empty or 'Date' not in data.columns or 'Volume' not in data.columns:
            raise ValueError("Data must be non-empty and contain 'Date' and 'Volume' columns.")

        plt.figure(figsize=(14, 7))
        plt.bar(data['Date'], data['Volume'], color='green', alpha=0.6)
        plt.title("Stock Volume Over Time")
        plt.xlabel("Date")
        plt.ylabel("Volume")
        plt.grid(True)

        if save_name:
            self._save_plot(save_name)
        plt.show()

    def plot_candlestick(self, data: pd.DataFrame, save_name: str = None) -> None:
        """Plot a candlestick chart for stock data."""
        if data.empty or not {'Date', 'Open', 'High', 'Low', 'Close'}.issubset(data.columns):
            raise ValueError("Data must be non-empty and contain 'Date', 'Open', 'High', 'Low', 'Close' columns.")

        data = data.copy()
        data['Date'] = pd.to_datetime(data['Date'])
        data.set_index('Date', inplace=True)

        # Use mplfinance to plot
        save_path = os.path.join(self.save_dir, save_name) if save_name else None
        save_path = os.path.abspath(save_path)  # Ensure it's the absolute path
        mpf.plot(
            data,
            type='candle',
            style='charles',
            title="Candlestick Chart",
            ylabel="Price",
            volume=True,
            savefig=save_path,
            figsize=(14, 7),
        )
        if save_name:
            print(f"Candlestick chart saved at: {save_path}")

    def visualize_choice(self, data: pd.DataFrame):
        """Prompt user to choose the type of plot to visualize."""
        while True:
            print("\nWhat would you like to plot?")
            print("1. Stock Price (with Moving Average & Volatility)")
            print("2. Stock Volume")
            print("3. Candlestick Chart")
            print("4. Exit")

            try:
                choice = int(UserInteractionHandler.get_user_input("Enter your choice (1/2/3/4): "))
                if choice == 1:
                    moving_avg = data['Close'].rolling(window=50).mean()
                    self.plot_stock_data(data, moving_avg=moving_avg, save_name="stock_price_analysis.png")
                elif choice == 2:
                    self.plot_volume(data, save_name="stock_volume.png")
                elif choice == 3:
                    self.plot_candlestick(data, save_name="candlestick_chart.png")
                elif choice == 4:
                    print("Exiting the visualizer.")
                    break
                else:
                    print("Invalid choice. Please try again.")
            except ValueError:
                print("Invalid input. Please enter a number between 1 and 4.")

    def run_visualizer(self, data: pd.DataFrame):
        """Start the visualizer by showing the available options."""
        if data.empty:
            raise ValueError("Data cannot be empty for visualization.")
        self.visualize_choice(data)
