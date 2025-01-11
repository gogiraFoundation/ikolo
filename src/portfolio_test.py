import unittest
from unittest.mock import patch, MagicMock
from portfolio_manager.visualizer import Visualizer
from portfolio_manager.metrics_calculator import MetricsCalculator
from portfolio_manager.data_fetcher import DataFetcher
from main import main

class TestPortfolioManager(unittest.TestCase):

    @patch('builtins.input', side_effect=['AAPL', '2023-01-01', '2023-12-31', '30', '15'])
    @patch('portfolio_manager.data_fetcher.DataFetcher.fetch_stock_data')
    @patch('portfolio_manager.metrics_calculator.MetricsCalculator.calculate_moving_average')
    @patch('portfolio_manager.metrics_calculator.MetricsCalculator.calculate_volatility')
    @patch('portfolio_manager.visualizer.Visualizer.plot_stock_data')
    def test_main_success(self, mock_plot, mock_volatility, mock_moving_avg, mock_fetch_data, mock_input):
        # Mocking return values
        mock_fetch_data.return_value = {'data': 'mock_data'}
        mock_moving_avg.return_value = [10, 20, 30]
        mock_volatility.return_value = [0.1, 0.2, 0.3]

        main()

        # Assertions
        mock_fetch_data.assert_called_once_with('AAPL', '2023-01-01', '2023-12-31')
        mock_moving_avg.assert_called_once_with({'data': 'mock_data'}, 30)
        mock_volatility.assert_called_once_with({'data': 'mock_data'}, 15)
        mock_plot.assert_called_once_with({'data': 'mock_data'}, [10, 20, 30], [0.1, 0.2, 0.3])

    @patch('builtins.input', side_effect=['AAPL', 'invalid_date', '2023-12-31', '30', '15'])
    @patch('portfolio_manager.data_fetcher.DataFetcher.fetch_stock_data', side_effect=ValueError("Invalid date format"))
    def test_main_fetch_data_error(self, mock_fetch_data, mock_input):
        with patch('builtins.print') as mock_print:
            main()
            mock_print.assert_any_call("Error fetching data: Invalid date format")

    @patch('builtins.input', side_effect=['AAPL', '2023-01-01', '2023-12-31', '30', '15'])
    @patch('portfolio_manager.data_fetcher.DataFetcher.fetch_stock_data', return_value={'data': 'mock_data'})
    @patch('portfolio_manager.metrics_calculator.MetricsCalculator.calculate_moving_average', side_effect=Exception("Calculation error"))
    def test_main_calculate_metrics_error(self, mock_moving_avg, mock_fetch_data, mock_input):
        with patch('builtins.print') as mock_print:
            main()
            mock_print.assert_any_call("Error calculating metrics: Calculation error")

    @patch('builtins.input', side_effect=['AAPL', '2023-01-01', '2023-12-31', '30', '15'])
    @patch('portfolio_manager.data_fetcher.DataFetcher.fetch_stock_data', return_value={'data': 'mock_data'})
    @patch('portfolio_manager.metrics_calculator.MetricsCalculator.calculate_moving_average', return_value=[10, 20, 30])
    @patch('portfolio_manager.metrics_calculator.MetricsCalculator.calculate_volatility', return_value=[0.1, 0.2, 0.3])
    @patch('portfolio_manager.visualizer.Visualizer.plot_stock_data', side_effect=Exception("Visualization error"))
    def test_main_visualization_error(self, mock_plot, mock_volatility, mock_moving_avg, mock_fetch_data, mock_input):
        with patch('builtins.print') as mock_print:
            main()
            mock_print.assert_any_call("Error visualizing data: Visualization error")

    @patch('builtins.input', side_effect=['AAPL', '2023-01-01', '2023-12-31', '30', '-10'])
    @patch('portfolio_manager.data_fetcher.DataFetcher.fetch_stock_data', return_value={'data': 'mock_data'})
    def test_main_invalid_volatility_window(self, mock_fetch_data, mock_input):
        with patch('builtins.print') as mock_print:
            main()
            mock_print.assert_any_call("Error calculating metrics: Invalid volatility window")

    @patch('builtins.input', side_effect=['AAPL', '2023-01-01', '2023-12-31', '0', '15'])
    @patch('portfolio_manager.data_fetcher.DataFetcher.fetch_stock_data', return_value={'data': 'mock_data'})
    def test_main_invalid_moving_average_window(self, mock_fetch_data, mock_input):
        with patch('builtins.print') as mock_print:
            main()
            mock_print.assert_any_call("Error calculating metrics: Invalid moving average window")

    @patch('builtins.input', side_effect=['AAPL', '2023-01-01', '2023-12-31', '30', '15'])
    @patch('portfolio_manager.data_fetcher.DataFetcher.fetch_stock_data', return_value={'data': 'mock_data'})
    def test_main_empty_data(self, mock_fetch_data, mock_input):
        mock_fetch_data.return_value = {}
        with patch('builtins.print') as mock_print:
            main()
            mock_print.assert_any_call("Error fetching data: No data returned")

if __name__ == '__main__':
    unittest.main()
