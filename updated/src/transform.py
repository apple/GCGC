# transform_data.py
""" Take data and selectively return or parse sections of the data.
    Remove extra characters or add them. Does not change any values"""
# Ellis Brown
# 6/15/2021
import numpy as np
import pandas as pd  # implicit. TODO: check if this is needed
import math
import re

# Access a Pandas database_table constructed through parse_data.py with labeled columns.
# Return the timestamps and pauses as a list
def get_time_and_event_durations(database_table):
    return get_time_in_seconds(database_table), get_event_durations_in_miliseconds(database_table)


def get_event_durations_in_miliseconds(database_table):
    if database_table.empty:
        return []
    else:
        return list(map(float, database_table["Duration_miliseconds"]))


def get_time_in_seconds(database_table):
    if database_table.empty:
        return []
    else:
        return list(map(float, database_table["TimeFromStart_seconds"]))


# Given a list of tables,
# Extract the event timestamp and event durations from each
# And return a list of lists of all event timestamps, and all event durations
def get_times_and_durations_from_event_lists(event_tables):
    xdatas_list = []
    ydatas_list = []
    for event_table in event_tables:
        xdata, ydata = get_time_and_event_durations(event_table)
        xdatas_list.append(xdata)
        ydatas_list.append(ydata)
    return xdatas_list, ydatas_list


def get_event_table_labels(event_tables, eventtype=True):

    if eventtype:
        return [
            event_tables[i]["EventType"].iloc[0] + " " + event_tables[i]["EventName"].iloc[0]
            for i in range(len(event_tables))
        ]
    else:
        return [event_tables[i]["EventName"].iloc[0] for i in range(len(event_tables))]


def compare_eventtype_time(event_table):
    concurrent = getConcurrentData(event_table)
    concurrent_total_time = sum(get_event_durations_in_miliseconds(concurrent))

    stw = getPausesData(event_table)
    stw_total_time = sum(get_event_durations_in_miliseconds(stw))
    return stw_total_time, concurrent_total_time


########
# Given a populated pandas database_table, find all rows that specify
# that they represent a concurrent pause, and return a modified database_table.
def getConcurrentData(database_table):
    concurrent = database_table.loc[database_table["EventType"] == "Concurrent"]
    return concurrent


def getPausesData(database_table):
    stoptheworld = database_table.loc[database_table["EventType"] == "Pause"]
    return stoptheworld


def seperatePausesConcurrent(database_table):
    return getPausesData(database_table), getConcurrentData(database_table)


# QUESTION: Would it be nice to append "Concurrent" to each type of concurrent event? Not needed?
def seperate_by_event_name(database_table):
    # Step 1: Sort based on column names in alphabetical order
    # Step 2: Traverse throuhgh the "EventName" column and find indicies where the event name switches
    # Step 3: transform each range into its own database_table
    # Step 4: Return a list of database_tables.
    sorted_data = database_table.sort_values(["EventName"])
    sorted_data = sorted_data.reset_index(drop=True)
    previousname = ""
    change_indicies = []
    for index in range(len(sorted_data["EventName"])):
        eventname = sorted_data["EventName"][index]
        # print(index, eventname)
        if previousname != eventname:
            change_indicies.append(index)
        previousname = eventname
    change_indicies.append(len(sorted_data["EventName"]))
    list_of_tables = []
    for index in range(len(change_indicies) - 1):
        list_of_tables.append(sorted_data.iloc[change_indicies[index] : change_indicies[index + 1]])

    return list_of_tables


# # Group all pauses & time data into N evenly distributed buckets, based on time
# def get_sum_pauses_n_buckets(timestamps, pausedata, num_buckets):
#     max_time = timestamps[-1]
#     duration = max_time / num_buckets
#     return __put_into_buckets(timestamps, pausedata, duration, num_buckets, sum)


# # Group all pasue & time data into some number of buckets with a given bucket duration
# def get_sum_pauses_n_duration(timestamps, pausedata, duration):
#     max_time = timestamps[-1]
#     num_buckets = max_time / duration
#     return __put_into_buckets(timestamps, pausedata, duration, num_buckets, sum)


# # Group all data based on event time into buckets, such that each bucket has the same duration
# def get_max_pauses_n_buckets(timestamps, pausedata, num_buckets):
#     max_time = timestamps[-1]
#     duration = max_time / num_buckets
#     return __put_into_buckets(timestamps, pausedata, duration, num_buckets, max)


# # Get the max pauses over buckets of n duration length
# def get_max_pauses_n_duration(timestamps, pausedata, duration):
#     max_time = timestamps[-1]
#     num_buckets = max_time / duration
#     return __put_into_buckets(timestamps, pausedata, duration, num_buckets, max)


# def __put_into_buckets(timestamps, pausedata, duration, num_buckets, grouping_method):
#     num_buckets = math.ceil(num_buckets)

#     buckets = [[] for i in range(num_buckets)]
#     times = [duration * i for i in range(1, num_buckets + 1)]

#     # First, sort all values into buckets based on the timestamp.
#     for time, pause in zip(timestamps, pausedata):
#         index_of_bucket = int(time / duration)
#         if index_of_bucket >= num_buckets:
#             index_of_bucket = num_buckets - 1
#         buckets[index_of_bucket].append(pause)

#     for idx in range(len(buckets)):
#         if buckets[idx]:
#             buckets[idx] = grouping_method(buckets[idx])
#         else:  # untested else case. TODO.
#             buckets[idx] = 0

