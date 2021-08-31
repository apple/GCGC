#      plotting.py
#
#   Defines functions to create plots based on filters and groupings, and a list of 
#   gc_event_dataframes. Each function returns or creates a plot or ASCII table.

import matplotlib.pyplot as plt
from filter_and_group import filter_and_group
from os import times
from matplotlib import pyplot as plt
import numpy as np # Used in percentile calculation


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
    column="Duration_milliseconds",
    column_timing = None,
):  
    # Filter and group data. Update colors and labels to reflect to-be-plotted data
    timestamp_groups, datapoint_groups, labels, colors, _ = filter_and_group(
        gc_event_dataframes, group_by, filter_by, labels, column, colors, column_timing
    )
    # if no plot is passed in, create a new plot
    if not plot:
        f, plot = plt.subplots()
    # Create a scatter plot with all data
    if len(datapoint_groups) > len(labels):
        print("Not enough labels to plot")
    if len(datapoint_groups) > len(colors):
        print("Not enough colors to plot")
    for time, datapoints, color, label in zip(timestamp_groups, datapoint_groups, colors, labels):
        plot.plot(time, datapoints, marker='o', linestyle='',markersize=3, label=label, color=color)

    # return a plot object to be displayed or modified
    plot.legend(bbox_to_anchor=(1.05, 1), loc="upper left")
    

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
    column="Duration_milliseconds",
    column_timing = None
):
    timestamp_groups, datapoint_groups, labels, colors, _ = filter_and_group(
        gc_event_dataframes, group_by, filter_by, labels, column, colors, column_timing
    )
    # if no plot is passed in, create a new plot
    if not plot:
        f, plot = plt.subplots()
    if len(datapoint_groups) > len(labels):
        print("Not enough labels to plot")
    if len(datapoint_groups) > len(colors):
        print("Not enough colors to plot")
    for time, datapoints, color, label in zip(timestamp_groups, datapoint_groups, colors, labels):
        plot.plot(time, datapoints, label=label, color=color)
    plot.legend(bbox_to_anchor=(1.05, 1), loc="upper left")
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
    column="Duration_milliseconds",
    column_timing = None,
):
    timestamp_groups, datapoint_groups, labels, colors = filter_and_group(
        gc_event_dataframes, group_by, filter_by, labels, column, colors, column_timing
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
    plot.legend(bbox_to_anchor=(1.05, 1), loc="upper left")
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
    column="Duration_milliseconds",
    column_timing = None,
):
    # Group and filter 
    timestamp_groups, datapoint_groups, labels, colors, alphas = filter_and_group(
        gc_event_dataframes, group_by, filter_by, labels, column, colors, column_timing
    )
    # if no plot is passed in, create a new plot
    if not plot:
        f, plot = plt.subplots()
    if len(datapoint_groups) > len(labels):
        print("Not enough labels to plot")
    if len(datapoint_groups) > len(colors):
        print("Not enough colors to plot")
    # Add the values to the plot. Labels will have the value of the sum appended to the end
    for idx, (datapoints, color, label, alpha) in enumerate(zip(datapoint_groups, colors, labels, alphas)):
        barheight = sum(datapoints)
        plot.bar(idx, barheight, label=label + " : " + str(round(barheight, 4)), color=color, alpha=alpha)
    
    plot.set_xticks(range(len(datapoint_groups)))
    plot.set_xticklabels(labels)
    plot.legend(bbox_to_anchor=(1.05, 1), loc="upper left")
    return plot


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
    column="Duration_milliseconds", # The column to find the averages of
    column_timing = None,
):
    # Filter and group
    _, datapoint_groups, labels, colors, _ = filter_and_group(
        gc_event_dataframes, group_by, filter_by, labels, column, colors, column_timing
    )
    # if no plot is passed in, create a new plot
    if not plot:
        f, plot = plt.subplots()
    if len(datapoint_groups) > len(labels):
        print("Not enough labels to plot")
    if len(datapoint_groups) > len(colors):
        print("Not enough colors to plot")
    for idx, (datapoints, color, label) in enumerate(zip(datapoint_groups, colors, labels)):
        barheight = sum(datapoints) / len(datapoints)
        plot.bar(idx, barheight, label=label + " : " + str(round(barheight, 4)), color=color)
    plot.set_xticks(range(len(datapoint_groups)))
    plot.set_xticklabels(labels)
    plot.legend(bbox_to_anchor=(1.05, 1), loc="upper left")
    return plot


