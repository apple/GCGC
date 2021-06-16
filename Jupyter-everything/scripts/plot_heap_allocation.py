import re
import numpy as np
import random

# from scripts import updated_parse_log as pl
import matplotlib.pyplot as plt

## # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#                   plot_heap_allocation_breakdown                             #
#                                                                              #
#   Purpose:                                                                   #
#       Print a graph showing the heap breakdown throughout runtime            #
#   Parameters:                                                                #
#        region_descriptions: Holds data about region breakdown during runtime #
## # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# TODO: This is very hard to understand function. WILL FIX SOON
# THE TIME TO FIX IS NOW!!!! TODO when back! :D


def plot_heap_regions(region_descriptions, axs=None, region_size=None):
    if not region_descriptions:
        print("No data passed into plot_heap_allocation_breakdown")
        return
    # determine data arrangement from list length
    # Robust arrangements will have type 'list'.
    # Non robust arrangements will have type 'dict'
    if type(region_descriptions) == dict:
        return plot_heap_regions_normal(region_descriptions, axs, region_size)
    elif type(region_descriptions) == list:
        return plot_heap_regions_robust(region_descriptions, axs, region_size)
    else:
        print("Unkown region_descriptions datatype. Abort.")
    return


# TODO: base the following information on time.
# It should not be too hard to do, its just nice to view data before doing that.
# Parameters:
#   region_descriptions   :  list of amount in the heap at each moment in time, before and after gc.
#   axs  (optional)       : matplotlib plot
#   region_size (optional): The size in MB of each region. Allows for plotting memory allocation rather than regions
def plot_heap_regions_robust(region_descriptions, axs=None, region_size=None):

    # Remove all 'after' gc collection data points, which appear every other entry.
    ###############################################################
    # The following removes every other entry for each region, as to only contain
    # the region size BEFORE garbage collection runs. I think I would like to make
    # this a permanant feautre, but imm not sure.

    for region in range(len(region_descriptions)):
        without_after_gc = []
        for index in range(len(region_descriptions[region])):
            if (index) % 2:
                without_after_gc.append(region_descriptions[region][index])
        region_descriptions[region] = without_after_gc
    ###############################################################
    if not axs:
        fig, axs = plt.subplots()
    # Create helper list [0...n-1] to plot for x axis based on time?
    x = np.array(list(range(len(region_descriptions[0]))))

    # Order matters here, associated with order collected this data.
    # TODO: Remove dependence on Order, use dictionary instead if possible
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
    colors = ["royalblue", "cyan", "black", "red", "purple", "purple", "brown", "darkmagenta", "lime", "green"]
    axs.set_xlabel("GC Run number (not based on time)")

    if region_size:
        axs.set_ylabel("Megabytes allocated")
    else:
        axs.set_ylabel("Number of memory blocks")
    axs.set_title("heap allocation throughout runtime")
    axs.legend(region_names)

    # Plot information for each region
    for idx in range(len(region_descriptions)):
        if region_size:
            axs.plot(
                x,
                np.array(list(row * region_size for row in region_descriptions[idx])),
                color=colors[idx],
                label=region_names[idx],
            )
        else:
            axs.plot(
                x, np.array(list(row for row in region_descriptions[idx])), color=colors[idx], label=region_names[idx]
            )
    axs.legend()
    return axs


## # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#                   plot_heap_regions_normal                                   #
#   Purpose:                                                                   #
#       Plot the heap breakdown throughout program using memory collected      #
#       following a log schema0. Display 3 plots                               #
#       -> Memory regions during runtime (without free memory)                 #
#       -> Free heap memory regions                                            #
#       -> Memory regions + free regions during runtime                        #
## # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def plot_heap_regions_normal(region_descriptions, axs=None, region_size=None):
    if not region_descriptions:
        print("No data passed into plot_heap_regions_normal.")
        return
    # Create integer list [0...n-1] to help plot allocation
    x = []
    for item in region_descriptions["Time"]:
        x.append(float(item))
    x = np.array(x)
    if not axs:
        fig, axs = plt.subplots()
    # Format plot
    axs.set_xlabel("Program runtime in seconds")
    if region_size:
        axs.set_ylabel("Memory allocation in MB")
    else:
        axs.set_ylabel("Memory allocation in number of regions")

    axs.set_title("Heap allocation before GC collection")
    axs.legend(list(region_descriptions.keys()))
    # Choose from some color choices. TODO: style colors
    colors = ["royalblue", "cyan", "black", "green", "purple", "lime", "brown", "darkmagenta", "lime", "green"]
    color_index = 0
    # Create the first plot

    for key in region_descriptions.keys():
        if str(key) != "Time":
            # Get list of the region size before & after every gc run
            pairs = []
            for idx in range(len(region_descriptions[key])):
                pairs.append(int(region_descriptions[key][idx][0]))
                # pairs.append(int(region_descriptions[key][idx][1])) # We dont care to see the after GC data at this time for a regional collector's regions.
            # Add to the current plot
            if region_size:
                axs.plot(
                    np.array(x),
                    np.array([pair * region_size for pair in pairs]),
                    color=colors[color_index],
                    label=str(key),
                )
            else:
                axs.plot(np.array(x), np.array(pairs), color=colors[color_index], label=str(key))
            color_index += 1

    # Show plot (without memory)
    axs.legend()  # TODO: test if removing this line does anything


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
def __addLabelsHeap(axs, title):
    axs.set_xlabel("Time passed (seconds)")
    axs.set_ylabel("Regions allocated")
    axs.set_title(title)
    axs.legend()
    return axs


def plot_heap_allocation_outof_max(
    timedata_seconds=[],
    memorydata=[],
    memorydata_unit="MB",
    heapsize=1,
    heapsize_unit="GB",
    axs=None,
    color=None,
    label=None,
):
    max_heap_size = __get_standardized_unit_size(heapsize, heapsize_unit)
    for i in range(len(memorydata)):
        memorydata[i] = __get_standardized_unit_size(memorydata[i], memorydata_unit)
    if not axs:
        f, axs = plt.subplots()
    if not color:
        color = (random.random(), random.random(), random.random())
    if not label:
        label = "Current heap usage"
    axs.plot(timedata_seconds, memorydata, color=color, label=label)
    return axs


def __get_standardized_unit_size(value, unit):
    # We will convert everything to MB

    if unit == "M":
        return value
    if unit == "G":
        return value * 1000
    if unit == "MB":
        return value
    if unit == "GB":
        return value * 1000
    if unit == "KB":
        return value / 1000
    print('Warning: Unkown unit "' + unit + '"')
    return value
