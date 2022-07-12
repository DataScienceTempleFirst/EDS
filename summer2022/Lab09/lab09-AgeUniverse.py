# -*- coding: utf-8 -*-
# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:hydrogen
#     text_representation:
#       extension: .py
#       format_name: hydrogen
#       format_version: '1.3'
#       jupytext_version: 1.10.3
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# %% [markdown] slideshow={"slide_type": "slide"}
# ## The Age of the Universe
# Welcome to Lab 9!
# <br>Elements of Data Science adapted from Berkeley Data8 
#
# Sometimes, the primary purpose of regression analysis is to learn something about the slope or intercept of the best-fitting line.  When we use a sample of data to estimate the slope or intercept, our estimate is subject to random error, just as in the simpler case of the mean of a random sample.
#
# In this lab, we'll use regression to get an accurate estimate for the age of the universe, using pictures of exploding stars.  Our estimate will come from a sample of all exploding stars. We'll compute a confidence interval to quantify the error caused by sampling.

# %% slideshow={"slide_type": "slide"}
name = ...

# %%
## import statements
# These lines load the tests. 
from gofer.ok import check
import numpy as np
from datascience import *
import pandas as pd
import matplotlib
from matplotlib import patches
%matplotlib inline
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.simplefilter('ignore', FutureWarning)
plt.style.use('fivethirtyeight')
from ipywidgets import interact, interactive, fixed
import ipywidgets as widgets

# %% [markdown]
# ### The Actual Big Bang Theory
# In the early 20th century, the most popular cosmological theory suggested that the universe had always existed at a fixed size.  Today, the Big Bang theory prevails: Our universe started out very small and is still expanding.
#
# A consequence of this is Hubble's Law, which says that the expansion of the universe creates the appearance that every celestial object that's reasonably far away from Earth (for example, another galaxy) is moving away from us at a constant speed.  If we extrapolate that motion backwards to the time when everything in the universe was in the same place, that time is (roughly) the beginning of the universe!
#
# Scientists have used this fact, along with measurements of the current *location* and *movement speed* of other celestial objects, to estimate when the universe started.
#
# The cell below simulates a universe in which our sun is the center and every other star is moving away from us.  Each star starts at the same place as the sun, then moves away from it over time.  Different stars have different directions *and speeds*; the arrows indicate the direction and speed of travel.
#
# Run the cell, then move the slider to see how things change over time.

# %% [markdown]
# #### Question 1
# When did the universe start, in this example?

# %%
# Just run this cell.  (The simulation is actually not
# that complicated; it just takes a lot of code to draw
# everything.  So you don't need to read this unless you
# have time and are curious about more advanced plotting.)

num_locations = 15
example_velocities = Table().with_columns(
    "x", np.random.normal(size=num_locations),
    "y", np.random.normal(size=num_locations))
start_of_time = -2

def scatter_after_time(t, start_of_time, end_of_time, velocities, center_name, other_point_name, make_title):
    max_location = 1.1*(end_of_time-start_of_time)*max(max(abs(velocities.column("x"))), max(abs(velocities.column("y"))))
    new_locations = velocities.with_columns(
            "x", (t-start_of_time)*velocities.column("x"),
            "y", (t-start_of_time)*velocities.column("y"))
    plt.scatter(make_array(0), make_array(0), label=center_name, s=100, c="yellow")
    plt.scatter(new_locations.column("x"), new_locations.column("y"), label=other_point_name)
    for i in np.arange(new_locations.num_rows):
        plt.arrow(
            new_locations.column("x").item(i),
            new_locations.column("y").item(i),
            velocities.column("x").item(i),
            velocities.column("y").item(i),
            fc='black',
            ec='black',
            head_width=0.025*max_location,
            lw=.15)
    plt.xlim(-max_location, max_location)
    plt.ylim(-max_location, max_location)
    plt.gca().set_aspect('equal', adjustable='box')
    plt.gca().set_position(make_array(0, 0, 1, 1))
    plt.legend(bbox_to_anchor=(1.6, .7))
    plt.title(make_title(t))
    plt.show()

interact(
    scatter_after_time,
    t=widgets.FloatSlider(min=start_of_time, max=5, step=.05, value=0, msg_throttle=1),
    start_of_time=fixed(start_of_time),
    end_of_time=fixed(5),
    velocities=fixed(example_velocities),
    center_name=fixed("our sun"),
    other_point_name=fixed("other star"),
    make_title=fixed(lambda t: "The world {:01g} year{} in the {}".format(abs(t), "" if abs(t) == 1 else "s", "past" if t < 0 else "future")));

# %% [markdown]
# <font color='blue'>*Write your answer here, replacing this text.*</font>