from src.graphing.summary import compare_summary


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
#
#       plot_summary
#
#   Create an ASCII table analyzing the breakdown of the number of events,
#   mean, standard deviation, total time, and maximum time
#
def plot_summary(
    gc_event_dataframes,# list of dataframes, containing gc event information. 
    group_by=None,      # A string to explain what groups to make within 1 log file
    filter_by=None,     # resitrctions on the data. list of tuples: (column, boolean-function)
    labels=None,        # list of str labels to describe each entry of gc_event_dataframes
    column="Duration_milliseconds", # Describes the column to find the percentiles of.
    throughput=False, # If true, then the throughput will be calculated from the gc_event_dataframe log info
):
    # Filter and group
    timestamp_groups, datapoint_groups, labels, _, __ = filter_and_group(
        gc_event_dataframes, group_by, filter_by, labels, column
    )
    PRINTING_SPACE_COUNT = 15
    if not labels:
        return
    if max([len(label) for label in labels]) <= PRINTING_SPACE_COUNT:
        if throughput:
            compare_summary(datapoint_groups, labels=labels, lists_of_timestamps=timestamp_groups)
        else:
            compare_summary(datapoint_groups, labels=labels)
        return
    # Create ASCII spreadsheet
    temporary_labels = []
    char_start = ord('A')
    found = False # Used to make sure passed DFs have correct data
    
    index = 0
    while index < len(datapoint_groups):
        if list(datapoint_groups[index]):
            if not found:
                print("Legend: ")
            found = True
            print(chr(char_start + index) + " | " + labels[index])
            temporary_labels.append(chr(char_start + index))
            index += 1 
        else:
            datapoint_groups.pop(index)

    if found:
        print("-" * 97)

    if throughput:
        compare_summary(datapoint_groups, labels=temporary_labels, lists_of_timestamps=timestamp_groups)
    else:
        compare_summary(datapoint_groups, labels=temporary_labels)
    

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
    column="Duration_milliseconds", # Describes the column to find the percentiles of.
):
    timestamp_groups, datapoint_groups, labels, _, __ = filter_and_group(
        gc_event_dataframes, group_by, filter_by, labels, column
    )
    PRINTING_SPACE_COUNT = 3
    if not labels:
        return
    if max([len(label) for label in labels]) <= PRINTING_SPACE_COUNT:
        compare_pauses_percentiles(datapoint_groups, labels=labels)
        return


    temporary_labels = []
    char_start = ord('A')
    if len(timestamp_groups) > len(labels):
        print("Not enough labels to plot")
    print("Legend (All timing in milliseconds) : ")
    for index, label in enumerate(labels):
        print(chr(char_start + index) + " | " + label)
        temporary_labels.append(chr(char_start + index))

    print("-" * 97)

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
    column_timing = None,
    colors = None,
):
    # if no plot is passed in, create a new plot
    if not plot:
        fig, plot = plt.subplots()

    # Access the beforeGC data
    timestamp_groups, datapoint_groups_before, _, colors, __ = filter_and_group(
        gc_event_dataframes, group_by, filter_by, labels, "HeapBeforeGC", colors, column_timing
    )
    # Access the afterGC data
    timestamp_groups, datapoint_groups_after, _, _, _ = filter_and_group(
        gc_event_dataframes, group_by, filter_by, labels, "HeapAfterGC", colors, column_timing
    )
    # Construct a table of "memory reclaimed" for each log, subtracting the before from after GC Heap allocation.
    reclaimed_bytes_groups = []
    for before_gc, after_gc in zip(datapoint_groups_before, datapoint_groups_after):
        reclaimed_bytes_groups.append([before - after for before, after in zip(before_gc, after_gc)])

    # Use the reclaimed_bytes_groups to plot the data
    if len(timestamp_groups) > len(labels):
        print("Not enough labels to plot")
    if len(timestamp_groups) > len(colors):
        print("Not enough colors to plot")
    for time, datapoints, color, label in zip(timestamp_groups, reclaimed_bytes_groups, colors, labels):
        plot.scatter(time, datapoints, label=label, color=color)
    plot.legend(bbox_to_anchor=(1.05, 1), loc="upper left")

    # Return a plot to be displayed or modified
    return plot


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
#       plot_frequency_intervals
#
#   Creates a histogram of freqencies of pauses, with an individual bar for each
#   gc_event_dataframe, based on the filters and groups. 
#
def plot_frequency_intervals(
    gc_event_dataframes,
    group_by=None,
    filter_by=None,
    labels=None,
    colors=None,
    plot=None,
    column="Duration_milliseconds",
    interval_duration = 0,
    column_timing = None
):
    if not interval_duration:
        print("No interval length provided. Abort.")
        return

    _, datapoint_groups, labels, colors, _ = filter_and_group(
        gc_event_dataframes, group_by, filter_by, labels, column, colors, column_timing
    )
    if len(datapoint_groups) > len(colors):
        print("Not enough colors to plot")
    # if no plot is passed in, create a new plot
    if not plot:
        f, plot = plt.subplots()

    number_of_buckets, min_time_duration, max_time_duration = get_buckets_and_range(datapoint_groups,
                                                                                      interval_duration)
    # Create the time intervals 
    time_intervals = [[0 for m in range(len(datapoint_groups))] for idx in range(number_of_buckets)]
    # put the data into buckets, creating a frequency plot for each bucket
    for idx, dataset in enumerate(datapoint_groups):
        for value in dataset:
            bucket_number = int((value - min_time_duration) / interval_duration)
            time_intervals[bucket_number][idx] += 1
    
    # time_intervals is a 2d array, with index representing a bucket.
    # PLot.
    width = 0.8 / len(datapoint_groups)
    labels_printed = False
    #   The width and index are important to plotting the same ordered bars on the graph,
    #   that come from different data set, but are associated with the same X labels
    for bucket_number, bucket in enumerate(time_intervals):
        if labels_printed:
            # The first time each group is plotted, their labels must be set
            for idx, value in enumerate(bucket):
                plot.bar(bucket_number + width * idx , value, width = width, color = colors[idx])
        else:
            # After having their labels plotted the first time, groups dont need to anymore (or repetition in legend occurs)
            for idx, value in enumerate(bucket):
                plot.bar(bucket_number + width * idx , value, width = width, color = colors[idx], label = labels[idx])
            labels_printed = True

    # Add styling to plot. Correctly set x-axis labels, and show the legend
    # Set the ACTUAL x tick values
    plot.set_xticks([num + width / 2 * len(datapoint_groups) - width / 2 for num in range(number_of_buckets)])
    plot.set_xticklabels([round(interval_duration * (b + 1),4 ) for b in range(number_of_buckets)])
    
    # Choose a reasonable number of x ticks to display.
    xticks, xlabels = simplify_xtickslabels(plot.get_xticks(), plot.get_xticklabels(), 20)
    plot.set_xticks(xticks)
    plot.set_xticklabels(xlabels)
    plot.legend(bbox_to_anchor=(1.05, 1), loc="upper left")
    return plot


