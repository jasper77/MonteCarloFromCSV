# Monte Carlo from CSV input

This is a set of scripts that will run a Monte Carlo simulation from the contents of a CSV file, from the command line.

## 1) Setting up to run the scripts

If you already have python3 and virtual environments set up, skip to installing the dependencies.

### 1.1) Set up your environment. Specifics will depend on your operating system. 
- Install Python3
  For a mac: https://docs.python-guide.org/starting/install3/osx/

### 1.2) To isolate python dependences, use a virtual environment. Set one up with pip:
  https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/
```
$ pip install virtualenv
$ virtualenv --version
```

### 1.3) Enter the virtual environment
[In the project folder]
```
$ python3 -m venv .venv
$ source .venv/bin/activate
```

### 1.4) Prepare pip
```
$ python3 -m pip install --upgrade pip
$ python3 -m pip --version
```

### 1.5) Install dependencies:
  For a mac:
`$ python3 -m pip install -r requirements.txt`

### 1.6) Make sure it runs with the sample configuration file and sample data.
`$ python3 MonteCarlo.py config.yaml`


## Section 2) Running a Monte Carlo simulation on your data

### 2.1) Make a CSV with your data
- Make a copy of the included sample CSV file and follow the same format for your own data.
- Dates should be consecutive, starting with the oldest first.

### 2.2) Edit your configuration file
Make a copy of the configuration file or edit the example included. Be sure it references your own CSV file.

### 2.3) Get your simulations; run the scripts
 - From the top level directory, you can use the included bash script to either run the simulation, or as
   a usage example.
`$ cd src`
`$ python3 MonteCarlo.py <config_file>`

## Interpreting the results:
```
Results are sent to stdout. 
Example output:
Monte Carlo Simulation Results:
50th Percentile (Median): 2024-01-21
85th Percentile: 2024-01-23
95th Percentile: 2024-01-23
```

The 50th percentile date means that 50% of the simulations completed by that date. That could be
interpreted as "If everything goes perfectly, low confidence" forecast.

The 85th percentile means 85% of the simulations completed on or before that date. That date has
a higher confidence. 

The 95th percentile represents a high confidence forecast.



## How it works:
This set of scripts reads your csv file containing dates, and the numbers of items completed for each
date in the file, into a pandas dataframe. Dates where zero items were completed are ignored.
The algorithm calculates the elapsed time between the different completion dates, to simulate task
durations. Then, the algorithm randomly samples from the durations for each item to forecast until all
of the items have been forecasted, and repeats that simulation the specified number of times.

Note: As long as tasks are started and complete at a consistent rate, it doesn't matter that 
actual task durations may be much longer than the space between completed items in the data.
