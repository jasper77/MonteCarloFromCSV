#!/usr/bin/env python3
from read_config import read_config
from csv_importer import read_data_file
import argparse
import pandas as pd
from monte_carlo_forecasting import simulate_completion

def monte_carlo_by_dates(settings):
    # Accessing settings
    data_file = settings['source_data']['data_file']

    projection_item_count = settings['Projections']['future_event_count']
    projection_percentile = settings['Projections']['percentile']
    projection_simulations = settings['Projections']['simulations']

    #log_file = settings['Logging']['log_file']

    print(f"Reading from {data_file}")

    print(f"Projecting {projection_item_count} items for {projection_percentile} percentile")
    print(f"Using {projection_simulations} simulations")
    #sprint(f"Logging to {log_file}")

    # Read the data from the csv file
    data_content = read_data_file(data_file)

    # Perform the monte carlo simulation.
    percentiles =  simulate_completion(data_content, projection_item_count, projection_simulations)

    print("Monte Carlo Simulation Results:")
    for percentile, date in percentiles.items():
        print(f"{percentile}: {pd.to_datetime(date).date()}")

    #print(f"50th Percentile: {percentiles['50th_percentile'].date()}")
    #print(f"85th Percentile: {percentiles['85th_percentile'].date()}")
    #print(f"95th Percentile: {percentiles['95th_percentile'].date()}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process a configuration file.")
    parser.add_argument("config_file", type=str, help="The path to the configuration file.")
    args = parser.parse_args()

    config_file = args.config_file
    settings = read_config(config_file)
    monte_carlo_by_dates(settings)

