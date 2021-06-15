import matplotlib.pyplot as plt
import random

# Making improvements to plot_data.py
# axs is an array of plt.Axes objects.
# think about them as all data associated with a plot
# TODO: Consider axis :: what should be done along the x and y axis for units?
def plot_pauses_bar(xdata=[], ydata=[], axs=None, color="", label=""):
    if not axs:
        print("No axes supplied. Create one using\nf, axs = matplotlib.pyplot.subplots()")
        return
    # If the color and label parameters have not been passed, use a random color as the new label

    if not label:
        label = "No label provided"
    if not color:
        r = random.random()
        b = random.random()
        g = random.random()
        color = (r, g, b)

    axs.bar(x=xdata, height=ydata, color=color, label=label)
    axs.set_ylabel("Pause duration (miliseconds)")
    axs.set_xlabel("Time from program start (seconds)")
    axs.set_title("Pauses during runtime")
    axs.legend()


def plot_pauses_scatter(xdata=[], ydata=[], axs=None, color="", label=""):
    if not axs:
        print("No axes supplied. Create one using\nf, axs = matplotlib.pyplot.subplots()")
        return
    # If the color and label parameters have not been passed, use a random color as the new label

    if not label:
        label = "No label provided"
    if not color:
        r = random.random()
        b = random.random()
        g = random.random()
        color = (r, g, b)

    axs.scatter(x=xdata, y=ydata, color=color, label=label)
    axs.set_ylabel("Pause duration (miliseconds)")
    axs.set_xlabel("Time from program start (seconds)")
    axs.set_title("Pauses during runtime (scatter)")
    axs.legend()


# Compare multiple plots using a bar graph.
# Parameters:
#   timedata_lists   :  list of [ list of times (x data) to be plotted]
#   heightdata_lists :  list of [ list of heights (y data) to be plotted]
#   label_list       :  list of labels (strings) to describe each passed (x/y) data list
#   colors(optional) :  list of colors to plot for each list passed. None => random colors
#   axs(optional)    :  plot with existing metadata. None => new figure created
def plot_bar_comparison(timedata_lists=[], heightdata_lists=[], label_list=[], colors=None, axs=None):
    if not timedata_lists:
        print("No timedata list in function plot_bar_comparison()")
        return
    if not heightdata_lists:
        print("No heightdata list in plot_bar_comparison()")
        return
    if not label_list:
        print("No label list in plot_bar_comparison()")
    if len(timedata_lists) != len(heightdata_lists):
        print("Length of timedata_lists and heightdata_lists do not match.", end="")
        print("timedata_lists: " + str(len(timedata_lists)) + ", heightdata_lists: " + str(len(heightdata_lists)))
        return
    if len(timedata_lists) != len(label_list):
        print("Length of timedata_lists and label_list do not match.", end="")
        print("timedata_lists: " + str(len(timedata_lists)) + ", label_list: " + str(len(label_list)))
        return
    if not colors:
        colors = []
    if not axs:
        fig, axs = plt.subplots()

    while len(colors) < len(timedata_lists):
        colors.append(None)

    for i in range(len(timedata_lists)):
        plot_pauses_bar(
            timedata_lists[i],
            heightdata_lists[i],
            axs,
            colors[i],
            label_list[i],
        )
    return axs

def plot_pauses_bar(xdata=[], ydata=[], axs=None, color="", label=""):
    