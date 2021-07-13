#   plotting2.py
#
#   Plotting functions handling gc_event_dataframes and filtering. A temporary 
#   extension of plotting.py, dividied off into its own file for development purposes.
#
#   7/8/2021
from src.filter_and_group import filter_and_group
from matplotlib import pyplot as plt
import numpy as np # Used in percentile calculation

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
    column="Duration_miliseconds",
    interval_duration = 0
):
    if not interval_duration:
        print("No interval length provided. Abort.")
        return

    _, datapoint_groups, labels, colors, _ = filter_and_group(
        gc_event_dataframes, group_by, filter_by, labels, column, colors
    )
    
    # if no plot is passed in, create a new plot
    if not plot:
        f, plot = plt.subplots()

    # Determine the number of buckets from max_time and interval duration
    max_pause_duration = 0
    for dataset in datapoint_groups:
        max_pause_duration = max(dataset.max(), max_pause_duration)
    number_of_buckets = int((max_pause_duration) / interval_duration) + 1
    
    # Create the time intervals 
    time_intervals = [[0 for m in range(len(datapoint_groups))] for idx in range(number_of_buckets)]

    # put the data into buckets, creating a frequency plot for each bucket
    for idx, dataset in enumerate(datapoint_groups):
        for value in dataset:
            bucket_number = int(value / interval_duration)
            time_intervals[bucket_number][idx] += 1
    
    # time_intervals is a 2d array, with index representing a bucket.
    # PLot.
    width = 0.8 / len(datapoint_groups)
    labels_printed = False
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
    plot.set_xticks([num + width / 2 * len(datapoint_groups) - width / 2 for num in range(number_of_buckets)])
    plot.set_xticklabels([round(interval_duration * (b + 1),4 ) for b in range(number_of_buckets)])
    plot.legend()
    return plot

                
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
    column="Duration_miliseconds",
    interval_duration = 0,
    percentiles = [99.99, 90, 50]
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
                                                                             colors)
    
    # # if no plot is passed in, create a new plot
    if not plot:
        f, plot = plt.subplots()
    
    # Determine the longest pause to calculate the number of intervalsm
    max_pause_duration = 0 
    for timestamp in timestamp_groups:
        max_pause_duration = max(timestamp.max(), max_pause_duration)
    number_of_buckets = int((max_pause_duration) / interval_duration) + 1
    
    # Determine the spacing along the X axis for the data
    x_alignment = list(range(number_of_buckets))
    
    # For each group, determine the percentile, and plot an independent line for that percentile
    for group, (timestamps, dataset) in enumerate(zip(timestamp_groups, datapoint_groups)):
        
        # First, group into buckets based on time interverals.
        buckets = group_into_buckets(timestamps, dataset, number_of_buckets, interval_duration)
        buckets_of_percentiles = map_get_percentiles(buckets, percentiles)
        
        # Collect the percentiles for the i-th group, percentile 0.
        single_line = [buckets_of_percentiles[i][0] for i in range(len(buckets_of_percentiles))] 
        
        # Plot the first line based on the first percentile, with a label
        plot.plot(x_alignment, single_line, label = labels[group], color = colors[group])
        
        # Plot the rest of the percentiles, with decreasing alpha (opacity) values per line
        for idx in range(1, len(percentiles)):
            single_line = [buckets_of_percentiles[i][idx] for i in range(len(buckets_of_percentiles))]
            plot.plot(x_alignment, single_line, color = colors [group], alpha = 1 - 0.15 * idx )
    
    # Add styling to the plot. Add legend, and x axis correct titles
    plot.legend()
    plot.set_xticks(x_alignment)
    plot.set_xticklabels([(val + 1) *interval_duration for val in x_alignment ])    
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
    column="Duration_miliseconds",
    interval_duration = 0,
    ):
    if not interval_duration:
        print("No interval length provided. Abort.")
        return
    timestamp_groups, datapoint_groups, labels, colors, _ = filter_and_group(
        gc_event_dataframes, group_by, filter_by, labels, column, colors)
    
    # # if no plot is passed in, create a new plot
    if not plot:
        f, plot = plt.subplots()

    # Determine the longest pause to calculate the number of intervals
    max_pause_duration = 0 #
    for timestamp in timestamp_groups:
        max_pause_duration = max(timestamp.max(), max_pause_duration)
    number_of_buckets = int((max_pause_duration) / interval_duration) + 1
    
    # Determine the spacing along the X axis for the data
    x_alignment = list(range(number_of_buckets))
    
    # Create a list of frequencies, one for each group, and plot that line
    for index, (timestamps, dataset) in enumerate(zip(timestamp_groups, datapoint_groups)):
        # First, group into buckets based on time interverals.
        buckets = group_into_buckets(timestamps, dataset, number_of_buckets, interval_duration)
        # Calculate the frequency of gc events per bucket time interval. Then plot
        frequency = [len(bucket) for bucket in buckets]
        plot.plot(x_alignment, frequency, label = labels[index], color = colors[index])
    
    # Add styling to the plot. Add legend, and correct x-axis labels
    plot.legend()
    plot.set_xticks(x_alignment)
    plot.set_xticklabels([(val + 1) *interval_duration for val in x_alignment ])    
    return plot




#       plot_sum_pause_intervals
#
#   Given a list of gc_event_dataframes, and groupings and filters,
#   plot the sum of all pauses in a provided interval in miliseconds,
#   for each resulting group.
#
#
def plot_sum_pause_intervals(
    gc_event_dataframes,
    group_by=None,
    filter_by=None,
    labels=None,
    colors=None,
    plot=None,
    column="Duration_miliseconds",
    interval_duration = 0, # miliseconds
    ):
    if not interval_duration:
        print("No interval length provided. Abort.")
        return

    # Filter and group data
    timestamp_groups, datapoint_groups, labels, colors, _ = filter_and_group(
        gc_event_dataframes, group_by, filter_by, labels, column, colors
    )
    
    # if no plot is passed in, create a new plot
    if not plot:
        f, plot = plt.subplots()
    
    # Determine the longest pause to calculate the number of intervals
    max_pause_duration = 0 #
    for timestamp in timestamp_groups:
        max_pause_duration = max(timestamp.max(), max_pause_duration)
    number_of_buckets = int((max_pause_duration) / interval_duration) + 1
    
    # Determine the spacing along the X axis for the data
    x_alignment = list(range(number_of_buckets))
    
    # Loop through all lists, and plot the line graphs 
    for index, (timestamps, dataset) in enumerate(zip(timestamp_groups, datapoint_groups)):
        # First, group into buckets based on time interverals.
        buckets = group_into_buckets(timestamps, dataset, number_of_buckets, interval_duration)
        # Calculate the sum in each bucket, to then plot
        sums = [sum(bucket) for bucket in buckets]
        plot.plot(x_alignment, sums, label = labels[index], color = colors[index])

    # Set the labels for the buckets, starting with a non-zero bucket    
    plot.legend()
    plot.set_xticks(x_alignment)
    plot.set_xticklabels([(val + 1) *interval_duration for val in x_alignment ])
    return plot