def simplify_xtickslabels(ticks, labels, max_ticks):
    original_tick_length = len(ticks)
    if original_tick_length < max_ticks:
        return ticks, labels
    # We need to trim the ticks. Choose the correct scaling factor to eliminate
    # to get the number optimally in the range.
    import math 
    divisor = math.ceil(original_tick_length / max_ticks)
    index = 0
    new_ticks = []
    new_tick_labels = []
    while index < original_tick_length:
        new_ticks.append(ticks[index])
        new_tick_labels.append(labels[index])
        index += divisor
    return new_ticks, new_tick_labels

#   (private function)
#
#       group_into_buckets
#
#   Given a time interval, and count of time intervals, sort data based on timestamps
#   into those time intervals, creating a bucket for each interval, and populating the
#   bucket with datapoints information for that interval. Return the list of buckets.
#
def group_into_buckets(timestamps, datapoints, num_time_intervals, interval_duration):
    buckets = [[] for idx in range(num_time_intervals)]

    # put the data into buckets z
    for time, datapoint in zip(timestamps, datapoints):
        bucket_number = int(time / interval_duration)
        buckets[bucket_number].append(datapoint)
    
    # Make sure empty buckets are filled with a zero value
    for idx in range(len(buckets)):
        if not buckets[idx]:
            buckets[idx].append(0)
    return buckets

