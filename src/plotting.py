#      plotting.py
#
#   Defines functions to create plots based on filters and groupings, and a list of 
#   gc_event_dataframes. Each function returns or creates a plot or ASCII table.
#
#   Ellis Brown, 7/7/2021

import matplotlib.pyplot as plt
from filter_and_group import filter_and_group


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
#       plot_scatter
#
#   Plots a scatter plot based on the provided gc_event_dataframes, and filters.
#   Returns a plot object that can then be updated.
#
def plot_scatter(
    gc_event_dataframes,  # list of dataframes, containing gc event information. 
    group_by=None,  # A string to explain what groups to make within 1 gc_event_dataframe
    filter_by=None, # resitrctions on the data. list of tuples: (column, boolean-function) 
    labels=None,    # list of str labels to describe each gc_event_dataframe.  
    colors=None,    # colors to override 
    plot=None,
    column="Duration_miliseconds",
):  
    # Filter and group data. Update colors and labels to reflect to-be-plotted data
    timestamp_groups, datapoint_groups, labels, colors, _ = filter_and_group(
        gc_event_dataframes, group_by, filter_by, labels, column, colors
    )
    # if no plot is passed in, create a new plot
    if not plot:
        f, plot = plt.subplots()

    # Create a scatter plot with all data
    for time, datapoints, color, label in zip(timestamp_groups, datapoint_groups, colors, labels):
        # plot.scatter(time, datapoints, label=label, color=color)
        plot.plot(time, datapoints, marker='o', linestyle='',markersize=0.75, label=label, color=color)
    plot.legend()
    # return a plot object to be displayed or modified
    return plot


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
#               plot_line
#
#   Returns a line plot based on the filters and grouping, applied to each
#   each gc_event_dataframes. Adds legends and labels to the plot as needed
#
def plot_line(
    gc_event_dataframes,
    group_by=None,
    filter_by=None,
    labels=None,
    colors=None,
    plot=None,
    column="Duration_miliseconds",
):
    timestamp_groups, datapoint_groups, labels, colors, _ = filter_and_group(
        gc_event_dataframes, group_by, filter_by, labels, column, colors
    )
    # if no plot is passed in, create a new plot
    if not plot:
        f, plot = plt.subplots()

    for time, datapoints, color, label in zip(timestamp_groups, datapoint_groups, colors, labels):
        plot.plot(time, datapoints, label=label, color=color)
    plot.legend()
    # Return a plot to be displayed or modified
    return plot


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
#       plot_pie_sum
#
#   Creates a pie chart based on the sum of values in 'column' in each 
#   gc_event_dataframe, based on the filters and groups 
#
def plot_pie_sum(
    gc_event_dataframes,
    group_by=None,
    filter_by=None,
    labels=None,
    colors=None,
    plot=None,
    column="Duration_miliseconds",
):
    timestamp_groups, datapoint_groups, labels, colors = filter_and_group(
        gc_event_dataframes, group_by, filter_by, labels, column, colors
    )
    # if no plot is passed in, create a new plot
    if not plot:
        f, plot = plt.subplots()

    # Calculate the size of each slice. Then, add the values to the label
    pie_slices_sizes = []
    for idx, datapoints in enumerate(datapoint_groups):
        pslice = sum(datapoints)
        pie_slices_sizes.append(slice)
        labels[idx] = labels[idx] + " : " + str(pslice)
    plot.pie(pie_slices_sizes, labels=labels, colors=colors, startangle=-40)
    plot.legend()
    return plot


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
#       plot_bar_sum
#
#   Plots a bar graph based on the sum of values found in 'column' for 
#   each gc_event_dataframe, based on the groupings and filters.
#
def plot_bar_sum(
    gc_event_dataframes,
    group_by=None,
    filter_by=None,
    labels=None,
    colors=None,
    plot=None,
    column="Duration_miliseconds",
):
    # Group and filter 
    timestamp_groups, datapoint_groups, labels, colors, alphas = filter_and_group(
        gc_event_dataframes, group_by, filter_by, labels, column, colors
    )
    # if no plot is passed in, create a new plot
    if not plot:
        f, plots = plt.subplots()

    # Add the values to the plot. Labels will have the value of the sum appended to the end
    for idx, (datapoints, color, label, alpha) in enumerate(zip(datapoint_groups, colors, labels, alphas)):
        barheight = sum(datapoints)
        plots.bar(idx, barheight, label=label + " : " + str(round(barheight, 4)), color=color, alpha=alpha)
    
    plots.set_xticks(range(len(datapoint_groups)))
    plots.set_xticklabels(labels)
    plots.legend()
    return plots


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
#       plot_bar_avg
#
#   Creates a bar graph with average values of from 'column' based on the
#   filters and grouping, and returns a plot.
#
def plot_bar_avg(
    gc_event_dataframes,# list of dataframes, containing gc event information. 
    group_by=None,      # A string to explain what groups to make within 1 log file
    filter_by=None,     # resitrctions on the data. list of tuples: (column, boolean-function)
    labels=None,        # list of str labels to describe each entry of gc_event_dataframes
    colors=None,        # A list of colors for the bars to be plotted as. 
    plot=None,          # A plot to add new plotted information to.
    column="Duration_miliseconds", # The column to find the averages of
):
    # Filter and group
    _, datapoint_groups, labels, colors, _ = filter_and_group(
        gc_event_dataframes, group_by, filter_by, labels, column, colors
    )
    # if no plot is passed in, create a new plot
    if not plot:
        f, plots = plt.subplots()

    for idx, (datapoints, color, label) in enumerate(zip(datapoint_groups, colors, labels)):
        barheight = sum(datapoints) / len(datapoints)
        plots.bar(idx, barheight, label=label + " : " + str(round(barheight, 4)), color=color)
    plots.set_xticks(range(len(datapoint_groups)))
    plots.set_xticklabels(labels)
    plots.legend()
    return plots


