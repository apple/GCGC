#       compare_logs.py
#
#   Compares multiple logs, by calling functions for each file in a list, or each
#   gc_event_dataframe in a list. Handles the complex mapping for different datatypes and labels
#
#   Ellis Brown, 6/29/2021

# Compare multiple logs, using the API calls designed for a singular log
# Handle graphing & colors & labels & data transformations.
# Ellis Brown, June 2021
from src import transform
from src.read_log_file import get_parsed_data_from_file
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


#       get_parsed_comparions_from_files
#
#   Take a list of log file paths/names, and construct a list of tables, one for
#   each log in the list.
#
def get_parsed_comparions_from_files(files, time_range_seconds=None):
    # Files must be a list of strings
    # Time range in seconds is either a list with 2 values,
    # or a single integer max time.
    assert isinstance(files, list)
    database_tables = []
    for file in files:
        database_table = get_parsed_data_from_file(file, time_range_seconds)
        if not database_table.empty:
            database_tables.append(database_table)
    return database_tables


#       seperate_pauses_concurrent_list
#
#   given a list of database tables, for each database_table in the list,
#   seperate it into two pandas databases, one for pauses & one for concurrent
#
def seperate_pauses_concurrent_lists(database_tables):
    assert isinstance(database_tables, list)
    for database_table in database_tables:
        assert isinstance(database_table, pd.DataFrame)
    stw_list = []
    concurrent_list = []
    for database_table in database_tables:
        pauses, concurrent = transform.seperate_pauses_concurrent(database_table)
        stw_list.append(pauses)
        concurrent_list.append(concurrent)
    return stw_list, concurrent_list


#       compare_stw_concurrent_durations
#
#   From a list of tables, compare the total sum of the concurrent
#   and STW durations in miliseconds against each other in a bar chart.
#   Return the chart axes.
#
def compare_stw_concurrent_durations(database_tables, labels):
    assert isinstance(database_tables, list)
    assert isinstance(labels, list)
    if not labels:
        print("No labels provided to compare_stw_concurrent_durations.")
        return None
    if not len(labels) == len(database_tables):
        print("Duration of database_tables list and labels list do not match.")
        return None
    fig, axs = plt.subplots()
    colors = ["r", "g", "b", "k", "c", "y", "m"]
    # colors = colors + colors + colors

    width = 0.9 / len(database_tables)
    for idx, database_table in enumerate(database_tables):
        stw_sum, concurrent_sum = transform.compare_eventtype_time_sums(database_table)
        x_coordinates = [i + width * idx for i in range(2)]
        axs.bar(x_coordinates, [stw_sum, concurrent_sum], width, color=colors[idx], label=labels[idx])
    axs.legend()
    # the median x tick along the axis
    axs.set_xticks([i + (width * (len(database_tables) - 1) / 2) for i in range(2)])
    axs.set_xticklabels(["STW Pauses", "Concurrent"])
    axs.set_ylabel("Total duration in seconds")
    axs.set_xlabel("Type of event")
    return axs
