# Given the configuration file passed in, determine whether to run a monte carlo
# simulation with historical data of specific dates when items are completed, and
# create forecasts with dates, or to run a monte carlo simulation based on counts
# of items completed per sprint with a forecast for how many sprints it might take
# to complete a number of items.
import sys
import os
import argparse

# Add the src directory to the sys.path
#sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '.', 'src')))
from src.mc_by_dates import monte_carlo_by_dates
from src.read_config import read_config

from read_config import read_config

def main(settings):

    forecast_sprints = settings['source_data']['use_sprints']
    print(f"Forecast dates")
    monte_carlo_by_dates(settings)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process a configuration file.")
    parser.add_argument("config_file", type=str, help="The path to the configuration file.")
    args = parser.parse_args()
    config_file = args.config_file
    settings = read_config(config_file)
    main(settings)