from src.graphing.trends import compare_trends


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
#
#       plot_trends
#
#   Create an ASCII table analyzing the breakdown of the number of events,
#   mean, standard deviation, total time, and maximum time
#
def plot_trends(
    gc_event_dataframes,# list of dataframes, containing gc event information. 
    group_by=None,      # A string to explain what groups to make within 1 log file
    filter_by=None,     # resitrctions on the data. list of tuples: (column, boolean-function)
    labels=None,        # list of str labels to describe each entry of gc_event_dataframes
    plot=None,          # unsued
    column="Duration_miliseconds", # Describes the column to find the percentiles of.
    throughput=False, # If true, then the throughput will be calculated from the gc_event_dataframe log info
):
    # Filter and group
    timestamp_groups, datapoint_groups, labels, _, __ = filter_and_group(
        gc_event_dataframes, group_by, filter_by, labels, column
    )
    # Create ASCII spreadsheet
    temporary_labels = []
    char_start = ord('A')
    print("Legend: ")
    for index, label in enumerate(labels):
        print(chr(char_start + index) + " | " + label)
        temporary_labels.append(chr(char_start + index))
    print("-" * 97)

    if throughput:
        compare_trends(datapoint_groups, labels=temporary_labels, lists_of_timestamps=timestamp_groups)
    else:
        compare_trends(datapoint_groups, labels=temporary_labels)
    

from src.graphing.percentiles import compare_pauses_percentiles


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
#
#       plot_percentiles
#
#   create an ASCII table with percentiles based on the provided filters & groupings
#
def plot_percentiles(
    gc_event_dataframes,# list of dataframes, containing gc event information. 
    group_by=None,      # A string to explain what groups to make within 1 log file
    filter_by=None,     # resitrctions on the data. list of tuples: (column, boolean-function)
    labels=None,        # list of str labels to describe each entry of gc_event_dataframes
    plot=None,          # unusued
    column="Duration_miliseconds", # Describes the column to find the percentiles of.
):
    timestamp_groups, datapoint_groups, labels, _, __ = filter_and_group(
        gc_event_dataframes, group_by, filter_by, labels, column
    )
    #### New ####
    temporary_labels = []
    char_start = ord('A')
    print("Legend (All timing in miliseconds) : ")
    for index, label in enumerate(labels):
        print(chr(char_start + index) + " | " + label)
        temporary_labels.append(chr(char_start + index))
    print("-" * 97)
    #### New ####

    compare_pauses_percentiles(datapoint_groups, labels=temporary_labels)
    # Since it is common for labels to get cut off, temporarily print them.

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
#
#       plot_reclaimed_bytes
#
#   Constructs a scatterplot showing the bytes reclaimed over time through gc events
#
def plot_reclaimed_bytes(
    gc_event_dataframes,
    group_by=None,  # A string to explain what groups to make within 1 log file
    filter_by=None, # resitrctions on the data. list of tuples: (column, boolean-function)
    labels=None,    # list of str labels to describe each entry of gc_event_dataframes
    plot=None,      # used if you would like to add this data to another plot
    column=None,    # overwritten manually 
):
    # if no plot is passed in, create a new plot
    if not plot:
        fig, plot = plt.subplots()

    # Access the beforeGC data
    timestamp_groups, datapoint_groups_before, _, colors, __ = filter_and_group(
        gc_event_dataframes, group_by, filter_by, labels, "HeapBeforeGC"
    )
    # Access the afterGC data
    timestamp_groups, datapoint_groups_after, _, _, _ = filter_and_group(
        gc_event_dataframes, group_by, filter_by, labels, "HeapAfterGC"
    )
    # Construct a table of "memory reclaimed" for each log, subtracting the before from after GC Heap allocation.
    reclaimed_bytes_groups = []
    for before_gc, after_gc in zip(datapoint_groups_before, datapoint_groups_after):
        reclaimed_bytes_groups.append([before - after for before, after in zip(before_gc, after_gc)])

    # Use the reclaimed_bytes_groups to plot the data
    for time, datapoints, color, label in zip(timestamp_groups, reclaimed_bytes_groups, colors, labels):
        plot.scatter(time, datapoints, label=label, color=color)
    plot.legend()

    # Return a plot to be displayed or modified
    return plot