# %% [markdown]
# #### Question 2
# After 5 years (with the slider all the way to the right), stars with longer arrows are further away from the Sun.  Why?

# %% [markdown]
# <font color='blue'>*Write your answer here, replacing this text.*</font>

# %% [markdown]
# ### Analogy: driving
# Here's an analogy to illustrate how scientists use information about stars to estimate the age of the universe.
#
# Suppose that at some point in the past, our friend Mei started driving in a car going at a steady speed of 60 miles per hour straight east.  We're still standing where she started.

# %% [markdown]
# We want to know how long she's been driving, but we forgot to record the time when she left.  If we find out that she's 120 miles away, and she's been going 60 miles per hour the whole time, we can infer that she left 2 hours ago.
#
# One way we can compute that number is by fitting a line to a scatter plot of our locations and speeds.  It turns out that the *slope* of that line is the amount of time that has passed.  Run the next cell to see a picture:

# %%
# Run this cell to see a picture of Mei's locations over time.

mei_velocity = Table().with_columns("x", make_array(60), "y", make_array(0))
interact(
    scatter_after_time,
    t=widgets.FloatSlider(min=-2, max=1, step=.05, value=0, msg_throttle=1),
    start_of_time=fixed(-2),
    end_of_time=fixed(1),
    velocities=fixed(mei_velocity),
    center_name=fixed("Us"),
    other_point_name=fixed("Mei"),
    make_title=fixed(lambda t: "Mei's position {:01g} hour{} in the {}".format(abs(t), "" if abs(t) == 1 else "s", "past" if t < 0 else "future")));

# %% [markdown]
# The slope of the line is 2 hours.  (The units are vertical-axis units divided by horizontal-axis units, which are $\frac{\texttt{miles}}{\texttt{miles} / \texttt{hour}}$, or hours.)  So that's our answer.
#
# Imagine that you don't know Mei's exact distance or speed, only rough estimates.  Then if you drew this line, you'd get a slightly bad estimate of the time since she left.  But if you measured the distance and speed of hundreds of people who left you at the same time going different speeds, and drew a line through them, the slope of that line would be a pretty good estimate of the time they left, even if the individual measurements weren't exactly right.
#
# The `drivers.csv` dataset contains the speeds and distances-from-start of 100 drivers.  They all left the same starting location at the same time, driving at a fixed speed on a straight line away from the start.  The measurements aren't exact, so they don't fit exactly on a line.  We've created a scatter plot and drawn a line through the data.

# %%
# Just run this cell to plot the data.
small_driving_example = Table().with_columns(
        "Name",                                       make_array("Us", "Mei"),
        "Speed moving away from us (miles per hour)", make_array(0,    60),
        "Current distance from us (miles)",           make_array(0,    120))

x = small_driving_example.column("Speed moving away from us (miles per hour)")
y = small_driving_example.column("Current distance from us (miles)")
plt.scatter(x,y, s=200)

# Now compute the fit and overlay
linear_model=np.polyfit(x,y,1)
linear_model_fn=np.poly1d(linear_model)
x_s=np.arange(0,60)
plt.plot(x_s,linear_model_fn(x_s),color="green")
plt.show()

# %% [markdown]
# #### Question 3
# By looking at the fit line, estimate how long ago (in hours) Mei left.

# %%
# Just run this cell.
drivers= Table.read_table("drivers.csv")
xd,yd = drivers.column("Speed moving away from us (miles per hour)"),drivers.column("Current distance from us (miles)")
drivers

# %%
plt.scatter(xd,yd, color='red')
# Second approach to plotting

#create scatterplot with regression line and confidence interval lines using Seaborn module
sns.regplot(xd, yd)
plt.show()

# %%
##### Fill in the start time you infer from the above line.
driving_start_time_hours = ...
driving_start_time_hours

# %%
check('tests/q3.py')

# %% [markdown]
# ### Back to cosmology
# To do the same thing for the universe, we need to know the distance-from-Earth and speed-away-from-Earth of many celestial objects.  Using pictures taken by very accurate telescopes and a lot of physics, astronomers have been able to estimate both.  It turns out that *nearby supernovae* -- stars that have recently died and exploded -- are among the best sources of this data, because they are very easy to see.  This picture taken by the Hubble telescope shows an entire galaxy, with a single supernova - as bright by itself as billions of stars - at the bottom left.
#
# <img src="supernova.jpg">
#
# Our astronomical data for today will come from the [Supernova Cosmology Project](http://supernova.lbl.gov/union/) at Lawrence Berkeley Lab.  The original dataset is [here](http://supernova.lbl.gov/union/figures/SCPUnion2.1_mu_vs_z.txt), with (brief) documentation [here](http://supernova.lbl.gov/union/descriptions.html#Magvsz).  Each row in the table corresponds to a supernova near Earth that was observed by astronomers.  From pictures like the one above, the astronomers deduced how far away each supernova was from Earth and how fast it was moving away from Earth.  Their deductions were good, but not perfect.
#
# Run the cell below to load the data into a table called `close_novas` and make a scatter plot. (If you prefer, you can also use the name `close_novae`; both are correct.)

