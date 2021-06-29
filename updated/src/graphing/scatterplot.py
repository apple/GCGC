from __generic_mapping import __generic_plotting
import random


def plot_pauses_scatter(xdata=[], ydata=[], axs=None, color="", label="", optional=None):
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
    axs.set_title("Pauses during runtime in miliseconds over time (scatter)")
    axs.grid()
    axs.legend()


def comparrison_scatter(xdata_list, ydata_list, axs=None, colors=[], labels=[]):
    return __generic_plotting(xdata_list, ydata_list, axs, colors, labels, plot_pauses_scatter)
