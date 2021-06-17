# Making improvements to plot_data.py
from os import times
import matplotlib.pyplot as plt
import random
import numpy as np
from scripts import make_heatmap as mh

# Set the size of the figures that appear in the Jupyter notebook
plt.rcParams["figure.figsize"] = [12, 7]

# axs is an array of plt.Axes objects.
# think about them as all data associated with a plot
# TODO: Consider axis :: what should be done along the x and y axis for units?
def plot_pauses_bar(xdata=[], ydata=[], axs=None, color="", label="", optional=None):
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


def plot_pauses_scatter(xdata=[], ydata=[], axs=None, color="", label="", optional=None):
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
#   labels       :  list of labels (strings) to describe each passed (x/y) data list
#   colors(optional) :  list of colors to plot for each list passed. None => random colors
#   axs(optional)    :  plot with existing metadata. None => new figure created
def compare_pauses_bar(timedata_lists=[], heightdata_lists=[], axs=None, colors=None, labels=[]):
    return __generic_plotting(timedata_lists, heightdata_lists, axs, colors, labels, plot_pauses_bar)


# Plots multiple sets of data onto the same scatter plot
# Parameters:
#   xdata_list       : list of [lists of x data, typically timestamps in seconds]
#   ydata_list       : list of [lists of y data, typically pauses in miliseconds]
#   axs(optional)    : A current plot with metadata/plotted values. None => new figure created
#   colors(optional) : A list of colors to plot corresponding to each of the passed list. None => random color
#   labels       : A list of labels to describe each passed list being plotted.
# Return:
#   axes (matplotlib.pyplot.Axes object) with everything plotted on it.
def comparrison_scatter(xdata_list, ydata_list, axs=None, colors=[], labels=[]):
    return __generic_plotting(xdata_list, ydata_list, axs, colors, labels, plot_pauses_scatter)


# Display what percent of pauses meet a certain percentile threshold
# Parameters:
#   pauses_miliseconds  : a list of pauses to be analyzed (in any order)
#   print_title         : True if you would like column headers
#   percentiles         : a list of percentiles to be plotted, in float list form.
#   label               : a label to be printed. Should be 0-10 characters
def print_percentiles(pauses_miliseconds=[], print_title=True, percentiles=None, label=None):
    if not pauses_miliseconds:
        print("pauses_miliseconds not provided to print_percentiles")
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
        print("Percentiles| " + title + "\n" + "-" * (len(title) + 12))
    print(__string_const_chars(label, 10) + " | ", end="")
    for p in percentiles:
        print(__string_const_chars(str(round(percentile_table[p], 3)), 6) + " | ", end="")
    print("")


# Plot the percentiles for pause time in miliseconds for all lists provided, on the same table
# Parameters:
#   pauses_miliseconds    : list of [list of pauses as floats in ms]
#   percentiles(optional) : list of float value percentiles to be viewed.
def compare_pauses_percentiles(list_of_list_pauses_ms=[], percentiles=None, labels=None):
    if not list_of_list_pauses_ms:
        print("No list_of_list_pauses_ms provided to plot_compare_percentiles")
        return
    if not labels:
        labels = [str(i) for i in range(len(list_of_list_pauses_ms))]
    print_percentiles(list_of_list_pauses_ms[0], True, percentiles, labels[0])

    for i in range(1, len(list_of_list_pauses_ms)):
        print_percentiles(list_of_list_pauses_ms[i], False, percentiles, labels[i])


# Print the trends within the data (total number of pauses, max wait, total wait mean wait)
# returns total wait
# Parameters:
#   pauses_miliseconds    : list of pauses (floats)
#   label                 : label for this row in the table
#   print_title(optional) : bool, True => print recorded values


def print_trends(pauses_miliseconds, label=None, print_title=True, total_runtime_seconds=0, timestamps=None):
    # Analyze trends. ALL PAUSES ARE IN MILISECONDS.
    max_pause = round(max(pauses_miliseconds, key=lambda i: float(i)), 4)
    sum_pauses = round(sum(float(i) for i in pauses_miliseconds), 4)
    average_wait = round(sum_pauses / len(pauses_miliseconds), 4)
    throughput = None
    if total_runtime_seconds:
        throughput = ((total_runtime_seconds * 1000) - sum_pauses) / (total_runtime_seconds * 1000)
    elif timestamps:
        throughput = ((timestamps[-1] * 1000) - sum_pauses) / (timestamps[-1] * 1000)

    # Print title with formatting
    if print_title:
        title = " Trends       | "  # 16 characters
        title += " Total Pauses | "
        title += " Max pause    | "
        title += " Sum pauses   | "
        title += " Mean pauses  | "
        if throughput:
            title += " Throughput   |"
        print(title)
        print("-" * len(title))
    num_chars = 16 - 3  # 16 = line length, 3 for ending char sequence " | "
    if not label:
        label = "Run:"
    # print with correct formatting the values
    line = __string_const_chars(label, num_chars) + " | "
    line += __string_const_chars(str(len(pauses_miliseconds)), num_chars) + " | "
    line += __string_const_chars(str(max_pause), num_chars) + " | "
    line += __string_const_chars(str(sum_pauses), num_chars) + " | "
    line += __string_const_chars(str(average_wait), num_chars) + " | "
    if throughput:
        line += __string_const_chars(str(throughput) + "%", num_chars) + " | "
    print(line)


