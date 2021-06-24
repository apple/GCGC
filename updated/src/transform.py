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
    assert isinstance(database_table, pd.DataFrame)
    return get_time_in_seconds(database_table), get_event_durations_in_miliseconds(database_table)


#       get_event_durations_in_miliseconds
#
#   Given a pandas dataframe table populated with parsed log information,
#   extract all 'event durations' from the Duration_miliseconds column, and
#   return them as a list of floats.
#
def get_event_durations_in_miliseconds(database_table):
    assert isinstance(database_table, pd.DataFrame)
    if database_table.empty:
        return []
    else:
        return list(map(float, database_table["Duration_miliseconds"]))


#       get_time_in_seconds
#
#   Given a pandas dataframe table populated with parsed information, exact only
#   the time since program start timestamps, and return them as a list of floats
#
def get_time_in_seconds(database_table):
    assert isinstance(database_table, pd.DataFrame)
    if database_table.empty:
        return []
    else:
        return list(map(float, database_table["TimeFromStart_seconds"]))


#    get_times_and_durations_from_event_lists
#
#   Given a list of tables, extract the event timestamp and event durations from each
#   and return 2 lists, one being a list containing lists of floats, corresponding to
#   timestamps, and the second being a list of floats corresponding to event durations
#
def get_times_and_durations_from_event_lists(event_tables):
    assert isinstance(event_tables, list)
    if not event_tables:
        print("Error: event_tables empty")
        return [], []
    for table in event_tables:
        assert isinstance(table, pd.DataFrame)
    xdatas_list = []
    ydatas_list = []
    for event_table in event_tables:
        xdata, ydata = get_time_and_event_durations(event_table)
        xdatas_list.append(xdata)
        ydatas_list.append(ydata)
    return xdatas_list, ydatas_list


#       get_event_table_labels
#
#   From a list of event_tables, gather the name of the
#   event type and event name and return that as a label,
#   one label corresponding to each event_table. If eventtype
#   is true, then the eventtype is part of the returned label.
#
def get_event_table_labels(event_tables, eventtype=True):
    # assert the correct parameter types
    assert isinstance(event_tables, list)
    if not event_tables:
        print("Error: event_tables empty")
        return None
    for table in event_tables:
        assert isinstance(table, pd.DataFrame)
        if table.empty:
            print("Error: Empty table in event_table, unable to assign it a label")
            return []
    # return the labels
    if eventtype:
        return [
            event_tables[i]["EventType"].iloc[0] + " " + event_tables[i]["EventName"].iloc[0]
            for i in range(len(event_tables))
        ]
    else:
        return [event_tables[i]["EventName"].iloc[0] for i in range(len(event_tables))]


#       compare_eventtype_time_sums
#
#   Gathers from a complete database_table the set of
#   Stop The World pause durations, and concurrent durations,
#   and returns the sum of each, as a pair of floats.
#
def compare_eventtype_time_sums(database_table):
    assert isinstance(database_table, pd.DataFrame)
    if database_table.empty:
        print("Error: Database_table is empty")
        return 0, 0
    concurrent = get_concurrent_data(database_table)
    concurrent_total_time = sum(get_event_durations_in_miliseconds(concurrent))

    stw = get_pauses_data(database_table)
    stw_total_time = sum(get_event_durations_in_miliseconds(stw))
    return stw_total_time, concurrent_total_time


#   get_concurrent_data
#
#   From a complete database_table, return the table rows that represent
#   a concurrent event.
#
def get_concurrent_data(database_table):
    assert isinstance(database_table, pd.DataFrame)
    if database_table.empty:
        print("Warning: Empty database table in get_concurrent_data")
        return None
    concurrent = database_table.loc[database_table["EventType"] == "Concurrent"]
    return concurrent


#   getPauseData
#
#   From a complete database_table, return the table rows that
#   represent all STW pause events.
#
def get_pauses_data(database_table):
    assert isinstance(database_table, pd.DataFrame)
    if database_table.empty:
        print("Warning: Empty database table in get_pauses_data")
        return None
    stoptheworld = database_table.loc[database_table["EventType"] == "Pause"]
    return stoptheworld


