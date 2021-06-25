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
#
#
def compare_stw_concurrent_durations(database_tables):
    N = len(database_tables)
    ind = np.arange(N)  # the x locations for the groups
    fig, axs = plt.sublpots()
    colors = ["r", "g", "b", "k", "o"]
    width = 0.9 / len(database_tables)
    for i, database_table in enumerate(database_tables):
        stw_sum, concurrent_sum = transform.compare_eventtype_time_sums(database_table)
        axs.bar([0, 1], [stw_sum, concurrent_sum], width, color=colors[i])

    fig, ax = plt.sublpots()

    stw_sums = [4, 9, 2]
    rects1 = ax.bar(ind, stw_sums, width, color="r")
    zvals = [1, 2, 3]
    rects2 = ax.bar(ind + width, zvals, width, color="g")
    kvals = [11, 12, 13]
    rects3 = ax.bar(ind + width * 2, kvals, width, color="b")
