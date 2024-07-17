# Python Coding Exercise
Data for the following exercise can be found [here](https://raw.githubusercontent.com/plotly/datasets/master/finance-charts-apple.csv).<p>
Please download the data locally and create a python package to accomplish the following:
1. Compute some basic information about the data set:<p>
a. What is the max, min, and average value (you may use the close price for the calculation or any other derivative if you’d like)<p>
b. Ensure that the time series data is clean. <p>
In the event a row is out of order or a duplicate exists please ignore the record and report them out after the
processing (the current data set does not include any dirty records)<p>
2. Find the average volume for the entire data set, please filter out any rows that are below this value and save the result set to a new csv file
3. Please also add the actual day of the entry into its own column (e.g., Monday, Tuesday, etc.)
4. Please aggregate the data sets to a week level and save the new data set as a separate csv file
5. Please graph the results from step #3 visually as a candlestick chart (you may utilize any open source library for this portion of the exercise)

# Solution
I have created a single script `answers.py` to answer all the questions.<p>
Questions 1-4 appear in stdout, Question 5 displays in the default browser window (see below).<p>
Each question is answered and provides sample data to visually validate the results.<p>
CSV files are (over)written out to the `data` directory (I handle both the data being stored locally or retrieving from the URL).<p>
The Candlestick chart is rendered using Plotly, but a package like Matplotlib would be easy to implement as well.<p>
`poetry` is required to execute the solution.<p>
URL's and file names are hard coded in the script; in a real life application, I would put these in a configuration file (using a Class or Dataclass) or accept them from the command line.<p>

# Candlestick Chart
The chart should render in your default browser. The Candlestick chart should look like this:
![img.png](img.png)
I have eliminated days that are under the average volume, so the chart will not have contiguous days.

# Usage
Setup (assuming Python already installed): [Install Poetry](https://python-poetry.org/docs/#installation)<p>
`poetry install`<p>
To test: `poetry run pytest`<p>
To execute: `poetry run python -m apple.answers`

# Assumptions
 - Python & Browser are installed
 - Compute has access to the Internet
 - There are less than 1,000,000 rows in the source data set. If there were more rows, I would have used a different approach; possibly yielding and buffering files or for Big Data sets, I would implement in Spark.
 - For Question 1:
   - Using `APPL.Close` for the aggregates
 - For Question 4:
    - 'week level' is driven by the data. Ie if data does not exist in a particular week, no rows are shown.
    - only aggregating the unique, in order data set (not the subset of data below the average volume).
 - For Question 5:
   - 'low volume days' are the days below the average volume
   - only low volume days are shown, so there will be many "missing" days on the chart
