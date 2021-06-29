import random
import matplotlib.pyplot as plt


def plot_heap_occupancy(
    timedata_seconds=[],
    memorydata=[],
    memorydata_unit="MB",
    heapsize=1,
    heapsize_unit="GB",
    axs=None,
    color=None,
    label=None,
    plot_max=True,
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
    # Plot the maximum heap size during runtime.
    if plot_max:
        x = [0, timedata_seconds[-1]]
        y = [max_heap_size, max_heap_size]
        axs.plot(x, y, color="k", label="Maximum heap size")
    axs.set_ylabel("Heap space in Megabytes (MB)")
    axs.set_xlabel("Time in seconds during program runtime")
    axs.set_title("Heap space used during runtime")
    axs.legend()
    return axs


# Plots how much of the heap is used, as a percentage of the maximum heap size
def plot_heap_occupancy_percentage(
    timedata_seconds=[],
    memorydata=[],
    memorydata_unit="MB",
    heapsize=1,
    heapsize_unit="GB",
    axs=None,
    color=None,
    label=None,
    plot_max=True,
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
    # Transform the data from a number to percentage.
    for i in range(len(memorydata)):
        memorydata[i] = memorydata[i] / max_heap_size * 100
    axs.plot(timedata_seconds, memorydata, color=color, label=label)
    # Plot the maximum heap size during runtime.
    if plot_max:
        x = [0, timedata_seconds[-1]]
        y = [100, 100]
        axs.plot(x, y, color="k", label=("100% : " + str(heapsize) + heapsize_unit))
    axs.set_ylabel("Percentage of heap filled")
    axs.set_xlabel("Time in seconds during program runtime")
    axs.set_title("Percentage of heap space used during runtime")
    axs.legend()
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
