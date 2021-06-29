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
from src.graphing.heapoccupancy import plot_heap_occupancy
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
    bar_labels = []
    width = 0.9 / len(database_tables)
    for idx, database_table in enumerate(database_tables):
        stw_sum, concurrent_sum = transform.compare_eventtype_time_sums(database_table)
        bar_labels.append(round(stw_sum, 4))
        bar_labels.append(round(concurrent_sum, 4))
        x_coordinates = [i + (width * idx) for i in range(2)]
        axs.bar(x_coordinates, [stw_sum, concurrent_sum], width, color=colors[idx], label=labels[idx])
    axs.legend()
    # the median x tick along the axis
    axs.set_xticks([i + (width * (len(database_tables) - 1) / 2) for i in range(2)])
    axs.set_xticklabels(["STW Pauses", "Concurrent"])
    axs.set_ylabel("Total duration in seconds")
    axs.set_xlabel("Type of event")
    rect = axs.patches
    for rect, label in zip(rect, bar_labels):
        height = rect.get_height()
        axs.text(rect.get_x() + rect.get_width() / 2, height + 5, label, ha="center", va="bottom")

    return axs


def get_time_and_event_durations_from_lists(gc_events_dataframes):
    assert isinstance(gc_events_dataframes, list)
    xxx = []
    yyy = []
    for dataframe in gc_events_dataframes:
        stw_times, stw_durations = transform.get_time_and_event_durations(dataframe)
        xxx.append(stw_times)
        yyy.append(stw_durations)
    return xxx, yyy


def extract_events_by_name(list_of_gc_event_dataframes):
    seperated_list_gc_event_dataframes = []
    for dataframe in list_of_gc_event_dataframes:
        seperated_table_list = transform.seperate_by_event_name(dataframe)
        seperated_list_gc_event_dataframes.append(seperated_table_list)
    # Creates A 2D list of stuff ..... :)
    return seperated_list_gc_event_dataframes


# TODO: fix this documentation. I believe this approach itself is flawed :(
def compare_events_bar_chart(two_dimensional_dataframe_list, legend_vals):
    assert isinstance(two_dimensional_dataframe_list, list)
    if not two_dimensional_dataframe_list:
        print("Warning: src.compare_logs compare_events_bar_chart parameter empty.")
        return None
    fig, axs = plt.subplots()

    width = 0.8 / len(two_dimensional_dataframe_list)
    # Algorithm:
    # 1) Count the number of upcoming categories.
    # 2) Group all things into those categories
    # 3) Plot.
    event_names = {}
    for item in two_dimensional_dataframe_list:
        for event in item:
            if event["EventName"].iloc[0] not in event_names:
                event_names[event["EventName"].iloc[0]] = None
    keys = list(event_names.keys())
    colors = ["r", "k", "b", "cyan", "green", "purple"]
    labels = []
    ticks_gathered = []
    for log_index in range(len(two_dimensional_dataframe_list)):
        label_added = False
        for key_index, key in enumerate(keys):
            found = False
            index_value = log_index * width + key_index
            for event in two_dimensional_dataframe_list[log_index]:
                if str(key) == event["EventName"].iloc[0]:  # O(N^2) FIX plz ... :(
                    found = True
                    duration = transform.get_event_durations_in_miliseconds(event)
                    if duration:
                        average = sum(duration) / len(duration)
                    else:
                        average = 0
                    labels.append(round(average, 5))
                    index_value = log_index * width + key_index
                    ticks_gathered.append(index_value)
                    if not label_added:
                        axs.barh(
                            [index_value], [average], width, color=colors[log_index], label=legend_vals[log_index]
                        )
                    else:
                        axs.barh([index_value], [average], width, color=colors[log_index])
                    label_added = True
            if not found:
                if not label_added:
                    axs.barh([index_value], 0, color=colors[log_index], label=legend_vals[log_index])
                else:
                    axs.barh([index_value], 0, color=colors[log_index])
                label_added = True
                axs.barh([index_value], 0, color=colors[log_index])
                labels.append(0)

    rect = axs.patches
    # axs.grid()
    for rect, label in zip(rect, labels):
        rect_width = rect.get_width()
        axs.text(rect_width + 0.45, rect.get_y() + rect.get_height() / 2, label, ha="center", va="bottom")
    ticks = [i + (width * (len(two_dimensional_dataframe_list) - 1) / 2) for i in range(len(keys))]
    axs.set_yticks(ticks)
    axs.set_yticklabels(keys)
    new_ticks = []

    for inner in range(len(keys)):
        for outer in range(len(two_dimensional_dataframe_list)):
            new_ticks.append(inner + outer * width - width / 2)
            new_ticks.append(inner + outer * width)

            new_ticks.append(inner + outer * width + width / 2)
    print(new_ticks)
    axs.set_yticks(new_ticks)
    axs.set_ylabel("Event type")
    axs.set_xlabel("Average time in MS")
    axs.set_title("Average event durations across all logs.")
    axs.legend()


def compare_heap_occupancy(gc_event_dataframes, max_heapsize):
    assert isinstance(gc_event_dataframes, list)
    times_max = []
    fig, g = plt.subplots()

    for dataframe in gc_event_dataframes:
        before_gc, after_gc, max_heap, times_selected = transform.get_heap_occupancy(dataframe)
        times_max.append(max(times_selected))
        # g = plot_heap_occupancy(
        #     times_selected, before_gc, "M", max_heapsize, "G", axs=g, label="Usage before gc", plot_max=False
        # )
        g = plot_heap_occupancy(
            times_selected, after_gc, "M", max_heapsize, "G", axs=g, label="Usage after gc", plot_max=False
        )

    g.plot([0, max(times_max)], [max_heapsize * 1000, max_heapsize * 1000], label="Max heapsize")
    g.legend()


def compare_heap_occupancy2(gc_event_dataframes, max_heapsize):
    assert isinstance(gc_event_dataframes, list)
    times_max = []
    fig, g = plt.subplots()

    for dataframe in gc_event_dataframes:
        before_gc, after_gc, max_heap, times_selected = transform.get_heap_occupancy(dataframe)
        times_max.append(max(times_selected))
        # g = plot_heap_occupancy(
        #     times_selected, before_gc, "M", max_heapsize, "G", axs=g, label="Usage before gc", plot_max=False
        # )
        g = plot_heap_occupancy(
            times_selected, before_gc, "M", max_heapsize, "G", axs=g, label="Usage before_gc", plot_max=False
        )
    g = plot_heap_occupancy(times_selected, before_gc, "M", max_heapsize, "G", axs=g, label="Usage before_gc")
    g.legend()