#   (private function)
#
#       get_percentile 
#
#   Given a bucket, and a list of percentiles,
#   create an ordered list of all percentiles for values in that
#   bucket, in the same order of the percentiles. Return that float list
#
def get_percentile(bucket, percentiles):
    computed_percentiles = []
    for percentile in percentiles:
        computed_percentiles.append(np.percentile(bucket, percentile))
    return computed_percentiles  

#   (private function)
#
#       map_get_percentiles
#   
#   From a list of buckets and percentiles, determine the percentiles 
#   each of the provided functions
#
def map_get_percentiles(buckets, percentiles):
    buckets_of_percentiles = []
    for bucket in buckets:
        buckets_of_percentiles.append(get_percentile(bucket, percentiles))
    return buckets_of_percentiles



#       plot_percentile_intervals
#
#   Given a list of gc_event_dataframes, and a filter and grouping,
#   determine the percentiles of latencys in each time interval specified
#   by `interval_duration`, and then plot all percentiles for each group.
#
def plot_percentile_intervals(
    gc_event_dataframes,
    group_by=None,
    filter_by=None,
    labels=None,
    colors=None,
    plot=None,
    column="Duration_milliseconds",
    interval_duration = 0,
    percentiles = [99.99, 90, 50],
    column_timing = None,
    line_graph = False, 
    different_colors = None
    ):
    if not interval_duration:
        print("No interval length provided. Abort.")
        return

    # Filter and group, collecting colors and labels
    timestamp_groups, datapoint_groups, labels, colors, _ = filter_and_group(gc_event_dataframes, 
                                                                             group_by,
                                                                             filter_by, 
                                                                             labels, 
                                                                             column, 
                                                                             colors,
                                                                             column_timing)
    if not line_graph and different_colors == None:
        different_colors = True
    if different_colors:
        from filter_and_group import get_colors_and_alphas
        colors, _ = get_colors_and_alphas(len(colors) * len(percentiles))
    # # if no plot is passed in, create a new plot
    if not plot:
        f, plot = plt.subplots()
    
    number_of_buckets, min_time_duration, _ = get_buckets_and_range(timestamp_groups, interval_duration)
    # Determine the spacing along the X axis for the data
    x_alignment = [idx * interval_duration + min_time_duration for idx in range(number_of_buckets)]
    if len(timestamp_groups) > len(labels):
        print("Not enough labels to plot")
    if len(datapoint_groups) > len(colors):
        print("Not enough colors to plot")
    # For each group, determine the percentile, and plot an independent line for that percentile
    for group, (timestamps, dataset) in enumerate(zip(timestamp_groups, datapoint_groups)):
        
        # First, group into buckets based on time interverals.
        buckets = group_into_buckets([time - min_time_duration for time in timestamps], dataset, number_of_buckets, interval_duration)
        buckets_of_percentiles = map_get_percentiles(buckets, percentiles)
        
        # Collect the percentiles for the i-th group, percentile 0.
        single_line = [buckets_of_percentiles[i][0] for i in range(len(buckets_of_percentiles))] 
        
        # Plot the first line based on the first percentile, with a label
        if line_graph:
            plot.plot(x_alignment, single_line, label = labels[group], color = colors[group]) # changed 
        else:

            plot.scatter(x_alignment, single_line, label = labels[group], color = colors[group]) # changed 
        
        # Plot the rest of the percentiles, with decreasing alpha (opacity) values per line
        for idx in range(1, len(percentiles)):
            if different_colors:
                single_line = [buckets_of_percentiles[i][idx] for i in range(len(buckets_of_percentiles))]
                if line_graph:
                    plot.plot(x_alignment, single_line, color = colors [group + idx], alpha = 1 - 0.15 * idx )
                else:
                    plot.scatter(x_alignment, single_line, color = colors [group + idx ], alpha = 1 - 0.15 * idx ) 
            else:
                single_line = [buckets_of_percentiles[i][idx] for i in range(len(buckets_of_percentiles))]
                if line_graph:
                    plot.plot(x_alignment, single_line, color = colors [group], alpha = 1 - 0.15 * idx )
                else:
                    plot.scatter(x_alignment, single_line, color = colors [group], alpha = 1 - 0.15 * idx ) 
    
    # Add styling to the plot. Add legend, and x axis correct titles
    plot.legend(bbox_to_anchor=(1.05, 1), loc="upper left")
    return plot
        

