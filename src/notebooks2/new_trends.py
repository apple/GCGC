#       percentiles.py
#
#   Analyzes trends in lists of pause data, and prints percentiles
#   of the longest paused time
#
#   Ellis Brown, 6/29/2021

from graphing.__generic_mapping import __string_const_chars
import numpy as np


def apply_filter(gc_event_dataframes, filter_by=None):
    dfs = []
    if filter_by:
        # create a copy, to be modified
        for df in gc_event_dataframes:
            dfs.append(df.copy())

        for idx in range(len(dfs)):
            for col, value in filter_by:
                if value:
                    dfs[idx] = dfs[idx][dfs[idx][col] == value]
                else:
                    dfs[idx] = dfs[idx][dfs[idx][col] != None]

    else:
        dfs = gc_event_dataframes
    return dfs


#       print_percentiles
#
#   Display what percent of pauses meet a certain percentile threshold
#
def print_percentiles(pauses_miliseconds=[], print_title=True, percentiles=None, label=None):
    # Parameters:
    #   pauses_miliseconds  : a list of pauses to be analyzed (in any order)
    #   print_title         : True if you would like column headers
    #   percentiles         : a list of percentiles to be plotted, in float list form.
    #   label               : a label to be printed. Should be 0-10 characters
    if not pauses_miliseconds:
        print("pauses_miliseconds not provided to print_percentiles")
        return
    pauses_miliseconds = sorted(pauses_miliseconds, reverse=True)
    percentile_table = {}
    if not percentiles:
        percentiles = [50, 75, 90, 95, 99, 99.9, 99.99]
    for p in percentiles:
        percentile_table[p] = np.percentile(pauses_miliseconds, p)
    if not label:
        label = "label"
    if print_title:
        title = ""
        for p in percentiles:
            title += __string_const_chars(str(p) + "%", 9) + " | "
        print("Percentiles| " + title + "\n" + "-" * (len(title) + 12))
    print(__string_const_chars(label, 10) + " | ", end="")
    for p in percentiles:
        print(__string_const_chars(str(round(percentile_table[p], 2)) + " ms", 9) + " | ", end="")
    print("")


#       compare_percentiles
#
#   Plot the percentiles for pause time in miliseconds for all lists provided, on the same table
#   Parameters:
#       pauses_miliseconds    : list of [list of pauses as floats in ms]
#       percentiles(optional) : list of float value percentiles to be viewed.
#
def compare_percentiles(gc_event_dataframes=None, percentiles=None, labels=None):
    list_of_list_pauses_ms = [list(df["TimeFromStart_seconds"]) for df in gc_event_dataframes]
    if not labels:
        labels = [str(i) for i in range(len(list_of_list_pauses_ms))]
    print_percentiles(list_of_list_pauses_ms[0], True, percentiles, labels[0])

    for i in range(1, len(list_of_list_pauses_ms)):
        print_percentiles(list_of_list_pauses_ms[i], False, percentiles, labels[i])


#       trends.py
#
#   Given a list of floats, analyze macro trends within the data such as
#   the sum, count, and max/min. Print using an ASCII table.
#
#   Ellis Brown, 6/29/2021

from graphing.__generic_mapping import __string_const_chars
import pandas as pd
import numpy as np

#       print_trends
#
# Print the trends within the data (total number of pauses, max wait, total wait mean wait)
# returns total wait
#
def print_trends(pauses_miliseconds, label=None, print_title=True, total_runtime_seconds=0, timestamps=None):
    # Parameters:
    #   pauses_miliseconds    : list of pauses (floats)
    #   label                 : label for this row in the table
    #   print_title(optional) : bool, True => print recorded values
    assert isinstance(pauses_miliseconds, list)
    if pauses_miliseconds:
        max_pause = round(max(pauses_miliseconds, key=lambda i: float(i)), 4)
        sum_pauses = round(sum(float(i) for i in pauses_miliseconds), 4)
        average_wait = round(sum_pauses / len(pauses_miliseconds), 4)
        std_deviation = round(np.std(pauses_miliseconds), 4)
    else:
        max_pause, sum_pauses, average_wait, std_deviation = 0, 0, 0, 0
    throughput = None
    if total_runtime_seconds:
        print(total_runtime_seconds)
        throughput = round(((total_runtime_seconds * 1000) - sum_pauses) / (total_runtime_seconds * 1000), 4) * 100
    elif timestamps:
        throughput = round(((timestamps[-1] * 1000) - sum_pauses) / (timestamps[-1] * 1000), 4) * 100

    # Print title with formatting
    if print_title:
        title = " Trends (ms)            | "  # 17 + 3 characters
        title += "Event Count  | "
        title += "Max Duration | "
        title += "Sum Duration | "
        title += "Mean Duration| "
        title += "Std Dev.     |"
        if throughput:
            title += " Throughput   |"
        print(title)
        print("-" * len(title))
    num_chars = 12
    if not label:
        label = "Run:"
    # print with correct formatting the values
    number_label_chars = 23
    label = label[-number_label_chars:]
    line = __string_const_chars(label, 23) + " | "
    line += __string_const_chars(str(len(pauses_miliseconds)), num_chars) + " | "
    line += __string_const_chars(str(max_pause), num_chars) + " | "
    line += __string_const_chars(str(sum_pauses), num_chars) + " | "
    line += __string_const_chars(str(average_wait), num_chars) + " | "
    line += __string_const_chars(str(std_deviation), num_chars) + " | "
    if throughput:
        line += __string_const_chars(str(round(throughput, 4)) + "%", num_chars) + " | "
    print(line)


#       compare_trends
#
#   Compares trends from a list of pauses lists
#
def compare_trends(gc_event_dataframes, labels=None, lists_of_total_program_runtime=[], lists_of_timestamps=[]):
    pauses_ms_lists = [list(df["TimeFromStart_seconds"]) for df in gc_event_dataframes]
    if not pauses_ms_lists:
        print("No pauses_ms_lists in compare_trends.")
        return
    if not labels:
        labels = [str(i) for i in range(len(pauses_ms_lists))]
    # The second and third parameters are optionally lists. Pass them if the parameter exists , and decide between the two.
    # Otherwise, pass none. Pass the first (index 0) with title TRUE, the rest in loop title FALSE.
    if lists_of_total_program_runtime:
        print_trends(pauses_ms_lists[0], labels[0], True, lists_of_total_program_runtime[0])
        for i in range(1, len(pauses_ms_lists)):
            print_trends(pauses_ms_lists[i], labels[i], False, lists_of_total_program_runtime[i])
    elif lists_of_timestamps:
        print_trends(pauses_ms_lists[0], labels[0], True, timestamps=lists_of_timestamps[0])
        for i in range(1, len(pauses_ms_lists)):
            print_trends(pauses_ms_lists[i], labels[i], False, timestamps=lists_of_timestamps[i])
    else:
        print_trends(pauses_ms_lists[0], labels[0], True)
        for i in range(1, len(pauses_ms_lists)):
            print_trends(pauses_ms_lists[i], labels[i], False)
