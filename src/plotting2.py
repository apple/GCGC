from numpy import number
from src.filter_and_group import filter_and_group
from matplotlib import pyplot as plt
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

    # Group the data into groups.
    max_pause_duration = 0
    for dataset in datapoint_groups:
        max_pause_duration = max(dataset.max(), max_pause_duration)
    
    number_of_buckets = int((max_pause_duration) / interval_duration) + 1
    time_intervals = [[0 for m in range(len(datapoint_groups))] for idx in range(number_of_buckets)]

    # put the data into buckets
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
            for idx, value in enumerate(bucket):
                plot.bar(bucket_number + width * idx , value, width = width, color = colors[idx])
        else:
            for idx, value in enumerate(bucket):
                plot.bar(bucket_number + width * idx , value, width = width, color = colors[idx], label = labels[idx])
            labels_printed = True
    plot.set_xticks([num + width / 2 * len(datapoint_groups) - width / 2 for num in range(number_of_buckets)])
    plot.set_xticklabels([round(interval_duration * (b + 1),4 ) for b in range(number_of_buckets)])
    plot.legend()
    return plot

import numpy as np
# def plot_percentile_intervals(    gc_event_dataframes,
#     group_by=None,
#     filter_by=None,
#     labels=None,
#     colors=None,
#     plot=None,
#     column="Duration_miliseconds",
#     interval_duration = 0,
#     percentiles = [50, 90, 99.99]
#     ):
#     if not interval_duration:
#         print("No interval length provided. Abort.")
#         return

#     timestamp_groups, datapoint_groups, labels, colors, _ = filter_and_group(
#         gc_event_dataframes, group_by, filter_by, labels, column, colors
#     )
    
#     # if no plot is passed in, create a new plot
#     if not plot:
#         f, plot = plt.subplots()
    
#     max_pause_duration = 0 #

#     for dataset in datapoint_groups:
#         max_pause_duration = max(dataset.max(), max_pause_duration)
    
#     number_of_buckets = int((max_pause_duration) / interval_duration) + 1

#     for dataset in datapoint_groups:
#         # Put the values into buckets.
#         buckets = [[] for idx in range(number_of_buckets)]
#         for value in dataset:
#             bucket_number = int(value / interval_duration)
#             buckets[bucket_number].append(value)

        
#         bucket_percentiles = [[[] for p in percentiles] for idx in range(number_of_buckets)]
#         for idx, bucket in enumerate(buckets):
#             for p_idx, percentile in enumerate(percentiles):
#                 bucket_percentiles[idx][p_idx] = np.percentile(bucket, percentile)

                
                

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

def get_percentile(bucket, percentiles):
    computed_percentiles = []
    for percentile in percentiles:
        computed_percentiles.append(np.percentile(bucket, percentile))
    return computed_percentiles  

def map_get_percentiles(buckets, percentiles):
    buckets_of_percentiles = []
    for bucket in buckets:
        buckets_of_percentiles.append(get_percentile(bucket, percentiles))
    return buckets_of_percentiles

#   TODO: Documentation. Requested by Bernd. Buckets percentiles
#
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
    # if not interval_duration:
    #     print("No interval length provided. Abort.")
    #     return

    timestamp_groups, datapoint_groups, labels, colors, _ = filter_and_group(
        gc_event_dataframes, group_by, filter_by, labels, column, colors
    )
    
    # # if no plot is passed in, create a new plot
    if not plot:
        f, plot = plt.subplots()
    max_pause_duration = 0 #

    for timestamp in timestamp_groups:
        max_pause_duration = max(timestamp.max(), max_pause_duration)
    
    number_of_buckets = int((max_pause_duration) / interval_duration) + 1
    x_data = list(range(number_of_buckets))
    for INDEX, (timestamps, dataset) in enumerate(zip(timestamp_groups, datapoint_groups)):
        # First, group into buckets based on time interverals.
        buckets = group_into_buckets(timestamps, dataset, number_of_buckets, interval_duration)
        buckets_of_percentiles = map_get_percentiles(buckets, percentiles)
        
        
        single_line = [buckets_of_percentiles[i][0] for i in range(len(buckets_of_percentiles))] 
        plot.plot(x_data, single_line, label = labels[INDEX], color = colors [INDEX])
        for idx in range(1, len(percentiles)):
            
            single_line = [buckets_of_percentiles[i][idx] for i in range(len(buckets_of_percentiles))]

            plot.plot(x_data, single_line, color = colors [INDEX], alpha = 1 - 0.15 * idx )
    plot.legend()
    plot.set_xticks(x_data)
    plot.set_xticklabels([(val + 1) *interval_duration for val in x_data ])    
    return plot
            
        
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
        gc_event_dataframes, group_by, filter_by, labels, column, colors
    )
    
    # # if no plot is passed in, create a new plot
    if not plot:
        f, plot = plt.subplots()
    max_pause_duration = 0 #

    for timestamp in timestamp_groups:
        max_pause_duration = max(timestamp.max(), max_pause_duration)
    

    number_of_buckets = int((max_pause_duration) / interval_duration) + 1
    x_data = list(range(number_of_buckets))
    
    for INDEX, (timestamps, dataset) in enumerate(zip(timestamp_groups, datapoint_groups)):
        # First, group into buckets based on time interverals.
        buckets = group_into_buckets(timestamps, dataset, number_of_buckets, interval_duration)
        frequency = [len(bucket) for bucket in buckets]
        plot.plot(x_data, frequency, label = labels[INDEX], color = colors [INDEX])
        
    plot.legend()
    plot.set_xticks(x_data)
    plot.set_xticklabels([(val + 1) *interval_duration for val in x_data ])    
    return plot

def plot_max_pause_intervals(
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
        gc_event_dataframes, group_by, filter_by, labels, column, colors
    )
    
    # # if no plot is passed in, create a new plot
    if not plot:
        f, plot = plt.subplots()
    max_pause_duration = 0 #

    for timestamp in timestamp_groups:
        max_pause_duration = max(timestamp.max(), max_pause_duration)
    

    number_of_buckets = int((max_pause_duration) / interval_duration) + 1
    x_data = list(range(number_of_buckets))
    
    for INDEX, (timestamps, dataset) in enumerate(zip(timestamp_groups, datapoint_groups)):
        # First, group into buckets based on time interverals.
        buckets = group_into_buckets(timestamps, dataset, number_of_buckets, interval_duration)
        maximums = [max(bucket) for bucket in buckets]
        plot.plot(x_data, maximums, label = labels[INDEX], color = colors [INDEX])
        
    plot.legend()
    plot.set_xticks(x_data)
    plot.set_xticklabels([(val + 1) *interval_duration for val in x_data ])
    return plot