#       plot_frequency_of_gc_intervals
# 
#   Given a list of gc_event_dataframes, and a filter and grouping, determine
#   the frequency of gc for each group, and plot a line for that group
#
def plot_frequency_of_gc_intervals(
    gc_event_dataframes,
    group_by=None,
    filter_by=None,
    labels=None,
    colors=None,
    plot=None,
    column="GCIndex", # Used to determine uniqueness of GC events
    interval_duration = 0,
    column_timing = None
    ):
    if not interval_duration:
        print("No interval length provided. Abort.")
        return
    timestamp_groups, datapoint_groups, labels, colors, _ = filter_and_group(
        gc_event_dataframes, group_by, filter_by, labels, column, colors, column_timing)
    # # if no plot is passed in, create a new plot
    if not plot:
        f, plot = plt.subplots()
    number_of_buckets, min_time_duration, _ = get_buckets_and_range(timestamp_groups, interval_duration)
    
    # Determine the spacing along the X axis for the data
    x_alignment = [idx * interval_duration + min_time_duration for idx in range(number_of_buckets)]
    if len(timestamp_groups) > len(labels):
        print("Not enough labels to plot")
    if len(datapoint_groups) > len(colors):
        print("Not enough colors to plot")
    # Create a list of frequencies, one for each group, and plot that line
    for index, (timestamps, dataset) in enumerate(zip(timestamp_groups, datapoint_groups)):
        # First, group into buckets based on time interverals.
        buckets = group_into_buckets([time - min_time_duration for time in timestamps], dataset, number_of_buckets, interval_duration)
        # Calculate the frequency of gc events per bucket time interval. Then plot
        frequency = [len(set(bucket)) for bucket in buckets] # Based on frequency of UNIQUE VALUES
        plot.plot(x_alignment, frequency, label = labels[index], color = colors[index])
    
    # Add styling to the plot. Add legend, and correct x-axis labels
    plot.legend(bbox_to_anchor=(1.05, 1), loc="upper left")
    return plot




#       plot_sum_pause_intervals
#
#   Given a list of gc_event_dataframes, and groupings and filters,
#   plot the sum of all pauses in a provided interval in milliseconds,
#   for each resulting group
#
def plot_sum_pause_intervals(
    gc_event_dataframes,
    group_by=None,
    filter_by=None,
    labels=None,
    colors=None,
    plot=None,
    column="Duration_milliseconds",
    interval_duration = 0, # milliseconds
    column_timing = None,
    remove_empty_intervals = False,
    line_graph = False
    ):
    return plot_using_intervals(gc_event_dataframes, group_by, filter_by, labels, colors, plot,
                                column, interval_duration, column_timing, remove_empty_intervals, line_graph)


def plot_heatmaps(
    gc_event_dataframes,
    dimensions = None,
    group_by=None,
    filter_by=None,
    labels=None,
    column="Duration_milliseconds",
    column_timing = None, 
    frequency_ticks = None
    ):
    from src.graphing.heatmap import get_heatmap_data, plot_heatmap
    timestamp_groups, datapoint_groups, labels, _, _ = filter_and_group(
        gc_event_dataframes, group_by, filter_by, labels, column, None, column_timing,
    )

    heatmap_list, dimensions = get_heatmap_data(timestamp_groups, datapoint_groups, labels, dimensions)
    for heatmap, label in zip(heatmap_list, labels):
        if heatmap.size != 0 and dimensions:
           graph = plot_heatmap(heatmap, dimensions, frequency_ticks) # Set the last value to TRUE to see labels of frequency
           graph.set_title("Latency during runtime: " +  label)

