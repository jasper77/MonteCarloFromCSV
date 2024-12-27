# Monte Carlo from CSV input

## Overview
After years of using Scrum and story points for project forecasting, I wanted a faster and less resource-intensive 
method for early and ongoing forecasts. Inspired by teams using Kanban for projects, I 
built this tool to experiment with my own data without relying on tools like Jira plugins.

This is a command-line utility for running Monte Carlo simulations to forecast project 
timelines. It uses historical data about completed tasks to predict how long it might 
take to finish a given number of items. 

With this utility, you can:
- Generate forecasts for any kind of work breakdown, such as epics, user stories, or
simply tasks.
- Evaluate how Monte Carlo simulations compare to traditional approaches by comparing
results from this tool against your other forecasts.
- Evaluate how accurate a Monte Carlo simulation might have been for a completed project 
by giving it historical data prior to the project, and the number of items completed in
that project.
- Use your own CSV data for flexible, independent analysis.

## What you'll need
1. A CSV file with:
- **Dates** when similar items were completed
- **Counts** of items completed on each date
2. The **number** of items you want to forecast for.

You don't need to track start dates or duration for individual work items - just the 
completion dates and counts.

This utility is not fully polished, but works as intended. I may enhance it further.

## Why use this tool?

Monte Carlo simulations provide a probabilistic answer to “When will it be done?” for 
software projects, offering several advantages over traditional methods like story points:
- **Faster, Meaningful Results**: It's possible to create meaningful forecasts without 
detailed technical breakdowns. Detailed technical breakdowns improve the accuracy of results.
- **Calendar-Based Forecasts**: Outputs projected completion dates with associated 
probabilities (e.g., “85% of simulations predict completion by MM-DD-YYYY”).
- **Works with Simple Data**: Requires only the dates and counts of completed items, not 
task durations or detailed sizes.
- **Accounts for Uncertainty**: Models variability by running thousands of simulations 
based on historical data.

If you’re exploring how Monte Carlo simulations can work with your data and workflow, this 
tool can help you experiment and assess their utility.

## Advantages over story points
Monte Carlo overcome many limitations of story point-based forecasting:

1. Handles Variability:
- Simulates multiple outcomes to account for uncertainty.
- Outputs a range of completion dates with probabilities, rather than a single estimate.

2. Simplified data requirements:
- There's no need to determine whether a task is a 1, 2, or 8; instead, make sure the tasks 
are broken down enough (most scrum teams already do this) and are small enough (similar to,
no bigger than an 8).
- Avoids reliance on subjective effort estimates tied to individual team members.
- Reduces reliance on deep technical breakdowns for early-stage forecasts.

3. Encourages workflow improvements
- Data completed with a continuous flow yields tighter MC forecasts than data from 
sprint-based task batching.
- Story point estimates that rely on certain individuals completing tasks encourage 
knowledge silos, increasing business risk.

4. Scales with complexity:
- As projects grow in size and complexity, MC forecasts remain meaningful, while story
points often lose reliability.

## When is Monte Carlo suitable for project work?

Monte Carlo simulations work best when certain conditions are met. 
[https://medium.com/swlh/littles-law-applied-in-agile-knowledge-work-part-1-81c0c1f217ec](This article) offers a good description.

In a nutshell:
- If you're already in the habit of breaking down work, as in the common Scrum practice 
of "no bigger than 8", you don't need to change the size of your work items. They do not
need to all the the same size.
- If you're batching work completion by sprint such that your historical data has
bursts of work completion, a MC simulation will give a broader forecast. If you're able
to modify that such that work enters work in progress and is completed in a continuous
flow, MC simulations will be more useful.
- If it's common for work to be blocked by dependencies after its begun, strive to identify 
and resolve those dependencies before putting a work item into the In-Progress stream.
- Prioritize completing work in progress before starting new work, starting with the
work with the longest in-progress time.
- Limit work in progress. The more work in progress (WIP) at the same time, the longer all
WIP will take to complete.

### Practical Considerations:
- Team size changes, holidays, or other disruptions may affect forecasts.
- Use common sense and context-specific judgement when interpreting results.

- Avoid frequent interruptions or long delays for tasks in progress. Strive to resolve
dependencies prior to starting work on a work item. If work is routinely paused
- Completing work in a steady stream tightens forecast ranges compared to batch
completions (e.g, at the end of sprints)

## 1) Setting up to run the scripts

If you already have python3 and virtual environments set up, skip to installing the dependencies.

### 1.1) Set up your environment. Specifics will depend on your operating system. 
- Install Python3
  * For a mac: https://docs.python-guide.org/starting/install3/osx/
  * For Windows: https://www.google.com/   :-)
  * For Linux: You don't need me to tell you! :-D 

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
If you need to install pip, do so. Here is a link for MacOS: https://www.geeksforgeeks.org/how-to-install-pip-in-macos/

```
$ python3 -m pip install --upgrade pip
$ python3 -m pip --version
```

### 1.5) Install dependencies:
  For a mac:
`$ python3 -m pip install -r requirements.txt`

### 1.6) Make sure it runs with the sample configuration file and sample data.
`$ ./run_simulation.sh`

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
`$ ./mc_by_dates.py <config_file>`

## Interpreting the results:
Results are sent to stdout. 
Example:
```
% ./run_simulation.sh
Reading from ../dates_and_counts.csv
Projecting 10 items for 85 percentile
Using 1000 simulations
Monte Carlo Simulation Results:
50th Percentile (Median): 2024-04-09
85th Percentile: 2024-04-13
95th Percentile: 2024-04-16
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

## Resources

[Little's Law Applied to Agile & Knowledg Work](https://medium.com/swlh/littles-law-applied-in-agile-knowledge-work-part-1-81c0c1f217ec)

[When Will It Be Done?](https://leanpub.com/whenwillitbedone)  Note: I've read this and Vacanti's previous book; this 
one can be considered a revision of the first book.

The podcast that convinced me I don't have to work for a giant company or have a tremendous amount of
process rigor in order for Kanban or Monte Carlo to make sense: [Agile Bites](https://youtu.be/h3Ds80fYvdw?si=prI9pRQK7bR9IRzu)

If you're using Jira and are unable to use a plugin, this tool offers a lot: 
[https://github.com/DeloitteDigitalUK/jira-agile-metrics](Jira Agile Metrics)
