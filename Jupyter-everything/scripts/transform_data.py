# transform_data.py
""" Take data and selectively return or parse sections of the data.
    Remove extra characters or add them. Does not change any values"""
# Ellis Brown
# 6/15/2021
import numpy as np
import pandas as pd  # implicit. TODO: check if this is needed

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
                        + str(y_bucket_count * y_bucket_duration) + " ms"
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