#       get_buckets_and_range
#
#   Given a list of data, and the interval duration, find the maximum and 
#   minimum values in the range, and return the number of buckets to fit
#   that range
#
def get_buckets_and_range(datapoint_groups, interval_duration):
    max_time_duration = 0    
    min_time_duration = datapoint_groups[0].iloc[0]

    for dataset in datapoint_groups:
        if list(dataset): # read as list to check for list legnth, rather than rely on pd.DataFrame.empty
            max_time_duration = max(dataset.max(), max_time_duration)
            min_time_duration = min(dataset.min(), min_time_duration)
    if interval_duration:
        number_of_buckets = int((max_time_duration - min_time_duration) / interval_duration) + 1
    else:
        number_of_buckets = 0
    return number_of_buckets, min_time_duration, max_time_duration




#       plot_sum_pause_intervals
#
#   Given a list of gc_event_dataframes, and groupings and filters,
#   plot the sum of all pauses in a provided interval in milliseconds,
#   for each resulting group.
#
#
def plot_using_intervals(
    gc_event_dataframes,
    group_by=None,
    filter_by=None,
    labels=None,
    colors=None,
    plot=None,
    column="Duration_milliseconds",
    interval_duration = 0, # milliseconds
    column_timing = None,
    remove_empty_intervals = False,
    plot_line = False,
    grouping_function = sum,
    ):
    if not interval_duration:
        print("No interval length provided. Abort.")
        return

    # Filter and group data
    timestamp_groups, datapoint_groups, labels, colors, _ = filter_and_group(
        gc_event_dataframes, group_by, filter_by, labels, column, colors, column_timing
    )
    
    # if no plot is passed in, create a new plot
    if not plot:
        f, plot = plt.subplots()
    
    # Determine the longest pause to calculate the number of intervals
    if not (timestamp_groups):
        return plot
    if not list(timestamp_groups[0]):
        return plot

    number_of_buckets, min_time_duration, max_time_duration = get_buckets_and_range(timestamp_groups, interval_duration)    
    # Determine the spacing along the X axis for the data
    x_alignment = [idx * interval_duration + min_time_duration for idx in range(number_of_buckets)]

    
    if len(timestamp_groups) > len(labels):
        print("Not enough labels to plot")
    if len(datapoint_groups) > len(colors):
        print("Not enough colors to plot")
    # Loop through all lists, and plot the line graphs 
    for index, (timestamps, dataset) in enumerate(zip(timestamp_groups, datapoint_groups)):
        # First, group into buckets based on time interverals.
        # print(dataset)

        # NOTE: here, we are subtracting the minimum time from everything to easily group them
        buckets = group_into_buckets([time - min_time_duration for time in timestamps], 
                                    dataset,
                                    number_of_buckets, 
                                    interval_duration)
        # Calculate the sum in each bucket, to then plot
        if remove_empty_intervals:
            x_alignment = [idx * interval_duration + min_time_duration for idx in range(number_of_buckets)]
            non_zero_buckets = []
            related_timestamps = []
            for idx, bucket in enumerate(buckets):
                if sum(bucket) != 0:
                    non_zero_buckets.append(bucket)
                    related_timestamps.append(x_alignment[idx])
            buckets = non_zero_buckets
            x_alignment = related_timestamps
            
        sums = [grouping_function(bucket) for bucket in buckets]
        if plot_line:
            plot.plot(x_alignment, sums, label = labels[index], color = colors[index])    
        else:
            plot.scatter(x_alignment, sums, label = labels[index], color = colors[index])

    # Set the labels for the buckets, starting with a non-zero bucket    
    plot.legend(bbox_to_anchor=(1.05, 1), loc="upper left")
    return plot

########
def plot_heatmaps_logarithmic(
    gc_event_dataframes,
    dimensions,
    group_by=None,
    filter_by=None,
    labels=None,
    colors=None,
    column="Duration_milliseconds",
    column_timing = None, 
    frequency_ticks = None,
    ):
    from src.graphing.heatmap import plot_heatmap_logarithmic, get_heatmap_data_logarithmic
    timestamp_groups, datapoint_groups, labels, colors, _ = filter_and_group(
        gc_event_dataframes, group_by, filter_by, labels, column, colors, column_timing,
    )
    heatmap_list, dimensions = get_heatmap_data_logarithmic(timestamp_groups, datapoint_groups, labels, dimensions)
    for heatmap, label in zip(heatmap_list, labels):
        if heatmap.size != 0 and dimensions:
            graph = plot_heatmap_logarithmic(heatmap, dimensions, frequency_ticks) # Set the last value to TRUE to see labels of frequency
            graph.set_title("Latency during runtime: " +  label)

