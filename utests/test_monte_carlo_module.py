import pytest
from datetime import datetime

import sys
import os

# Add the src directory to the sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

import monte_carlo_forecasting as mcf

# Sample data dictionary with varying numbers of items completed per date
data_dict = {
    '2023-01-01': 1,
    '2023-01-05': 3,  # 3 items completed on this date
    '2023-01-12': 2,
    '2023-01-20': 1,
    '2023-01-28': 4,  # 4 items completed on this date
    '2023-02-02': 1,
    '2023-02-09': 1,
    '2023-02-17': 1,
    '2023-02-24': 1,
    '2023-03-01': 1,
}


def test_simulation_output_keys():
    """Test if simulation output contains the required keys."""
    forecast_items = 5
    num_simulations = 100
    results = mcf.simulate_completion(data_dict, forecast_items, num_simulations)

    # Check if output has all required keys
    assert '50th Percentile (Median)' in results
    assert '85th Percentile' in results
    assert '95th Percentile' in results


def test_simulation_output_types():
    """Test if simulation outputs dates as expected for percentiles."""
    forecast_items = 5
    num_simulations = 100
    results = mcf.simulate_completion(data_dict, forecast_items, num_simulations)

    # Check if values are of datetime type
    assert isinstance(results['50th Percentile (Median)'], datetime)
    assert isinstance(results['85th Percentile'], datetime)
    assert isinstance(results['95th Percentile'], datetime)


def test_increasing_percentiles():
    """Test that the percentiles are in the correct order (50th <= 85th <= 95th)."""
    forecast_items = 5
    num_simulations = 1000  # Use a larger number for accuracy
    results = mcf.simulate_completion(data_dict, forecast_items, num_simulations)

    assert results['50th Percentile (Median)'] <= results['85th Percentile']
    assert results['85th Percentile'] <= results['95th Percentile']


def test_forecast_more_items_than_data():
    """Test forecasting when the forecast items are more than historical data total items."""
    forecast_items = 15  # Forecast more items than present in historical data
    num_simulations = 500
    results = mcf.simulate_completion(data_dict, forecast_items, num_simulations)

    # Check if the simulation returns valid dates without error
    assert '50th Percentile (Median)' in results
    assert '85th Percentile' in results
    assert '95th Percentile' in results

def test_zero_forecast_items():
    """Test behavior when forecast items is zero."""
    forecast_items = 0
    num_simulations = 100
    results = mcf.simulate_completion(data_dict, forecast_items, num_simulations)

    # If no items are forecasted, the result should be the last date in the data set
    last_date = max(datetime.strptime(date, '%Y-%m-%d') for date in data_dict.keys())
    assert results['50th Percentile (Median)'] == last_date
    assert results['85th Percentile'] == last_date
    assert results['95th Percentile'] == last_date


def test_large_simulation_count():
    """Test handling of a large number of simulations."""
    forecast_items = 5
    num_simulations = 10000  # Large number of simulations for stability check
    results = mcf.simulate_completion(data_dict, forecast_items, num_simulations)

    # Check if output is produced correctly under high simulation load
    assert '50th Percentile (Median)' in results
    assert '85th Percentile' in results
    assert '95th Percentile' in results

data_dict1 = {
    '2023-01-01': 0,  # Start of project; no items completed on this date
    '2023-01-05': 3,  # 3 items completed on this date
    '2023-01-12': 2,
    '2023-01-20': 1,
    '2023-01-28': 4,  # 4 items completed on this date
    '2023-02-02': 1,
    '2023-02-09': 1,
    '2023-02-17': 1,
    '2023-02-24': 1,
    '2023-03-01': 1,
}

import pandas as pd
def test_ignore_zero_items_to_start():
    forecast_items = 5
    num_simulations = 10000  # Large number of simulations for stability check

    # Expected dates when using data_dict
    expected_dates = {
        '50th Percentile (Median)': datetime(2023, 3, 23),
        '85th Percentile': datetime(2023, 4, 1),
        '95th Percentile': datetime(2023, 4, 5),
    }

    results = mcf.simulate_completion(data_dict, forecast_items, num_simulations)

    assert results['50th Percentile (Median)'].to_pydatetime() == expected_dates['50th Percentile (Median)']
    assert results['85th Percentile'].to_pydatetime() == expected_dates['85th Percentile']
    assert results['95th Percentile'].to_pydatetime() == expected_dates['95th Percentile']

    # Expected dates when using data_dict1
    expected_dates = {
        '50th Percentile (Median)': datetime(2023, 3, 23),
        '85th Percentile': datetime(2023, 4, 1),
        '95th Percentile': datetime(2023, 4, 5),
    }

    results1 = mcf.simulate_completion(data_dict1, forecast_items, num_simulations)

    assert results['50th Percentile (Median)'].to_pydatetime() == expected_dates['50th Percentile (Median)']
    assert results['85th Percentile'].to_pydatetime() == expected_dates['85th Percentile']
    assert results['95th Percentile'].to_pydatetime() == expected_dates['95th Percentile']
