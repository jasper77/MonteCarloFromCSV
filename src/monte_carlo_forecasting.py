import numpy as np
import pandas as pd
from datetime import timedelta
import random


def simulate_completion(data_dict, forecast_items, num_simulations):
    """
    Perform a Monte Carlo simulation to forecast task completion time when multiple items
    can be completed on the same date.
    Allows for the number of forecasted items to be greater than the number of historically completed items.

    Args:
        data_dict (dict): A dictionary where keys are dates (as 'YYYY-MM-DD' strings) and values are event counts.
        forecast_items (int): Number of items to forecast.
        num_simulations (int): Number of Monte Carlo simulations to run.

    Returns:
        dict: A dictionary with simulated completion dates for the 50th, 85th, and 95th percentiles.
    """
    # Step 1: Convert data_dict to a Pandas DataFrame
    df = pd.DataFrame(list(data_dict.items()), columns=['Date', 'Events'])
    df['Date'] = pd.to_datetime(df['Date'])

    # Step 2: Calculate the time differences (durations) between consecutive dates
    df = df.sort_values('Date')
    df['Duration'] = df['Date'].diff().dt.days
    df = df.dropna(subset=['Duration'])

    # Step 3: Extract task durations and item counts
    durations = df['Duration'].tolist()
    events = df['Events'].tolist()

    # Step 4: Run Monte Carlo simulations
    simulation_results = []
    last_known_date = df['Date'].max()

    for _ in range(num_simulations):
        total_items = 0
        simulated_date = last_known_date

        while total_items < forecast_items:
            # Randomly sample a duration from the historical data
            duration = random.choice(durations)
            event_count_for_duration = random.choice(events)

            simulated_date += timedelta(days=duration)
            total_items += event_count_for_duration  # Add the number of items completed in that duration

        # Append the simulated date for when the last item is completed
        simulation_results.append(simulated_date)

    # Step 5: Calculate the percentiles for the simulated results
    simulation_results = np.array(simulation_results)

    results = {
        '50th Percentile (Median)': np.percentile(simulation_results, 50),
        '85th Percentile': np.percentile(simulation_results, 85),
        '95th Percentile': np.percentile(simulation_results, 95),
    }

    return results


if __name__ == "__main__":
    # Example usage:
    # Historical data dictionary: {Date: Event count}
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

    # Forecast the completion of 5 additional items, running 10,000 simulations
    forecast_items = 5
    num_simulations = 10000

    # Run the Monte Carlo simulation
    forecast_results = simulate_completion(data_dict, forecast_items, num_simulations)

    # Output the results
    print("Monte Carlo Simulation Results:")
    for percentile, date in forecast_results.items():
        print(f"{percentile}: {pd.to_datetime(date).date()}")