def plot_percentages(
    gc_event_dataframes,  # list of dataframes, containing gc event information. 
    group_by=None,  # A string to explain what groups to make within 1 gc_event_dataframe
    filter_by=None, # resitrctions on the data. list of tuples: (column, boolean-function) 
    labels=None,    # list of str labels to describe each gc_event_dataframe.  
    colors=None,    # colors to override 
    plot=None,
    column="Duration_milliseconds",
    column_timing = None,
    maxes_list = None,
    line_graph = False
):  
    # Filter and group data. Update colors and labels to reflect to-be-plotted data
    timestamp_groups, datapoint_groups, labels, colors, _ = filter_and_group(
        gc_event_dataframes, group_by, filter_by, labels, column, colors, column_timing
    )
    # if no plot is passed in, create a new plot
    if not plot:
        f, plot = plt.subplots()
    # Create a scatter plot with all data
    if len(datapoint_groups) > len(labels):
        print("Not enough labels to plot")
    if len(datapoint_groups) > len(colors):
        print("Not enough colors to plot")
    if len(maxes_list) < len(datapoint_groups):
        print("Not enough max values for associated percentages to plot")
    for time, datapoints, maxv, color, label in zip(timestamp_groups, datapoint_groups, maxes_list, colors, labels):
        datapoints = get_percentages(datapoints, maxv)
        if line_graph:
            plot.plot(time, datapoints, label=label, color=color)
        else:
            plot.scatter(time, datapoints,  label=label, color=color)
    plot.legend(bbox_to_anchor=(1.05, 1), loc="upper left")
    # return a plot object to be displayed or modified
    return plot

def get_percentages(datalist, max_value):
    return [data / max_value * 100 for data in datalist]

#       allocation_rate
#
#   Calculates and reports the allocation rate during runtime from gc information.
#   Optional parameter: percentile: If used, then calculates the specified percentile 
#                       allocation rate. If left as None, finds the mean allocation rate.
#   Optional parameter: interval_duration: Groups collected data into ranges, then either
#                       finds the mean or a percentile based on above optional param.
#
def allocation_rate(
    gc_event_dataframes,  # list of dataframes, containing gc event information. 
    group_by=None,  # A string to explain what groups to make within 1 gc_event_dataframe
    filter_by=None, # resitrctions on the data. list of tuples: (column, boolean-function) 
    labels=None,    # list of str labels to describe each gc_event_dataframe.  
    interval_duration=None, # integer or float. Creates groups of this size to find alloc rate.
    colors=None,    # colors to override 
    plot=None, #    matplotlib ax to plot onto. If none provided, one is created
    column_before="HeapBeforeGC", # Column used as information before event
    column_after= "HeapAfterGC", # Column used to find information after event
    column_timing = None, # Timing information used for X axis. List of floats or ints
    percentile = None, #  If True, and interval_duration is not None, plots the percentile
    line_graph = False # Plots as a line graph rather than a scatter plot
):  
    from src.graphing.allocation_rate import calculate_allocation_rate
    return calculate_allocation_rate(gc_event_dataframes, group_by, filter_by, labels,
                                     interval_duration, colors, plot, column_before, column_after,
                                     column_timing, percentile, line_graph)


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
#       plot_scatter_universal
#
#   Plots a scatter plot based on the provided gc_event_dataframes, and filters.
#   Returns a plot object that can then be updated.
#
def plot_scatter_universal(
    gc_event_dataframes,  # list of dataframes, containing gc event information. 
    group_by=None,  # A string to explain what groups to make within 1 gc_event_dataframe
    filter_by=None, # resitrctions on the data. list of tuples: (column, boolean-function) 
    labels=None,    # list of str labels to describe each gc_event_dataframe.  
    colors=None,    # colors to override 
    plot=None,
    column="Duration_milliseconds",
    column_timing = None,
    interval_duration = None,
    grouping_function = None,
    include_timing_in_bucket = False,
    line_graph = False,
):  
    # Filter and group data. Update colors and labels to reflect to-be-plotted data
    timestamp_groups, datapoint_groups, labels, colors, _ = filter_and_group(
        gc_event_dataframes, group_by, filter_by, labels, column, colors, column_timing
    )
    # if no plot is passed in, create a new plot
    if not plot:
        f, plot = plt.subplots()
    # Create a scatter plot with all data
    if len(datapoint_groups) > len(labels):
        print("Not enough labels to plot")
    if len(datapoint_groups) > len(colors):
        print("Not enough colors to plot")
    
    
    
    if interval_duration:
        min_time, max_time = determine_extremes(timestamp_groups)
        bucket_count = get_bucket_count(min_time, max_time, interval_duration)
        
        for timestamp_list, datapoint_list, label, color in zip(timestamp_groups, datapoint_groups, labels, colors):
            print("Before population")
            buckets, bucket_timing = populate_buckets(bucket_count, timestamp_list, datapoint_list, 
                                    interval_duration, min_time, include_timing_in_bucket)
            print("After population")
            xdata, ydata = apply_grouping_function(buckets, bucket_timing, grouping_function, include_timing_in_bucket)   

            if line_graph:
                plot.plot(xdata, ydata, label=label, color=color)
            else:
                plot.scatter(xdata, ydata, label=label, color=color)
    else:
        for timestamp_list, datapoint_list, label, color in zip(timestamp_groups, datapoint_groups, labels, colors):
            
            xdata, ydata = apply_grouping_function(list(datapoint_list), list(timestamp_list), grouping_function, include_timing_in_bucket)   
            if line_graph:
                plot.plot(xdata, ydata, label=label, color=color)
            else:
                plot.scatter(xdata, ydata, label=label, color=color)
    plot.legend(bbox_to_anchor=(1.05, 1), loc="upper left")
    return plot 

