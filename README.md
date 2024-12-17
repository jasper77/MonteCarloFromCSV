# Monte Carlo from CSV input

## Why use this?
Monte Carlo simulations are one way to answer "When will it be done?" for software projects that use a Kanban workflow. It will tell you, based on historical data, future calendar dates with probabilities of completing by then. For example, 85% of the simulations completed all of the tasks by MM-DD-YYYY.    All you need are the dates upon which similar items were completed in the past, and a count of how many items were completed on those dates.

Monte Carlo has several advantages over using story points:

- If you are able to consistently break down work into "small enough" pieces, you can use MC without knowing the sizes of the individual pieces more precisely. The pieces do not need to be the same size as each other, as long as they're not too big. This is similar to a common scrum practice of "If it's bigger than an 8, break it down," so if you already do this, your data might be the right kind of data.

- If your work breakdowns are at a level that do no require deep technical dives and technical breakdowns, then you can use MC to make forecasts without such deep dives. That means if you regularly identify a trackable level above the technical tasks, whether they be user stories or mini milestones or whatever you call them, you can use those instead of the detailed technical tasks. And if you're able to identify that breakdown without the more time consuming technical breakdown in a meaningful way, you can use MC simulations before doing the deep dive.

- Monte Carlo simulates give you calendar dates. Yes, you do need to apply judgement to interpreting them, the same as you should with any forecasting method. Considering factors such as whether your team size has changed, or were there significant interruptions in the past or will there be coming up. And if you change the nature of the work item you're tracking or doing, that will effect results.

Both of the above points mean that, if you have the data, you can get meaningful forecasts faster. 

If you follow a common practice of loading up a sprint with tasks at the start, and aim to complete them all before the end of the sprint, instead of following a continuous flow, you'll find the ranges given by a MC forecast will be wider. Switching to a continous flow will make MC forecasts more useful.

Would you like to use past data to forecast a project you already completed, to see how close a Monte Carlo simulation came to
reality? Would you like to make a forecast on an upcoming project? On an ongoing project?

This is a set of scripts that will run a Monte Carlo simulation from the contents of a CSV file, from the command line. 

## Motivation behind this project
I've worked for multiple companys dedicated to using Scrum, and using story points for forecasting. I was looking for a way to get early forecasts faster and without involving all the people you need for a meaningful technical breakdown and story point exercise, and a better way to update forecasts as a project progresses. I'd heard that some companies find that Kanban worked better for them, and they don't use story points; instead they make sure
all tasks are broken down small enough (akin to "If it's bigger than an 8, break it down or make it smaller", a common practice among
teams that follow scrum) and then use Monte Carlo to answer the question "How long will the set of items for this project take to
complete?" I wanted to explore how to use Monte Carlo using my own data, not a Jira plugin. This tool accomplishes that goal. 

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