#     return times, buckets

# Given lists of multiple pauses / stops, compare the runtime of the data.
# def compare_max_pauses_n_duration(xdata_lists, ydata_lists, duration):
#     xdata_bucketed_lists = []
#     ydata_bucketed_lists = []
#     for i in range(len(xdata_lists)):
#         xdata, ydata = SOMEFUNCTIONGOESHERE(xdata_lists[i], ydata_lists[i], duration)
#         xdata_bucketed_lists.append(xdata)
#         ydata_bucketed_lists.append(ydata)
#     return xdata_bucketed_lists, ydata_bucketed_lists

# def compare_max_pauses_n_buckets(xdata_lists, ydata_lists, num_buckets):
#     # Get the correct duration for a bucket to be applied to all data
#     max_pause = 0
#     for datalist in xdata_lists:
#         max_p = max(datalist)
#         max_pause = max(max_p, max_pause)
#     duration = math.ceil(max_pause / num_buckets)
#     # Gather the data using a constant duration and return
#     xdata_bucketed_lists = []
#     ydata_bucketed_lists = []
#     for i in range(len(xdata_lists)):
#         xdata, ydata = SOMEFUNCTIONGOESHERE(xdata_lists[i], ydata_lists[i], duration)
#         xdata_bucketed_lists.append(xdata)
#         ydata_bucketed_lists.append(ydata)
#     return xdata_bucketed_lists, ydata_bucketed_lists


# def compare_sum_pauses_n_duration(xdata_lists, ydata_lists, duration):
#     xdata_bucketed_lists = []
#     ydata_bucketed_lists = []
#     for i in range(len(xdata_lists)):
#         xdata, ydata = SOMEFUNCTIONGOESHERE(xdata_lists[i], ydata_lists[i], duration)
#         xdata_bucketed_lists.append(xdata)
#         ydata_bucketed_lists.append(ydata)
#     return xdata_bucketed_lists, ydata_bucketed_lists

# # Removes all data from a log file after a specified timestamp
# def setMaxTime(df, maxtime):
#     times = get_time_in_seconds(df)
#     cutoff = -1
#     for i in range(len(times)):
#         if times[i] > maxtime:
#             cutoff = i
#             break
#     if cutoff != -1:
#         to_cut = [idx for idx in range(cutoff, len(times))]
#         df.drop(to_cut, inplace=True)

# def compare_sum_pauses_n_buckets(xdata_lists, ydata_lists, num_buckets):
#     # Get the correct duration for a bucket to be applied to all data
#     max_pause = 0
#     for datalist in xdata_lists:
#         max_p = max(datalist)
#         max_pause = max(max_p, max_pause)
#     duration = math.ceil(max_pause / num_buckets)
#     # Gather the data using a constant duration and return
#     xdata_bucketed_lists = []
#     ydata_bucketed_lists = []
#     for i in range(len(xdata_lists)):
#         xdata, ydata = SOMEFUNCTIONGOESHERE(xdata_lists[i], ydata_lists[i], duration)
#         xdata_bucketed_lists.append(xdata)
#         ydata_bucketed_lists.append(ydata)
#     return xdata_bucketed_lists, ydata_bucketed_lists


# # Make a heatmap from given parameters. Recommended: Use default or change default for ALL runs.
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
    times_seconds, pauses_ms = get_time_and_event_durations(table)

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


# get the heap occupancy over runtime as a result of particular phases
def get_heap_occupancy(database_table):
    if database_table.empty:
        print("Empty database_table in get_heap_occupancy")
        return
    memory_change = list(database_table["MemoryChange_MB"])
    before_gc = []
    after_gc = []
    max_heap = []
    parsed_timestamps = []
    times = get_time_in_seconds(database_table)
    regex_pattern_memory = "(\d+)\w+->(\d+)\w+\((\d+)\w+\)"
    #   String parses things in this pattern: 1234M->123M(9999M)
    # Capture pattern 1: Before
    # Capture pattern 2: After
    # Capture pattern 3: Current maximum heap size (can change... lol)
    for idx in range(len(memory_change)):
        if memory_change[idx]:
            match = re.search(regex_pattern_memory, memory_change[idx])
            if match:
                before_gc.append(int(match.group(1)))
                after_gc.append(int(match.group(2)))
                max_heap.append(int(match.group(3)))
                parsed_timestamps.append(times[idx])

            else:
                print("Warning: Unable to parse this memory_change[idx]: " + memory_change[idx])
                # final return value is the unit as a string
    return before_gc, after_gc, max_heap, parsed_timestamps


#  See how much memory is free'd per phase of the gc
def get_reclaimed_mb_over_time(database_table):
    before_gc, after_gc, max_heap, parsed_timestamps = get_heap_occupancy(database_table)
    relcaimed_bytes = [before - after for before, after in zip(before_gc, after_gc)]
    return relcaimed_bytes, parsed_timestamps


def group_into_pause_buckets(stw_table, bucket_size_ms):
    pauses = get_event_durations_in_miliseconds(stw_table)
    max_pause = max(pauses)
    interval_bucket_count = max_pause / bucket_size_ms + 1
    frequencies = [0 for i in range(int(interval_bucket_count))]
    for pause in pauses:
        idx = int(pause / bucket_size_ms)
        if idx >= interval_bucket_count:
            print("Error: idx is >= interval_bucket_count, transform.py line 336")
        frequencies[idx] += 1
    return frequencies
