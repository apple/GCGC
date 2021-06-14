import matplotlib.pyplot as plt
import random
# Making improvements to plot_data.py
# axs is an array of plt.Axes objects.
# think about them as all data associated with a plot
  # TODO: Consider axis :: what should be done along the x and y axis for units?  
def plot_pauses_bar(xdata = [], ydata = [], axs = None, color = "", label = ""):
    if not axs:
        print("No axes supplied. Create one using\nf, axs = matplotlib.pyplot.subplots()")
        return
    # If the color and label parameters have not been passed, use a random color as the new label
    if not color:
        r = random.random()
        b = random.random()
        g = random.random()
        color = (r, g, b)
    if not label:
        label = str(__rgb_to_hex(color))

    axs.bar(x = xdata, height = ydata, color = color, label = label)
    axs.set_ylabel("Pause duration (miliseconds)");
    axs.set_xlabel("Time from program start (seconds)")
    axs.set_title("Pauses during runtime")
    axs.legend()


# Take a rgb tuple triplet, and turn it into a hex code representing the rgb color
def __rgb_to_hex(rgb):
    r = round(rgb[0] * 255)
    g = round(rgb[1] * 255)
    b = round(rgb[2] * 255)
    return "%02x%02x%02x" % (r, g, b)



def get_time_in_seconds(dataframe):
    if dataframe.empty:
        return []
    else:
        return dataframe["TimeFromStart_seconds"]

def get_pauses_in_miliseconds(dataframe):
    if dataframe.empty:
        return []
    else:
        return dataframe["PauseDuration_miliseconds"]
         
def get_combined_xy_pauses(dataframe):
    if dataframe.empty:
        return []
    else:
        time_s    = get_time_in_seconds(dataframe)
        pauses_ms = get_pauses_in_miliseconds(dataframe)
        return time_s, pauses_ms