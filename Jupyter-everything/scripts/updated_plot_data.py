# Making improvements to plot_data.py
import matplotlib.pyplot as plt
import random
import numpy as np

# Set the size of the figures that appear in the Jupyter notebook
plt.rcParams["figure.figsize"] = [12, 7]

# axs is an array of plt.Axes objects.
# think about them as all data associated with a plot
# TODO: Consider axis :: what should be done along the x and y axis for units?
def plot_pauses_bar(xdata=[], ydata=[], axs=None, color="", label=""):
    if not axs:
        print("No axes supplied. Create one using\nf, axs = matplotlib.pyplot.subplots()")
        return
    if not label:
        label = "No label provided"
    if not color:
        r = random.random()
        b = random.random()
        g = random.random()
        color = (r, g, b)

    axs.bar(x=xdata, height=ydata, color=color, label=label, width=2.0)
    axs.set_ylabel("Pause duration (miliseconds)")
    axs.set_xlabel("Time from program start (seconds)")
    axs.set_title("Pauses during runtime")
    axs.legend()


def plot_pauses_scatter(xdata=[], ydata=[], axs=None, color="", label=""):
    if not axs:
        print("No axes supplied. Create one using\nf, axs = matplotlib.pyplot.subplots()")
        return
    # If the color and label parameters have not been passed, use a random color as the new label

    if not label:
        label = "No label provided"
    if not color:
        r = random.random()
        b = random.random()
        g = random.random()
        color = (r, g, b)

    axs.scatter(x=xdata, y=ydata, color=color, label=label)
    axs.set_ylabel("Pause duration (miliseconds)")
    axs.set_xlabel("Time from program start (seconds)")
    axs.set_title("Pauses during runtime (scatter)")
    axs.legend()


# Compare multiple plots using a bar graph.
# Parameters:
#   timedata_lists   :  list of [ list of times (x data) to be plotted]
#   heightdata_lists :  list of [ list of heights (y data) to be plotted]
#   label_list       :  list of labels (strings) to describe each passed (x/y) data list
#   colors(optional) :  list of colors to plot for each list passed. None => random colors
#   axs(optional)    :  plot with existing metadata. None => new figure created
def plot_bar_comparison(timedata_lists=[], heightdata_lists=[], axs=None, colors=None, label_list=[]):
    if not timedata_lists:
        print("No timedata list in function plot_bar_comparison()")
        return
    if not heightdata_lists:
        print("No heightdata list in plot_bar_comparison()")
        return
    if not label_list:
        print("No label list in plot_bar_comparison()")
    if len(timedata_lists) != len(heightdata_lists):
        print("Length of timedata_lists and heightdata_lists do not match.", end="")
        print("timedata_lists: " + str(len(timedata_lists)) + ", heightdata_lists: " + str(len(heightdata_lists)))
        return
    if len(timedata_lists) != len(label_list):
        print("Length of timedata_lists and label_list do not match.", end="")
        print("timedata_lists: " + str(len(timedata_lists)) + ", label_list: " + str(len(label_list)))
        return
    if not colors:
        colors = []
    if not axs:
        fig, axs = plt.subplots()

    while len(colors) < len(timedata_lists):
        colors.append(None)

    for i in range(len(timedata_lists)):
        plot_pauses_bar(
            timedata_lists[i],
            heightdata_lists[i],
            axs,
            colors[i],
            label_list[i],
        )
    return axs


# Plots multiple sets of data onto the same scatter plot
# Parameters:
#   xdata_list       : list of [lists of x data, typically timestamps in seconds]
#   ydata_list       : list of [lists of y data, typically pauses in miliseconds]
#   axs(optional)    : A current plot with metadata/plotted values. None => new figure created
#   colors(optional) : A list of colors to plot corresponding to each of the passed list. None => random color
#   label_list       : A list of labels to describe each passed list being plotted.
# Return:
#   axes (matplotlib.pyplot.Axes object) with everything plotted on it.
def plot_comparison_scatter(xdata_list, ydata_list, axs=None, colors=[], label_list=[]):
    if not xdata_list:
        print("No timedata list in function plot_bar_comparison()")
        return
    if not ydata_list:
        print("No heightdata list in plot_bar_comparison()")
        return
    if not label_list:
        print("No label list in plot_bar_comparison()")
    if len(xdata_list) != len(ydata_list):
        print("Length of xdata_lists and ydata_lists do not match.", end="")
        print("xdata_lists: " + str(len(xdata_list)) + ", ydata_list: " + str(len(ydata_list)))
        return
    if len(xdata_list) != len(label_list):
        print("Length of timedata_lists and label_list do not match.", end="")
        print("xdata_lists: " + str(len(xdata_list)) + ", label_list: " + str(len(label_list)))
        return
    if not colors:
        colors = []
    while len(colors) < len(xdata_list):
        colors.append(None)
    if not axs:
        fig, axs = plt.subplots()

    for i in range(len(xdata_list)):
        plot_pauses_scatter(xdata_list[i], ydata_list[i], axs, colors[i], label_list[i])
    return axs


