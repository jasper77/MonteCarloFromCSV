# Monte Carlo from CSV input

## What is this?
This is a command line utility you can use to run a Monte Carlo forecast to see how long a number of items might take 
to complete given a set of dates on which similar items were completed previously. Either use it to make a forecast
in the future for a project work breakdown, or use it to see how right or wrong the method might have been for a 
project you've already completed.  You need two things: a CSV file containing a list of dates on which past items 
were completed, along with the numbers of items completed on each of those dates, and the number of items you would 
like a forecast for. You do not need to know when work items started, or how long they took to complete.

This is not a completely polished utility and there is more I'd like to do with it, but it works as advertised. 

## Why use this?
Monte Carlo simulations are one way to answer "When will it be done?" for software projects. You can get meaningful
results faster and with less data than alternative methods. Depending on what you track, you might not need deep
technical deep dives in order to get useful forecasts. Since MC forecasts give you calendar dates, not sizes, they
need less interpretation.  If you are wondering how well MC simulations might work with the sort of data you already
have, with the workflow you already have, this utility can help answer.

MC simulation tells you, based on historical data, future calendar dates with probabilities of completing by those 
dates. For example, 85% of the simulations completed all of the tasks by MM-DD-YYYY. All you need are the dates upon which 
similar items were completed in the past, and a count of how many items were completed on those dates. In the right
situation, Monte Carlo forecasting can give you meaningful early projections with less effort than alternatives, and
can be used to make more meaningful projections as a project is underway. What do we mean by "similar items?" That
answer depends on your context. They could be simply "tasks" as long as you have a consistent way of defining tasks. 
They could be epics, or user stories, or mini-milestones.

Monte Carlo has several advantages over using story points:

- Instead of giving a single date, MC simulations account for variability and uncertainty by running multiple
simulations with random inputs from your data set, and uses distributions to model the uncertainty.

- If you are able to consistently break down work into "small enough" pieces, you can use MC without knowing the 
sizes of the individual pieces more precisely. The pieces do not need to be the same size as each other, as long 
as they're not too big. This is similar to a common scrum practice of "If it's bigger than an 8, break it down," 
so if you already do this, your data might already be the right kind of data.

- If your work breakdowns are at a level that do not require deep technical dives and technical breakdowns, then 
you can use MC to make forecasts without such deep dives. That means if you regularly identify a trackable level 
above the technical tasks, whether they be user stories or mini milestones or whatever you call them, you can use 
those instead of the detailed technical tasks. And if you're able to identify that breakdown without the more time 
consuming technical breakdown in a meaningful way, you can use MC simulations before doing the deep dive.

- If your story point sizes depend on knowing who will do sized work item, that can encourage teams to always have work
items done by the people who can do them the fastest, which encourages knowledge silos and increases business risk.

- Monte Carlo simulations give you calendar dates. Yes, you do need to apply judgement to interpreting them, the 
same as you should with any forecasting method. Considering factors such as whether your team size has changed, or 
were there significant interruptions in the past or will there be coming up. And if you change the nature of the 
work item you're tracking or doing, that will effect results.

- As projects increase in size and complexity, where the cumulative uncertainty of many tasks can significantly 
affect the forecast, MC simulations become more meaningful, while story points become less reliable.

The above points mean that, if you have the data, you can get meaningful forecasts faster. 

If you follow a common practice of loading up a sprint with tasks at the start, and aim to complete them all before 
the end of the sprint, instead of following a continuous flow, you'll find the ranges given by a MC forecast will be 
wider. Switching to a continuous flow will make MC forecasts more useful.

Would you like to use past data to forecast a project you already completed, to see how close a Monte Carlo simulation 
came to reality? Would you like to make a forecast on an upcoming project? On an ongoing project?

This is a set of scripts that will run a Monte Carlo simulation from the contents of a CSV file, from the command line. 

## When is Monte Carlo suitable for project work?
A popular misconception is that since Monte Carlo projections don't require you to differentiate between small and large
tasks, then they only work for tasks of about the same size. While a collection of tasks of varying sizes can be 
forecasted using Monte Carlo, a few things do need to be true for the forecasts to be meaningful:
- The work size can't vary too much. Generally, if you've been following Scrum and you're already good at breaking down
work that is too big, then you're already doing what you need to do; make sure the work isn't too big.
- Little's Law is satisfied when:
  - The rate at which new work items enter "Work in Progress" is about the same at the rate at which work exits. In 
  other words, don't take new work faster than your ability to complete existing work.
  - The number of work items in progress remains about the same. 
  - The amount of time a work item spends in progress, from when you start working on it to when it's done, doesn't 
  vary a lot. That means you don't start items and let them sit "in progress", blocked by dependencies or interrupted
  by higher priority work, at least not regularly.

In practice, these constraints mean:
- If you have work in progress and a hot priority comes up, instead of putting an in-progress work item on hold, 
make the hot priority the next thing to start after after completing something in progress. If you simply must interrupt 
work in progress, such as addressing an on-call fire, that doesn't negate Monte Carlo, as long as it doesn't happen
too often.
- Always prioritize finishing work in progress before starting new work. If you have a team and team members make it
a practice to see what they can do to help complete work in progress before starting new work, not only does that
break down knowledge silos, it also improves overall team throughput while increasing the utility of MC forecasts.
- Prioritize the oldest work first, where "oldest" is work that entered in-progress first.
- If a work item is blocked due to an external dependency, strive to resolve that dependency. Better yet, strive to 
make sure you don't start work on an item until external dependencies are resolved. If your workflows depends on 
reaching a point and then pausing to wait on something external you can't control and with a high degree of variability,
consider re-examining how you define your workflow.
- Whenever your team size changes, such that your WIP limit (amount of work you can have in progress at the same time) 
changes, understand that will affect forecasts.
- Whenever anything happens to interrupt the flow, such as a holiday or vacation season, understand that will affect 
forecasts. Neither this point nor the point above means MC can't work, it means you need to
use common sense when deciding how to apply the forecasts.
- The more work there is in progres at the same time, the longer it will take to finish them.
 

## Motivation behind this project
I've worked for multiple companies dedicated to using Scrum, and using story points for forecasting. I was looking for a way to get early forecasts faster and without involving all the people you need for a meaningful technical breakdown and story point exercise, and a better way to update forecasts as a project progresses. I'd heard that some companies find that Kanban worked better for them, and they don't use story points; instead they make sure
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
