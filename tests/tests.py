import pandas as pd
from src.metrics_calculator import MetricsCalculator


def test_calculate_moving_average():
    data = pd.DataFrame({"Close": [10, 20, 30, 40, 50]})
    result = MetricsCalculator.calculate_moving_average(data, window=3)
    expected = pd.Series([None, None, 20.0, 30.0, 40.0])
    pd.testing.assert_series_equal(result, expected, check_exact=False)
