# transform_data.py
""" Take data and selectively return or parse sections of the data.
    Remove extra characters or add them. Does not change any values"""
# Ellis Brown
# 6/15/2021
import numpy as np
import pandas as pd  # implicit. TODO: check if this is needed
import math
import re

# Access a Pandas dataframe constructed through parse_data.py with labeled columns.
# Return the timestamps and pauses as a list
def get_combined_xy_pauses(dataframe, to_list=True):
    if dataframe.empty:
        print("Warning: Empty dataframe")
        return [], []
    else:
        if to_list:
            time_in_seconds = list(dataframe["TimeFromStart_seconds"])
            pauses_in_ms = list(dataframe["PauseDuration_miliseconds"])
        else:
            time_in_seconds = dataframe["TimeFromStart_seconds"]
            pauses_in_ms = dataframe["PauseDuration_miliseconds"]
        return time_in_seconds, pauses_in_ms


def remove_last_character(line):
    return line[:-1]


def get_time_in_seconds(dataframe, to_list=True):
    if dataframe.empty:
        return []
    else:
        if to_list:
            return list(dataframe["TimeFromStart_seconds"])
        return dataframe["TimeFromStart_seconds"]


def get_pauses_in_miliseconds(dataframe, to_list=True):
    if dataframe.empty:
        return []
    else:
        if to_list:
            return list(dataframe["PauseDuration_miliseconds"])
        return dataframe["PauseDuration_miliseconds"]


# Group all pauses & time data into N evenly distributed buckets, based on time
def get_sum_pauses_n_buckets(timestamps, pausedata, num_buckets):
    max_time = timestamps[-1]
    duration = max_time / num_buckets
    return __put_into_buckets(timestamps, pausedata, duration, num_buckets, sum)


# Group all pasue & time data into some number of buckets with a given bucket duration
def get_sum_pauses_n_duration(timestamps, pausedata, duration):
    max_time = timestamps[-1]
    num_buckets = max_time / duration
    return __put_into_buckets(timestamps, pausedata, duration, num_buckets, sum)


# Get the max pause in a specified duration, such that there are n buckets
def get_max_pauses_n_buckets(timestamps, pausedata, num_buckets):
    max_time = timestamps[-1]
    duration = max_time / num_buckets
    return __put_into_buckets(timestamps, pausedata, duration, num_buckets, max)


# Get the max pauses over buckets of n duration length
def get_max_pauses_n_duration(timestamps, pausedata, duration):
    max_time = timestamps[-1]
    num_buckets = max_time / duration
    return __put_into_buckets(timestamps, pausedata, duration, num_buckets, max)


def __put_into_buckets(timestamps, pausedata, duration, num_buckets, grouping_method):
    num_buckets = math.ceil(num_buckets)

    buckets = [[] for i in range(num_buckets)]
    times = [duration * i for i in range(1, num_buckets + 1)]

    # First, sort all values into buckets based on the timestamp.
    for time, pause in zip(timestamps, pausedata):
        index_of_bucket = int(time / duration)
        if index_of_bucket >= num_buckets:
            index_of_bucket = num_buckets - 1
        buckets[index_of_bucket].append(pause)

    for idx in range(len(buckets)):
        if buckets[idx]:
            buckets[idx] = grouping_method(buckets[idx])
        else:  # untested else case. TODO.
            buckets[idx] = 0

    return times, buckets


# Given lists of multiple pauses / stops, compare the runtime of the data.
def compare_max_pauses_n_duration(xdata_lists, ydata_lists, duration):
    xdata_bucketed_lists = []
    ydata_bucketed_lists = []
    for i in range(len(xdata_lists)):
        xdata, ydata = get_max_pauses_n_duration(xdata_lists[i], ydata_lists[i], duration)
        xdata_bucketed_lists.append(xdata)
        ydata_bucketed_lists.append(ydata)
    return xdata_bucketed_lists, ydata_bucketed_lists


def compare_max_pauses_n_buckets(xdata_lists, ydata_lists, num_buckets):
    # Get the correct duration for a bucket to be applied to all data
    max_pause = 0
    for datalist in xdata_lists:
        max_p = max(datalist)
        max_pause = max(max_p, max_pause)
    duration = math.ceil(max_pause / num_buckets)
    # Gather the data using a constant duration and return
    xdata_bucketed_lists = []
    ydata_bucketed_lists = []
    for i in range(len(xdata_lists)):
        xdata, ydata = get_max_pauses_n_duration(xdata_lists[i], ydata_lists[i], duration)
        xdata_bucketed_lists.append(xdata)
        ydata_bucketed_lists.append(ydata)
    return xdata_bucketed_lists, ydata_bucketed_lists


def compare_sum_pauses_n_duration(xdata_lists, ydata_lists, duration):
    xdata_bucketed_lists = []
    ydata_bucketed_lists = []
    for i in range(len(xdata_lists)):
        xdata, ydata = get_sum_pauses_n_duration(xdata_lists[i], ydata_lists[i], duration)
        xdata_bucketed_lists.append(xdata)
        ydata_bucketed_lists.append(ydata)
    return xdata_bucketed_lists, ydata_bucketed_lists