# Display what percent of pauses meet a certain percentile threshold
# Parameters:
#   pauses_miliseconds  : a list of pauses to be analyzed (in any order)
#   print_title         : True if you would like column headers
#   percentiles         : a list of percentiles to be plotted, in float list form.
#   label               : a label to be printed. Should be 0-10 characters
def plot_percentiles(pauses_miliseconds=[], print_title=True, percentiles=None, label=None):
    if not pauses_miliseconds:
        print("pauses_miliseconds not provided to plot_percentiles")
        return
    pauses_miliseconds = sorted(pauses_miliseconds, reverse=True)
    percentile_table = {}
    if not percentiles:
        percentiles = [50, 75, 90, 95, 99, 99.9, 99.99]
    for p in percentiles:
        percentile_table[p] = np.percentile(pauses_miliseconds, p)
    if not label:
        label = "label"
    if print_title:
        title = ""
        for p in percentiles:
            title += __string_const_chars(str(p) + "%", 6) + " | "
        print("label      | " + title + "\n" + "-" * (len(title) + 12))
    print(__string_const_chars(label, 10) + " | ", end="")
    for p in percentiles:
        print(__string_const_chars(str(round(percentile_table[p], 3)), 6) + " | ", end="")
    print("")


# Plot the percentiles for pause time in miliseconds for all lists provided, on the same table
# Parameters:
#   pauses_miliseconds    : list of [list of pauses as floats in ms]
#   percentiles(optional) : list of float value percentiles to be viewed.
def plot_comparison_percentiles(pauses_miliseconds=[], percentiles=None, labels=None):
    if not pauses_miliseconds:
        print("No pauses_miliseconds provided to plot_comparison_percentiles")
        return
    if not labels:
        labels = [str(i) for i in range(len(pauses_miliseconds))]
    plot_percentiles(pauses_miliseconds[0], True, percentiles, labels[0])

    for i in range(1, len(pauses_miliseconds)):
        plot_percentiles(pauses_miliseconds[i], False, percentiles, labels[i])


# Print the trends within the data (total number of pauses, max wait, total wait mean wait)
# returns total wait
# Parameters:
#   pauses_miliseconds : list of pauses (floats)
#   print_to_screen    : bool, True => print recorded values
def print_trends(pauses_miliseconds, print_to_screen=True):

    max_wait = max(pauses_miliseconds, key=lambda i: float(i))
    total_wait = round(sum(float(i) for i in pauses_miliseconds), 4)
    average_wait = round(total_wait / len(pauses_miliseconds), 4)

    if print_to_screen:
        print("Total num pauses in ms: " + str(len(pauses_miliseconds)) + "\n")
        print("Max wait in  ms: " + str(max_wait) + " ms\n")
        print("Total wait in ms: " + str(total_wait) + " ms\n")
        print("Average (mean) wait in ms: " + str(average_wait) + " ms\n")

    return total_wait


# Creates a string in exactly the specified numchars.
# If len(string) > numchars, some of the string is not displayed.
# if len(string) < numchars, spaces are appended to the back of the string.
# returns a string containing the update string with len = numchars.
def __string_const_chars(string, numchars):
    char_list = ""
    for i in range(len(string)):
        char_list += string[i]
        numchars -= 1
        if numchars == 0:
            return char_list
    for i in range(numchars):
        char_list += " "
    return char_list


# Plots pauses from a passed set of timestamps in seconds and pause durations in miliseconds.
# Parameters:
#   time_seconds       : list of timestamps in seconds
#   pauses_miliseconds : list of pauses in miliseconds
#   axs                : plot with existing metadata.
#   color(optional)    : Color for this line. None => random color
def plot_pauses_line(time_seconds=[], pauses_miliseconds=[], axs=None, color="", label=""):
    if not axs:
        print("No axes supplied. Create one using\nf, axs = matplotlib.pyplot.subplots()")
        return
    if not label:
        label = "No label provided"
    if not color:
        r = random.random()
        b = random.random()
        g = random.random()
        color = (r, g, b)
    axs.plot(time_seconds, pauses_miliseconds, color=color, label=label)
    axs.set_ylabel("Pause duration (miliseconds)")
    axs.set_xlabel("Time from program start (seconds)")
    axs.set_title("Pauses during runtime")
    axs.legend()


# Compare a different lists of timestamps and ydata on the same line graph.
# Parameters:
#   timedata_lists : list of [list of timestamps in seconds]
#   ydata_lists    : list of [list of pause durations, in miliseconds]
#   axs(optional)  : a matplotlib.pyplot.Axes object. Contains plot information. None => new figure
#   colors(optiona): The colors in order to plot onto the line graph. None => Random colors
#   labels         : The list of labels for each list of data.
#  Return : axs (matplotlib.pyplot.Axes object) with updated information plotted from the graph
def comparison_pauses_line(timedata_lists=[], ydata_lists=[], axs=None, colors=None, labels=[]):
    if not timedata_lists:
        print("No timedata list in function plot_bar_comparison()")
        return
    if not ydata_lists:
        print("No heightdata list in plot_bar_comparison()")
        return
    if not labels:
        print("No label list in plot_bar_comparison()")
    if len(timedata_lists) != len(ydata_lists):
        print("Length of timedata_lists and heightdata_lists do not match.", end="")
        print("timedata_lists: " + str(len(timedata_lists)) + ", heightdata_lists: " + str(len(ydata_lists)))
        return
    if len(timedata_lists) != len(ydata_lists):
        print("Length of timedata_lists and label_list do not match.", end="")
        print("timedata_lists: " + str(len(timedata_lists)) + ", label_list: " + str(len(labels)))
        return
    if not colors:
        colors = []
    if not axs:
        fig, axs = plt.subplots()
    while len(colors) < len(timedata_lists):
        colors.append(None)

    for i in range(len(timedata_lists)):
        plot_pauses_line(timedata_lists[i], ydata_lists[i], axs, colors[i], labels[i])
    return axs
