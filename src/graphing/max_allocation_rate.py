# The max allocation rate is defined as the difference bewtween the heap usage at GC event A and event A+1.
# To find it, given a list of data, find the difference between values in "column"
from numpy import diff
from filter_and_group import filter_and_group
from matplotlib import pyplot as plt
def difference_in_entries(
    gc_event_dataframes,  # list of dataframes, containing gc event information. 
    group_by=None,  # A string to explain what groups to make within 1 gc_event_dataframe
    filter_by=None, # resitrctions on the data. list of tuples: (column, boolean-function) 
    labels=None,    # list of str labels to describe each gc_event_dataframe.  
    colors=None,    # colors to override 
    plot=None,
    column_before="HeapBeforeGC",
    column_after= "HeapAfterGC",
    column_timing = None,
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
        datapoints = get_difference(list(before_list), list(after_list))
        time = list(time)
        time.pop()
        if line_graph:
            plot.plot(time, datapoints, label=label, color=color)
        else:
            plot.scatter(time, datapoints,  label=label, color=color)
    plot.legend()
    # return a plot object to be displayed or modified
    return plot

def get_difference(before_list, after_list):
    difference_list = []
    # https://plumbr.io/handbook/gc-tuning-in-practice/high-allocation-rate
    for index in range(len(before_list) - 1):
        difference_list.append(before_list[index + 1] - after_list[index] )
    return difference_list