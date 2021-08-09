# The max allocation rate is defined as the difference bewtween the heap usage at GC event A and event A+1.
# To find it, given a list of data, find the difference between values in "column"
from filter_and_group import filter_and_group
from matplotlib import pyplot as plt

def difference_in_entries(
    gc_event_dataframes,  # list of dataframes, containing gc event information. 
    group_by=None,  # A string to explain what groups to make within 1 gc_event_dataframe
    filter_by=None, # resitrctions on the data. list of tuples: (column, boolean-function) 
    labels=None,    # list of str labels to describe each gc_event_dataframe.  
    interval_seconds=None,
    colors=None,    # colors to override 
    plot=None,
    column_before="HeapBeforeGC",
    column_after= "HeapAfterGC",
    column_timing = None,
    percentile = None,
    line_graph = False
):  
# Filter and group data. Update colors and labels to reflect to-be-plotted data
    timestamp_groups, before_list, labels, colors, _ = filter_and_group(
        gc_event_dataframes, group_by, filter_by, labels, column_before, colors, column_timing
    )
    timestamp_groups, after_list, labels, colors, _ = filter_and_group(
        gc_event_dataframes, group_by, filter_by, labels, column_after, colors, column_timing
    )

    # if no plot is passed in, create a new plot
    if not plot:
        f, plot = plt.subplots()
    # Create a scatter plot with all data
    if len(before_list) > len(labels):
        print("Not enough labels to plot")
    if len(after_list) > len(colors):
        print("Not enough colors to plot")
    for time, before_list, after_list, color, label in zip(timestamp_groups, before_list, after_list, colors, labels):
        time = list(time)
        start_times, datapoints = get_difference(list(before_list), list(after_list), time, interval_seconds, percentile)
        time.pop()
        if line_graph:
            plot.plot(start_times, datapoints, label=label, color=color)
        else:
            plot.scatter(start_times, datapoints,  label=label, color=color)
            
    plot.legend()
    # return a plot object to be displayed or modified
    return plot

def get_difference(before_list, after_list, time, interval_seconds, percentile):
    times = []
    difference_list = []
    # https://plumbr.io/handbook/gc-tuning-in-practice/high-allocation-rate
    interval_start_time = time[0]
    allocated_bytes = 0
    if percentile is None or interval_seconds is None:
        for index in range(len(before_list) - 1):
            allocated_bytes += before_list[index + 1] - after_list[index] 
            elapsed_seconds = time[index + 1] - interval_start_time
            if (interval_seconds is None or elapsed_seconds >= interval_seconds):
                difference_list.append(allocated_bytes / elapsed_seconds)
                times.append(time[index])
                allocated_bytes = 0
                interval_start_time = time[index + 1]
        return times, difference_list
    else:
        import numpy as np
        allocated_bytes_rate= []
        percentile_array = []
        # Create a list of all allocation rates within a time interval.
        # Then, take the percentile from that list
        for index in range( len(before_list) - 1):
            allocated_bytes_rate.append((before_list[index + 1] - after_list[index]) / (time[index + 1] - time[index]))
            elapsed_seconds = time[index + 1] - interval_start_time
            if (elapsed_seconds >= interval_seconds):
                times.append(time[index]) # Set the timestamp for this time interval
                percentile_array.append(np.percentile(allocated_bytes_rate, percentile)) 
                interval_start_time = time[index + 1]
                allocated_bytes_rate = []
        return times, percentile_array
    
