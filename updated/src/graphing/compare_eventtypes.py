#       compare_eventtypes
#
#   Plot differences from gc_event_dataframes trends. 
#   Plots comparisons between sum or average of events of certain types
#
#   Ellis Brown, 6/29/2021
import matplotlib.pyplot as plt
import sys
import pandas as pd
import numpy as np

sys.path.append("/Users/ellisbrown/Desktop/Project/updated/src/")
import transform


def compare_eventtypes_pie(database_table):
    assert isinstance(database_table, pd.DataFrame)
    if database_table.empty:
        print("Error: Empty database_table in compare_eventtypes_pie")
        return None
    fig, axs = plt.subplots()
    pauses_time, concurr_time = transform.compare_eventtype_time_sums(database_table)  # get the ratios of pause time
    axs.axis("equal")  # center axis
    axs.set_title("Comparison of Event Types")  # set the title
    axs = axs.pie([pauses_time, concurr_time], labels=["STW Pauses", "Concurrent Time"])
    return axs


def compare_eventtypes_bar(database_table):  # TODO FIX
    fig1, axs = plt.subplots()
    pauses_time, concurr_time = transform.compare_eventtype_time_sums(database_table)  # get the ratios of pause time
    pauses_time = pauses_time / 1000
    concurr_time = concurr_time / 1000
    #  Plot using a bar graph.
    bars = ["STW Pauses", "Concurrent Time"]
    bars = ["A", "B"]
    heights = [pauses_time, concurr_time]
    axs.bar(bars, heights)
    axs.grid()
    axs.set_ylabel("Total pause time in seconds")
    axs.set_title("Comparison of event types")
    axs.set_xlabel("Types of events")
    return axs


#       compare_averages_bar
#
#   Compare the mean of each list in the durations_lists, plotting them
#   horizontally in a bar chart, using labels and titles to display the plot.
#
def compare_averages_bar(durations_lists, labels, title=None):
    assert isinstance(durations_lists, list)
    assert isinstance(labels, list)
    if title:
        assert isinstance(title, str)
    else:
        title = "Mean durations in miliseconds"

    fig, ax = plt.subplots()
    duration_averages = []
    for i in range(len(durations_lists)):
        duration_averages.append(sum(durations_lists[i]) / len(durations_lists[i]))
    ax.barh(np.arange(len(labels)), duration_averages, align="center")
    ax.set_yticks(np.arange(len(labels)))
    ax.set_yticklabels(labels)
    ax.set_xlabel("Miliseconds average")
    ax.set_title(title)
    ax.grid()
    return ax