# Compares trends from a list of pauses lists
def compare_trends(pauses_ms_lists, labels=None):
    if not pauses_ms_lists:
        print("No pauses_ms_lists in compare_trends.")
        return
    if not labels:
        labels = [str(i) for i in range(len(pauses_ms_lists))]
    print_trends(pauses_ms_lists[0], labels[0], True)
    for i in range(1, len(pauses_ms_lists)):
        print_trends(pauses_ms_lists[i], labels[i], False)


# Creates a string in exactly the specified numchars.
# If len(string) > numchars, some of the string is not displayed.
# if len(string) < numchars, spaces are appended to the back of the string.
# returns a string containing the update string with len = numchars.
def __string_const_chars(string, numchars):
    string = str(string)
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
def plot_pauses_line(time_seconds=[], pauses_miliseconds=[], axs=None, color="", label="", optional=None):
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
def compare_pauses_line(timedata_lists=[], ydata_lists=[], axs=None, colors=None, labels=[]):
    return __generic_plotting(timedata_lists, ydata_lists, axs, colors, labels, plot_pauses_line)


def plot_paused_and_running_line(
    time_seconds=[], pauses_miliseconds=[], axs=None, color="", label="", const_bar_width=False
):
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
    x_data = []
    y_data = []
    ###### Create X-Y Data. bumps for height based on pause duration #####
    if not const_bar_width:
        for x, y in zip(time_seconds, pauses_miliseconds):
            # convert y from ms to seconds
            y_scaled = y / 1000
            # first, create a point at time before pause
            x_data.append(x)
            y_data.append(0)
            # next, create a point of y height, at that initial time
            x_data.append(x)
            y_data.append(y)
            # last point in pause duration high
            x_data.append(x + y_scaled)
            y_data.append(y)
            # end pause duration high
            x_data.append(x + y_scaled)
            y_data.append(0)
    else:  # Create buckets of the same size, placed uniformly over time.
        pt_uniform = time_seconds[0] * 0.7  # 0.7 constant for bar width
        # 1 means bars indistinguishable
        # 0 means no bars
        for x, y in zip(time_seconds, pauses_miliseconds):
            x_data.append(x)
            y_data.append(0)
            x_data.append(x)
            y_data.append(y)
            x_data.append(x + pt_uniform)
            y_data.append(y)
            x_data.append(x + pt_uniform)
            y_data.append(0)

    axs.plot(x_data, y_data, color=color, label=label),
    axs.set_ylabel("Pause duration (miliseconds)")
    axs.set_xlabel("Time from program start (seconds)")
    axs.set_title("Pauses during runtime")
    axs.legend()


# Applys a mapping for each list entry to the needed plotting function
def compare_paused_running_line(xdata_list, ydata_list, axs=None, colors=[], labels=[], const_bar_width=False):
    return __generic_plotting(
        xdata_list, ydata_list, axs, colors, labels, plot_paused_and_running_line, const_bar_width
    )


def __generic_plotting(xdata_list, ydata_list, axs=None, colors=[], labels=[], plotting_function=None, optional=None):
    if not xdata_list:
        print("No timedata list in function plot_bar_compare()")
        return
    if not ydata_list:
        print("No heightdata list in plot_bar_compare()")
        return
    if not labels:
        print("No label list in plot_bar_compare()")
    if len(xdata_list) != len(ydata_list):
        print("Length of xdata_lists and ydata_lists do not match.", end="")
        print("xdata_lists: " + str(len(xdata_list)) + ", ydata_list: " + str(len(ydata_list)))
        return
    if len(xdata_list) != len(labels):
        print("Length of timedata_lists and labels do not match.", end="")
        print("xdata_lists: " + str(len(xdata_list)) + ", labels: " + str(len(labels)))
        return
    if not colors:
        colors = []
    while len(colors) < len(xdata_list):
        colors.append(None)
    if not axs:
        fig, axs = plt.subplots()

    # Apply the specific plotting
    for i in range(len(xdata_list)):
        plotting_function(xdata_list[i], ydata_list[i], axs, colors[i], labels[i], optional)
    return axs


def plot_heatmap(heatmap, dimensions, labels=True):
    return mh.plot_heatmap(heatmap, dimensions, labels)


def print_metadata(metadata_table, labels=None, column_width=14):
    if not labels:
        labels = [i for i in range(len(metadata_table))]
    categories = {}
    for item in metadata_table[0]:
        categories[item[0]] = [item[0]]
    for metadata in metadata_table:
        for section in metadata:
            categories[section[0]].append(section[1])
    labels.insert(0, "Category")
    __print_metadata_section(labels, column_width)
    for section in metadata_table[0]:
        __print_metadata_section(categories[section[0]], column_width)


def __print_metadata_section(values_list, column_width):
    num_chars = column_width - 1
    line = ""
    for value in values_list:
        if len(value) < num_chars:
            line += __string_const_chars(value, num_chars) + "|"
        else:
            line += __string_const_chars(value[:num_chars], num_chars) + "|"
    print(line)
    line = ""
    for value in values_list:
        if len(value) < num_chars:
            line += __string_const_chars(" ", num_chars) + "|"
        else:
            line += __string_const_chars(value[num_chars:], num_chars) + "|"
    print(line)
    print(len(line) * "-")