def compare_sum_pauses_n_buckets(xdata_lists, ydata_lists, num_buckets):
    # Get the correct duration for a bucket to be applied to all data
    max_pause = 0
    for datalist in xdata_lists:
        max_p = max(datalist)
        max_pause = max(max_p, max_pause)
    duration = math.ceil(max_pause / num_buckets)
    # Gather the data using a constant duration and return
    xdata_bucketed_lists = []
    ydata_bucketed_lists = []
    for i in range(len(xdata_lists)):
        xdata, ydata = get_sum_pauses_n_duration(xdata_lists[i], ydata_lists[i], duration)
        xdata_bucketed_lists.append(xdata)
        ydata_bucketed_lists.append(ydata)
    return xdata_bucketed_lists, ydata_bucketed_lists


# Make a heatmap from given parameters. Recommended: Use default or change default for ALL runs.
def get_heatmap_data(
    table,
    x_bucket_count=20,
    y_bucket_count=20,
    x_bucket_duration=100,
    y_bucket_duration=10,
    suppress_warnings=False,
):

    if table.empty:
        print("Empty table in get_heatmap_data")
        return
    times_seconds, pauses_ms = get_combined_xy_pauses(table)

    # create buckets to store the time information.
    # first, compress into num_b buckets along the time X-axis.
    x_b = [[] for i in range(x_bucket_count)]

    # populate buckets along the x axis.
    for pause, time in zip(pauses_ms, times_seconds):
        bucket_no = int(time / x_bucket_duration)
        if not suppress_warnings:
            if bucket_no >= (x_bucket_count + 1):

                print(
                    "Warning: Time recorded lies outside of specified time range: "
                    + str(time)
                    + " > "
                    + str(x_bucket_count * x_bucket_duration)
                )
        if bucket_no >= x_bucket_count:
            bucket_no = x_bucket_count - 1
        x_b[bucket_no].append(pause)

    max_pause_ms = max(pauses_ms)
    min_pause_ms = min(pauses_ms)
    # create heatmap, which will be a 2d-array
    heatmap = []

    # go through each time interval, and sort the pauses there into frequency lists
    for bucket in x_b:
        yb = [0 for i in range(y_bucket_count)]  # construct a 0 frequency list
        for time in bucket:
            # determine which ms pause bucket
            y_bucket_no = int(time / y_bucket_duration)
            if not suppress_warnings:
                if y_bucket_no >= y_bucket_count + 1:
                    print(
                        "Warning: Value for latency lies outside of range: "
                        + str(time)
                        + " > "
                        + str(y_bucket_count * y_bucket_duration)
                        + " ms"
                    )

            if y_bucket_no >= y_bucket_count:
                y_bucket_no = y_bucket_count - 1

            # increase the frequency of that pause in this time interval
            yb[y_bucket_no] += 1

        # Add the data to the 2d array
        heatmap.append(yb)
    heatmap = np.rot90(heatmap)  # fix orientation
    return np.array(heatmap), [
        x_bucket_count,
        y_bucket_count,
        x_bucket_duration,
        y_bucket_duration,
    ]


def get_heap_occupancy(dataframe):
    if dataframe.empty:
        print("Empty dataframe in get_heap_occupancy")
        return
    if "AdditionalNotes" in dataframe.columns:
        memory_change = list(dataframe["AdditionalNotes"])
    else:
        memory_change = list(dataframe["MemoryChange"])
    before_gc = []
    after_gc = []
    max_heap = []
    unit = None
    times = get_time_in_seconds(dataframe)
    parsed_timestamps = []

    regex_pattern_memory = "(\d+)(\w+)->(\d+)\w+\((\d+)\w+\)"
    #   String parses things in this pattern: 1234M->123M(9999M)
    # Capture pattern 1: Before
    # Capture pattern 2: unit
    # Capture pattern 3: After
    # Capture pattern 4: Current maximum heap size (can change... lol)
    for idx in range(len(memory_change)):
        if memory_change[idx]:
            match = re.search(regex_pattern_memory, memory_change[idx])
            if match:
                before_gc.append(int(match.group(1)))
                unit = match.group(2)
                after_gc.append(int(match.group(3)))
                max_heap.append(int(match.group(4)))
                parsed_timestamps.append(times[idx])

            else:
                print("Warning: Unable to parse this memory_change[idx]: " + memory_change[idx])
                # final return value is the unit as a string
    return before_gc, after_gc, max_heap, unit, parsed_timestamps


# TODO: documentation
# Remove every other value from an array. The offset is either 1 or 0 to show if removing first or second value.
def remove_every_other(arr, offset):
    half_arr = []
    for i in range(len(arr)):
        if (i + offset) % 2:
            half_arr.append(arr[i])
    return half_arr


# Removes all data from a log file after a specified timestamp
def setMaxTime(df, maxtime):
    times = get_time_in_seconds(df)
    cutoff = -1
    for i in range(len(times)):
        if times[i] > maxtime:
            cutoff = i
            break
    if cutoff != -1:
        to_cut = [idx for idx in range(cutoff, len(times))]
        df.drop(to_cut, inplace=True)