# %% [markdown]
# #### Question 4
# Looking this plot, make a guess at the age of the universe.
#
# **Note**: Make sure you get the units right!  In case you need to know what a parsec is, it's a big unit of distance, equivalent to 30.86 trillion kilometers.

# %%
# Just run this cell.
close_novas = Table.read_table("close_novas.csv")
close_novae = close_novas


xn,yn = close_novae.column("Speed (parsecs/year)"),close_novae.column("Distance (million parsecs)")
sns.regplot(xn, yn)
plt.show()

close_novas

# %%
# Fill this in manually by examining the line above.
first_guess_universe_age_years = ...

# This just shows your guess as a nice string, in billions of years.
"{:,} billion years".format(round(first_guess_universe_age_years / 1e9, 2))

# %%
check('tests/q4.py')

# %% [markdown]
# ### Fitting the line yourself
# Displaying a fit line is visually helpful but we need to be able to calculate the slope as a number.  Recall that the least-squares regression line for our supernova data is:
# * the line
# * with the smallest average (over all the supernovae we observe)
# * error,
# * squared,
# * where the error is
#
# $$\text{the supernova's actual distance from Earth} - \text{the height of the line at that supernova's speed.}$$

# %%
## TEST Fitting a practice line with slope and intercept that you pick 
slope = ...
intercept = ...
predict = close_novas.column('Speed (parsecs/year)')*slope+intercept
tbl = close_novas.with_column('predict',predict/1e6)
#tbl = 
tbl


# %% [markdown]
# #### Question 5
# Define a function called `errors`.  It should take three arguments:
# 1. a table like `close_novas` (with the same column names and meanings, but not necessarily the same data)
# 2. the slope of a line (a number)
# 3. the intercept of a line (a number).
#
# It should return an array of the errors made when a line with that slope and intercept is used to predict distance from speed for each supernova in the given table.  (The error is the actual distance minus the predicted distance.)

# %% for_assignment_type="student"
def errors(tbl, slope, intercept):
    ## extract values from table  
    ...
    
    ## predicted values from line  
    predicted_y = ...
    
    ## errors 
    error_values = ...
    
    return ...


# %% [markdown]
# #### Question 6
# Using `errors`, compute the errors for the line with slope `16000` and intercept `0` on the `close_novas` dataset.  Name that array `example_errors`.  Then make a scatter plot of the errors.
#
# **Hint:** To make a scatter plot of the errors, plot the error for each supernova in the dataset.  Put the actual speed on the horizontal axis and the error on the vertical axis.

# %%
example_errors = errors(...,...,...)
example_errors

# %%
## Check sign of error
np.round(example_errors.item(0), 2)

# %%
check('tests/q6.py')


# %% [markdown]
# You should find that the errors are almost all negative.  That means our line is a little bit too steep.  Let's find a better one.

# %% [markdown]
# #### Question 7
# Define a function called `fit_line`.  It should take a table like `close_novas` (with the same column names and meanings) as its argument.  It should return an array containing the slope (as item 0) and intercept (as item 1) of the least-squares regression line predicting distance from speed for that table.
#
# Here we will *minimize* square errors.
#
# Note: If you haven't tried to use the [`minimize` function](http://data8.org/datascience/util.html#datascience.util.minimize) yet, now is a great time to practice. Here's an [example from the textbook, Inferential Thinking 15.3](https://inferentialthinking.com/chapters/15/3/Method_of_Least_Squares.html?highlight=least%20squares).
#
# First we will define an *mse* function to get the mean squared error.

# %%
def mse(tbl,xlabel,ylabel,any_slope,any_intercept):
    xdata, ydata = tbl.column(xlabel), tbl.column(ylabel)
    fitted = any_slope * xdata + any_intercept
    mse = np.mean((ydata - fitted) ** 2)
    print("Root mean squared error:", mse ** 0.5)
    return mse


# %%
mse(close_novas,'Speed (parsecs/year)','Distance (million parsecs)',1600,0)


# %% [markdown]
# In order to use datascience *minimize* function we need to be able to vary all function parameters which is impossible for table name and data column labels so we creat a related function below.

# %%
def mse_c(any_slope,any_intercept):
    tbl = close_novas
    xlabel = 'Speed (parsecs/year)'
    ylabel = 'Distance (million parsecs)'
    xdata, ydata = tbl.column(xlabel), tbl.column(ylabel)
    fitted = any_slope * xdata + any_intercept
    mse = np.mean((ydata - fitted) ** 2)
    print("Root mean squared error:", mse ** 0.5)
    return mse


