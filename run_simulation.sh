#!/bin/bash

# This is a simple helper script to demonstrate how to get a forecast.
# This assumes your config file is located in this directory, and is
# named config.yaml.

cd src
python3 mc_by_dates.py ../config.yaml