########
#   
#       Given a lists of timestamp_lists, find the minimum and maximum
#       times in the provided range. Every timestamp_list in the passed lists
#       should be a pandas series.
#
def determine_extremes(timestamp_lists):
    # Requirement: It is expected that passed timestamp lists are
    # sorted, with the smallest values first. 

    min_time = max_time = timestamp_lists[0].iloc[0] # Access pandas series index 0 with iloc 
    for timestamp_list in timestamp_lists:
        min_time = min(min_time, timestamp_list.iloc[0]) # First element in timestamp_list
        max_time = max(max_time, timestamp_list.iloc[-1]) # Last element in timestamp_list
    return min_time, max_time

########
#
#       Determine the number of buckets for a range of data, based
#       on their interval_duration. Return the bucket count, rounded up.
#
def get_bucket_count(min_time, max_time, interval_duration):
    total_duration = max_time -  min_time 
    bucket_count = int(total_duration / interval_duration) + 1
    return bucket_count

#######
#       
#       Populate an array of interval buckets with values from 
#       the
#
def populate_buckets(bucket_count, timestamp_list, datapoint_list, 
                    interval_duration, min_time, include_timing_in_bucket):
    
    buckets = [[] for index in range(bucket_count)]
    if include_timing_in_bucket:
        timing_buckets = [[] for index in range(bucket_count)]
        for time in range(len(timestamp_list)):
            timing_buckets[int((time - min_time)/ interval_duration)].append(time)
    else:
        timing_buckets = [int(min_time + interval_duration * index + 1) for index in range(bucket_count)]
    for time, data in zip(timestamp_list, datapoint_list):
        bucket_idx = int((time - min_time) / interval_duration)
        buckets[bucket_idx].append(data)
    # check if any buckets are empty
    for idx in range(bucket_count):
        if len(buckets[idx]) == 0:
            buckets[idx] = [0]
    return buckets, timing_buckets
    
#######
#
#       Apply the grouping function to each bucket. If time has been
#       included in the grouping function, zip and apply on that as well.
#
def apply_grouping_function(buckets, timing_buckets, grouping_function, include_timing_in_bucket):
    output_xdata = []
    output_ydata = []
    for index in range(len(buckets)):
        if include_timing_in_bucket:
            x, y = grouping_function(buckets[index], timing_buckets[index])
        else:
            y = grouping_function(buckets[index])        
            x = timing_buckets[index]
        if type(x) == list:
            for xdata in x:
                output_xdata.append(xdata)
        else:
            output_xdata.append(x)
        if type(y) == list:
            for ydata in y:
                output_ydata.append(ydata)
        else:
            output_ydata.append(y)
        

    return output_xdata, output_ydata