# %% [markdown]
# ##### Determine the mse (mean squared error) for three values of any_slope and any_intercept

# %%
###
mse_c(...,...)

# %% [markdown]
# Now use minimize to find minimum of mse for any_slope and any_intercept

# %%
minimize(mse_c)

# %%
values = minimize(mse_c)
print(values,values[0],values[1]) # print and extract values


# %% [markdown]
# Now define the function *fit_line* below to use minimize function 

# %%
def fit_line(tbl):
    # Your code may need more than 1 line below here.
    ...
    slope = ...
    intercept = ...
    return make_array(slope, intercept)
    
# Here is an example call to your function.  To test your function,
# figure out the right slope and intercept by hand.
example_table = Table().with_columns(
    "Speed (parsecs/year)", make_array(0, 1),
    "Distance (million parsecs)", make_array(1, 3))
fit_line(example_table)

# %%
check('tests/q7.py')

# %% [markdown]
# #### Question 8
# Use your function to fit a line to `close_novas`.
#
# Then, set `new_errors` equal to the errors that we get calling `errors` with our new line. The following line will graph the corresponding residual plot with a best fit line.
#
# Make sure that the residual plot makes sense (Hint: what qualities should the best fit line of a residual plot have?)

# %%
best_line = ...
best_line_slope = ...
best_line_intercept = ...

new_errors = ...

# This code displays the residual plot, given your values for the best_line_slope and best_line_intercept
best=Table().with_columns("Speed (parsecs/year)", 
                    close_novas.column("Speed (parsecs/year)"), 
                    "Distance errors (million parsecs)", 
                    new_errors
                   )
xb,yb = best.column("Speed (parsecs/year)"),best.column("Distance errors (million parsecs)")
sns.regplot(xb, yb)
plt.show()

# This just shows your answer as a nice string, in billions of years.
"Slope: {:g} (corresponding to an estimated age of {:,} billion years)".format(best_line_slope, round(best_line_slope/1000, 4))

# %% [markdown]
# That slope (multiplied by 1 million) is an estimate of the age of the universe.  The current best estimate of the age of the universe (using slightly more sophisticated techniques) is 13.799 billion years.  
# <br>
# What was our determined age? Did we get close?<br>
#
# <font color='blue'>*Write your answer here, replacing this text.*</font>
#
#
# One reason our answer might be a little off is that we are using a sample of only some of the supernovae in the universe.  Our sample isn't exactly random, since astronomers presumably chose the novae that were easiest to measure (or used some other nonrandom criteria).  But let's assume it is.  How can we produce a confidence interval for the age of the universe?

# %% [markdown]
# #### Question 9
# It's time to bootstrap so that we can quantify the variability in our estimate! Simulate 1000 resamples from `close_novas`.  For each resample, compute the slope of the least-squares regression line, and multiply it by 1 million to compute an estimate of the age of the universe.  Store these ages in an array called `bootstrap_ages`, and then use them to compute a 95% confidence interval for the age of the universe.
#
# **Note:** This might take up to a minute, and more repetitions will take even longer. See text: [Inferential Thinking 13.1](https://inferentialthinking.com/chapters/13/2/Bootstrap.html?highlight=bootstrap)

# %%
bootstrap_ages = make_array()
for i in np.arange(1000):
    bootstrap_ages = ...

lower_end = ...
upper_end = ...
Table().with_column("Age estimate", bootstrap_ages*1e-9).hist(bins=np.arange(12, 16, .1), unit="billion years")
print("95% confidence interval for the age of the universe: [{:g}, {:g}] billion years".format(lower_end*1e-9, upper_end*1e-9))

# %%
check('tests/q9.py')

# %% [markdown]
# Nice work, data astronomer! You can compare your result to the [Planck project 2015 results](https://arxiv.org/pdf/1502.01589.pdf), which estimated the age of the universe to be 13.799±0.021 billion years. **Please remember to submit!***

# %%
# For your convenience, you can run this cell to run all the tests at once!
import glob
from gofer.ok import check
correct = 0
checks = [3,4,6,7,9]
total = len(checks)
for x in checks:
    print('Testing question {}: '.format(str(x)))
    g = check('tests/q{}.py'.format(str(x)))
    if g.grade == 1.0:
        print("Passed")
        correct += 1
    else:
        print('Failed')
        display(g)

print('Grade:  {}'.format(str(correct/total)))
print("Nice work ",name)
import time;
localtime = time.asctime( time.localtime(time.time()) )
print("Submitted @ ", localtime)
