import matplotlib.pyplot as plt
import sys

sys.path.append("/Users/ellisbrown/Desktop/Project/updated/src/")
import transform


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
