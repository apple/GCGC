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
    colors = np.random.rand(len(database_tables), 3)
    colors = ["r", "orange", "gold", "lawngreen", "indigo", "violet"]
    colors = colors + colors
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


#       get_time_and_event_durations_from_lists
#
#   From multiple gc_event_dataframes, gather their timestamp and event_durations,
#   and return a list of each, in the same order as the dataframes
#
def get_time_and_event_durations_from_lists(gc_events_dataframes):
    assert isinstance(gc_events_dataframes, list)
    timestamps_2d = []  # 2d: list of list of floats
    durations_2d = []  # 2d: list of list of floats
    for dataframe in gc_events_dataframes:
        stw_times, stw_durations = transform.get_time_and_event_durations(dataframe)
        timestamps_2d.append(stw_times)
        durations_2d.append(stw_durations)
    return timestamps_2d, durations_2d


#       extract_events_by_name
#
#   Takes a list of gc_event_dataframes, and accesses each dataframe. From there,
#   it seperates the events by name into smaller dataframes. Returns a list of these groupings of
#   dataframes, such that the order of the returned grouping reflects the order of the passed gc_event_dataframes
#
def extract_events_by_name(list_of_gc_event_dataframes):
    seperated_list_gc_event_dataframes = []
    for dataframe in list_of_gc_event_dataframes:
        seperated_table_list = transform.seperate_by_event_name(dataframe)
        seperated_list_gc_event_dataframes.append(seperated_table_list)
    # Creates A 2D list of stuff ..... :)
    return seperated_list_gc_event_dataframes


#       compare_events_bar_chart
#
# Takes in a list of dataframes, and cmopares the mean duration of the events
# If one log has event that another does not, the duration = 0.
#
# TODO: fix this documentation. I believe this approach itself is flawed :(
def compare_events_bar_chart(two_dimensional_dataframe_list, legend_vals, display_barvals=False):
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
    # colors = ["r", "k", "b", "cyan", "green", "purple"]
    # colors = np.random.rand(len(two_dimensional_dataframe_list), 3)
    colors = ["r", "orange", "gold", "lawngreen", "indigo", "violet"]
    colors = colors + colors
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
                            [index_value],
                            [average],
                            width,
                            color=colors[log_index],
                            label=legend_vals[log_index],
                            alpha=0.5,
                        )
                    else:
                        axs.barh([index_value], [average], width, color=colors[log_index], alpha=0.5)
                    label_added = True
            if not found:
                if not label_added:
                    axs.barh([index_value], 0, color=colors[log_index], label=legend_vals[log_index], alpha=0.5)
                else:
                    axs.barh([index_value], 0, color=colors[log_index], alpha=0.5)
                label_added = True
                axs.barh([index_value], 0, color=colors[log_index])
                labels.append("")
    rect = axs.patches
    # axs.grid()
    if display_barvals:
        for rect, label in zip(rect, labels):
            rect_width = rect.get_width()
            axs.text(rect_width, rect.get_y() + rect.get_height() / 2, label, ha="center", va="bottom")
    ticks = [i + (width * (len(two_dimensional_dataframe_list) - 1) / 2) for i in range(len(keys))]

    axs.set_yticks(ticks)
    axs.set_yticklabels(keys)
    new_ticks = []
    for inner in range(len(keys)):
        for outer in range(len(two_dimensional_dataframe_list)):
            new_ticks.append(inner + outer * width - width / 2)
            new_ticks.append(inner + outer * width)

            new_ticks.append(inner + outer * width + width / 2)

    axs.set_yticks(new_ticks)
    axs.set_ylabel("Event type")
    axs.set_xlabel("Average time in MS")
    axs.set_title("Average event durations across all logs.")
    axs.legend()


#       compare_heap_occupancy
#
#   From a list of dc_event_dataframes, plot the heap allocation before GC and after GC
#   on two charts. Plots the maximum heapsize as a constant line, to show how full the heap is.
#   Note: If different plots of have different maximum heaps, this may not make sense.
#
def compare_heap_occupancy(gc_event_dataframes, max_heapsize, labels):
    # Parameters:
    #   gc_event_dataframes: list, each elemt being of type pd.DataFrame
    #   max_heapsize: contains the size of the heap in GB
    #   labels: list of all names for the dataframes. typically filenames
    assert isinstance(gc_event_dataframes, list)
    assert isinstance(labels, list)
    assert type(max_heapsize) == float or type(max_heapsize) == int
    if not gc_event_dataframes:
        print("Error: No gc_event_dataframes in compare_heap_occupancy.")
        return None
    if not labels:
        print("Error: No labels in compare_heap_occupancy.")
    if not len(labels) == len(gc_event_dataframes):
        print("Length of labels does not match lengh of gc_event_dataframes in compare_heap_occupancy")
    for dataframe in gc_event_dataframes:
        assert isinstance(dataframe, pd.DataFrame)
    # After parameters are correct, create two plots, one for before gc events, one for after gc events
    fig, before = plt.subplots()
    fig, after = plt.subplots()
    # Get the heap occupancy over time for the first dataframe, and plot with the max
    before_gc, after_gc, _, times_selected = transform.get_heap_occupancy(gc_event_dataframes[0])
    before = plot_heap_occupancy(times_selected, before_gc, "M", max_heapsize, "G", before, label=labels[0])
    after = plot_heap_occupancy(times_selected, after_gc, "M", max_heapsize, "G", after, label=labels[0])

    # for every other item in the list, plot before & after heap allocation over time.
    for idx, dataframe in enumerate(gc_event_dataframes[1:]):
        before_gc, after_gc, _, times_selected = transform.get_heap_occupancy(dataframe)
        before = plot_heap_occupancy(
            times_selected, before_gc, "M", max_heapsize, "G", axs=before, label=labels[idx + 1], plot_max=False
        )
        after = plot_heap_occupancy(
            times_selected, after_gc, "M", max_heapsize, "G", axs=after, label=labels[idx + 1], plot_max=False
        )
    before.set_ylim(0)  # Make sure axis are not misleading (especially between the two charts)
    after.set_ylim(0)  # Make sure axis are not misleading (especially between the two charts)
    before.set_title("Memory used BEFORE  gc")
    after.set_title("Memory used AFTER gc")
    return (before, after)  # Return plots