#   seperate_pauses_concurrent
#
#   From a complete database_table, seperate the table into two
#   tables, one for all pause events, and the second for all concurrent events
#   Note: the original table is not modified.
#
def seperate_pauses_concurrent(database_table):
    assert isinstance(database_table, pd.DataFrame)
    if database_table.empty:
        print("Warning: Empty database table in seperate_pauses_concurrent")
        return None
    return get_pauses_data(database_table), get_concurrent_data(database_table)


#   seperate_by_event_name
#
#   Given a database_table with some number of rows, return a list
#   of tables sorted based on alphanetical order by EventName. Each index in
#   the returned list is a table, all of whose rows share the same EventName
#
def seperate_by_event_name(database_table):
    assert isinstance(database_table, pd.DataFrame)
    if database_table.empty:
        print("Warning: Empty database table in seperate_by_event_name")
        return None
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


#       get_heap_occupancy
#
#   From a database table, return all associated information about heap
#   occupancy before and after each event, if reported. Because not all
#   events change heap occupancy (free/used memory), this also returns
#   a lists of floats corresponding to the times where the memory did change
#
def get_heap_occupancy(database_table):
    assert isinstance(database_table, pd.DataFrame)
    if database_table.empty:
        print("Warning: Empty database_table in get_heap_occupancy")
        return None
    memory_change = list(database_table["MemoryChange_MB"])
    before_gc = []
    after_gc = []
    max_heap = []
    parsed_timestamps = []
    times = get_time_in_seconds(database_table)
    regex_pattern_memory = "(\d+)\w+->(\d+)\w+\((\d+)\w+\)"
    # String parses things in this pattern: 1234M->123M(9999M)
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


#       get_reclaimed_mb_over_time
#
#  Given a database table, find the change in total memory allocated after each event,
#   to find the total reclaimed bytes. Because not all events reclaim bytes, report the times
#   where they do change. Both lists returned contain floats.
#
def get_reclaimed_mb_over_time(database_table):
    assert isinstance(database_table, pd.DataFrame)
    if database_table.empty:
        print("Warning: Empty database_table in get_reclaimed_mb_over_time")
        return [], []
    before_gc, after_gc, max_heap, parsed_timestamps = get_heap_occupancy(database_table)
    relcaimed_bytes = [before - after for before, after in zip(before_gc, after_gc)]
    return relcaimed_bytes, parsed_timestamps


#       group_into_pause_buckets
#
#   Given a table containing events, place the events into time intervals of size
#   bucket_size_ms, and return a frequency list from that information.
#
def group_into_pause_buckets(stw_table, bucket_size_ms):
    assert isinstance(stw_table, pd.DataFrame)
    assert (type(bucket_size_ms) == int) or (type(bucket_size_ms) == float)
    if stw_table.empty:
        print("Warning: Empty table in group_into_pause_buckets.")
        return None
    if bucket_size_ms <= 0:
        print("Warning: Bucket_size_ms is equal to zero. Please use a positive number.")
        return None

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


#       get_heatmap_data
#
#   Create a 2d numpy array, and dimensions list associated with a event_table, such that
#   the 2d array represents the frequencies of latency events, based on the specified dimensions.
def get_heatmap_data(
    event_table,  # database_table of events. Typically only pause events
    x_bucket_count=20,  # Number of time intervals to group gc events into. INT ONLY
    y_bucket_count=20,  # Number of latency time intervals to group events into. INT ONLY
    x_bucket_duration=100,  # Duration in seconds that each time interval bucket has for gc event timestamps
    y_bucket_duration=10,  # Duration in miliseconds for the length of each latency interval bucket
    suppress_warnings=False,  # If True, warnings about values lying outside of dimension range will not be printed.
):
    assert isinstance(event_table, pd.DataFrame)
    if event_table.empty:
        print("Warning: Empty table in get_heatmap_data.")
        return None, None
    for x in [x_bucket_count, y_bucket_count]:
        assert type(x) == int, "Warning: x_bucket_count and y_bucket_count must be integers"

    for x in [x_bucket_duration, y_bucket_duration]:
        assert (
            type(x) == int or type(x) == float
        ), "Warning: x_bucket_duration and y_bucket_duration must be floats or integers"
    for x in [x_bucket_count, y_bucket_count, x_bucket_duration, y_bucket_duration]:
        if x <= 0:
            print("Warning: All dimensions must be greater than zero.")
            return None, None

    if event_table.empty:
        print("Empty event_table in get_heatmap_data")
        return None, None
    times_seconds, pauses_ms = get_time_and_event_durations(event_table)

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
