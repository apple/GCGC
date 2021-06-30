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


#       compare_eventtypes_pie
#
#   Creates a pie chart to compare the Stop the world pauses vs concurrent times sums
#   for information in a gc_event_dataframe
#
#
def compare_eventtypes_pie(gc_event_dataframe):
    assert isinstance(gc_event_dataframe, pd.DataFrame)
    if gc_event_dataframe.empty:
        print("Error: Empty gc_event_dataframe in compare_eventtypes_pie")
        return None
    fig, axs = plt.subplots()
    # get the sums for each
    pauses_time, concurr_time = transform.compare_eventtype_time_sums(gc_event_dataframe)
    axs.set_title("Comparison of Event Types")  # set the title
    axs = axs.pie([pauses_time, concurr_time], labels=["STW Pauses", "Concurrent Time"])
    return axs


#       compare_eventtypes_bar
#
#   Calculates the total time spent in concurrent events and stop the world events,
#   and plots them against each other on a figure
#
def compare_eventtypes_bar(gc_event_dataframe):
    fig1, axs = plt.subplots()
    pauses_time, concurr_time = transform.compare_eventtype_time_sums(
        gc_event_dataframe
    )  # get the ratios of pause time
    pauses_time = pauses_time / 1000
    concurr_time = concurr_time / 1000
    #  Plot using a bar graph.
    bars = ["STW Pauses", "Concurrent Time"]
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
