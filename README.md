# Monte Carlo from CSV input

This is a set of scripts that will run a Monte Carlo simulation from the contents of a CSV file, from the command line. If you're 
used to following Scrum with sprints and you'd like to explore the continuous flow of Kanban, and would like to know how well a Monte
Carlo simulation can answer the question "When might this number of items be done?" based on your own historical data, you can use this.

I was working in a company dedicated to Scrum for software project work and using story points to forecast how long a project might take to 
complete. I'd heard about companies finding that Kanban worked better for them, and they don't use story points; instead they make sure
all tasks are broken down small enough (akin to "If it's bigger than an 8, break it down or make it smaller", a common practice among
teams that follow scrum) and then use Monte Carlo to answer the question "How long will the set of items for this project take to
complete?" I wanted to explore how to use Monte Carlo using my own data, not a Jira plugin. This tool accomplishes that goal. 

A nice thing about Monte Carlo is that it can be used on any type of work breakdown, which means it can solve a problem for software
companies; there is often value in getting a loose idea of how long a project might take prior to investing in a thorough technical 
breakdown. When projects can be broken down by epics or mini-milestones that are all "no bigger than a breadbox" consistently, and
the breakdown does not need a thorough technical analysis, then Monte Carlo can be used to get that idea when applied to that level
of breakdown. 

Example: If you're used to using epics, and you can say on which dates past epics were completed, and you know how many epics your
upcoming project will contain, you can create a CSV file containing the dates when past epics were completed and a count of completed epics
for each date in the CSV (i.e. On date YYYY-MM-DD, 2 epics were completed). If you have a record of completions for individual tasks, 
and you have a task breakdown for the future work, use that. If you have historical data from before a recently completed project and 
you want to see how accurately an MC forecast would have been for your just-finishe project, you can create a CSV file with the 
historical data from before this project, and ask this tool to forecast how long it would take to complete the tasks you knew about at 
the start of the project.

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
