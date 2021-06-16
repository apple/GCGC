import re
import numpy as np
from scripts import updated_parse_log as pl
import matplotlib.pyplot as plt

## # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#                   plot_heap_allocation_breakdown                             #
#                                                                              #
#   Purpose:                                                                   #
#       Print a graph showing the heap breakdown throughout runtime            #
#   Parameters:                                                                #
#       counts: list  -> could represent two different data formats            #
#            if len(list) == 1:                                                #
#                   2 dimensional list, with all region counts                 #
#                   before and after gc pauses                                 #
#            if len(list) == 2:                                                #
#                   list[0] = dictionary, with all region counts               #
#                   list[2] = integer, size of initial free memory             #
## # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# TODO: This is very hard to understand function. WILL FIX SOON
# THE TIME TO FIX IS NOW!!!! TODO when back! :D
def plot_heap_allocation_breakdown(breakdown_lst, max_heap=0):
    if not breakdown_lst:
        return

    # determine data arrangement from list length
    if (len(breakdown_lst)) == 2:
        return __plot_HA_schema0(breakdown_lst, max_heap)

    # Access 2 dimensional list of allocation during runtime
    allocation_summary = breakdown_lst[0]

    # Create helper list [0...n-1] to plot
    x = np.array(list(range(len(allocation_summary))))

    # Order matters here, associated with order collected this data.
    # TODO: Remove dependence on Order, use dictionary instead
    region_names = [
        "Free",
        "Young",
        "Survivor",
        "Old",
        "Humongus_start",
        "Humongus_continue",
        "Collection_set",
        "Open_archive",
        "Closed_archive",
        "TAMS",
    ]

    # Add titles and format style to plot
    colors = ["royalblue", "cyan", "black", "green", "purple", "lime", "brown", "darkmagenta", "lime", "green"]
    plt.xlabel("GC Run number (not based on time)")
    plt.ylabel("Number of memory blocks")
    plt.title("heap allocation throughout runtime")
    plt.legend(region_names)
    # Plot information for each region
    for idx in range(len(allocation_summary[0])):
        plt.plot(x, np.array(list(row[idx] for row in allocation_summary)), color=colors[idx], label=region_names[idx])
    plt.legend()
    plt.show()


## # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#                   __plot_HA_schema0                                          #
#   Purpose:                                                                   #
#       Plot the heap breakdown throughout program using memory collected      #
#       following a log schema0. Display 3 plots                               #
#       -> Memory regions during runtime (without free memory)                 #
#       -> Free heap memory regions                                            #
#       -> Memory regions + free regions during runtime                        #
#                                                                              #
#   Parameters:                                                                #
#       dd : list, 2 items                                                     #
#       dd[0] : dictionary containing                                          #
#               keys:   names of regions during runtime                        #
#              values:  list of before/after tuple pairs of size when gc runs  #
#       dd[1] : Initial number of free regions before runtime.                 #
#                                                                              #
#   Return: None                                                               #
#                                                                              #
#   Note: generates MatPlotLib plot                                            #
## # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def __plot_HA_schema0(dd, max_heap=0):

    if (not dd) or (len(dd) < 2) or (not dd[0]):
        return
    if not dd:
        print("No data to plot")
        return
    if len(dd) < 2:
        print("Not enough data to plot Heap Allocation")
        return
    if not dd[0]:
        print("List missing collected Heap Allocation data")
        return
    if not dd[1] and not max_heap:
        print("Failed to find inital memory size. Rerun with parameter max_heap = (int)")
    if max_heap != 0:
        dd[1] = max_heap
    data_dictionary = dd[0]
    # get free_memory list of memory during runtime

    # Create integer list [0...n-1] to help plot allocation
    # TODO: Change this to be based on actual time in program.
    x = []
    for item in data_dictionary["Time"]:
        x.append(float(item))
        x.append(float(item))
    x = np.array(x)  # *2 for tuples

    # Format plot
    plt.xlabel("GC Run : Time in seconds")
    plt.ylabel("Number of memory blocks")
    plt.title("heap allocation throughout runtime")
    plt.legend(list(data_dictionary.keys()))
    # Choose from some color choices. TODO: style colors
    colors = ["royalblue", "cyan", "black", "green", "purple", "lime", "brown", "darkmagenta", "lime", "green"]
    color_index = 0
    # Create the first plot
    plt.figure(1)

    for key in data_dictionary.keys():
        if str(key) != "Time":
            # Get list of the region size before & after every gc run
            pairs = []
            for idx in range(len(data_dictionary[key])):
                pairs.append(int(data_dictionary[key][idx][0]))
                pairs.append(int(data_dictionary[key][idx][1]))
            # Add to the current plot
            plt.plot(np.array(x), np.array(pairs), color=colors[color_index], label=str(key))
            color_index += 1

    # Show plot (without memory)
    plt.legend()  # TODO: test if removing this line does anything
    plt.show()

    # Create second plot: (Just memory during runtime)
    # As heap memory could always be 99% free, seeing the changes in the
    # amonut of free memory in it's own plot is valuable
    # plt.figure(2)
    # plt.plot(x, np.array(free_memory), color = "red", label = "Free Memory")
    # plt.legend()
    # plt.show()

    # Create third plot
    # plt.figure(3)
    # # Add back all information from plot 1
    # for key in data_dictionary.keys():
    #     if str(key) != "Time":
    #         pairs = []
    #         for idx in range(len(data_dictionary[key])):
    #             pairs.append(int(data_dictionary[key][idx][0]))
    #             pairs.append(int(data_dictionary[key][idx][1]))
    #         plt.plot(np.array(x), np.array(pairs), color=colors[color_index], label=str(key))
    #         color_index += 1
    # # add the free memory to the plot
    # plt.plot(x, np.array(free_memory), color="red", label="Free Memory")

    # # Display plot
    # plt.legend()
    # plt.show()


def __sum_allocation(table, keywords, ax, before=False, color="", label=""):

    if not table or not keywords:
        print("__sum_allocation parameters incorrect. Abort.")
        return

    heap_alloc = table

    # get timestamps_seconds from the time keyword in the table. Convert str->float
    timestamps_seconds = list(map(float, heap_alloc["Time"]))

    before_regions = []
    after_regions = []

    # loop through the length of the found allocation changes
    for row in range(len(heap_alloc[keywords[0]])):
        # set up temorary sums to aquire value for each thing we comparing
        after_tsum = 0
        before_tsum = 0
        # match all keys for this row, and find the value
        for key in keywords:
            if before:
                before_tsum += float(heap_alloc[key][row][0])
            else:
                after_tsum += float(heap_alloc[key][row][1])

        if before:
            before_regions.append(before_tsum)
        else:
            after_regions.append(after_tsum)

    # obtain return variables
    allocation = before_regions if before else after_regions
    ax.plot(timestamps_seconds, allocation, color=color, label=label)
    return ax


# Add labels to a heap allocation chart.
# Return updated plot.
def __addLabelsHeap(ax, title):
    ax.set_xlabel("Time passed (seconds)")
    ax.set_ylabel("Regions allocated")
    ax.set_title(title)
    ax.legend()
    return ax
