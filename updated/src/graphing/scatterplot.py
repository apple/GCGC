#       scatterplot.pt
#
#   Plots scatterplot based on input parameters. Used to simplify labels and plotting on
#   the same graph, as needed.
#
#   Ellis Brown, 6/29/2021

from graphing.__generic_mapping import __generic_plotting
import matplotlib.pyplot as plt
import random

#       plot_pauses_scatter
#
#   Creates a scatter plot from the provided data.
#
def plot_pauses_scatter(xdata=[], ydata=[], axs=None, color="", label="", optional=None):
    assert isinstance(xdata, list)
    assert isinstance(ydata, list)
    if not axs:
        print("No axes supplied. Create one using\nf, axs = matplotlib.pyplot.subplots()")
        return
    # If the color and label parameters have not been passed, use a random color as the new label
    if not label:
        label = "No label provided"
    if not color:
        color = (random.random(), random.random(), random.random())  # random color
    # Create amd label the plot
    axs.scatter(x=xdata, y=ydata, color=color, label=label)
    axs.set_ylabel("Pause duration (miliseconds)")
    axs.set_xlabel("Time from program start (seconds)")
    axs.set_title("Pauses during runtime in miliseconds over time (scatter)")
    axs.grid()
    axs.legend()
    return axs


#       comparrison_scatter
#
#   Takes multiple lists of scatterplot data, to be plotted on the same figure, and applies the
#   the plot_pauses_scatter function to all.
#
#   Implementation note: __generic_plotting just confirms that the parameters are successful, then calls
#   plot_pauses_scatter for all entries in xdata_list and ydata_list
#
def comparrison_scatter(xdata_list, ydata_list, axs=None, colors=[], labels=[]):
    return __generic_plotting(xdata_list, ydata_list, axs, colors, labels, plot_pauses_scatter)
