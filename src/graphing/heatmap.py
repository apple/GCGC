#       filename
#
#   Using parsed data in a gc_event_dataframe, creates heatmaps to visually
#   show latency during runtime.
#
#   Ellis Brown, 6/29/2021

import matplotlib
from matplotlib import pyplot as plt
import numpy as np

# TODO: Most of this code is borrowed. Read and update documentation
# to be consistent to my personal style.

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#                     plot_heatmap()                            #
#   Purpose:                                                    #
#       Plot a latency heatmap for pauses during runtime.       #
#   Parameters:                                                 #
#       table : a table containing pause info and time info     #
#       num_b : number of buckets along both axis for heat map  #
#       labels: True means add frequency labels inside heatmap  #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def plot_heatmap(heatmap, dimensions, labels=True):

    width = dimensions[0]  # x_bucket_count
    height = dimensions[1]  # y_bucket_count
    max_pause_ms = height * dimensions[3]
    max_time_ms = width * dimensions[2]
    min_pause_ms = 0
    multipler = max_time_ms / width  # multipler is the size of a bucket for time direction

    # x labels are the time labels
    time_labels = [num * multipler for num in range(1, width + 1)]  # TODO : UPDATE TO BE FASTER

    time_labels_temp = []
    for i in range(len(time_labels)):
        if not i % 2:
            time_labels_temp.append(str(round(time_labels[i], 2)) + " s")
        else:
            time_labels_temp.append("")

    # time_labels = [str(round(label, 2)) + " s" for label in time_labels]
    time_labels = time_labels_temp

    # size of the buckets for ms pause
    multipler = (max_pause_ms - min_pause_ms) / height
    # y labels are ms pause time labels
    latency_labels = [round((num * multipler) + min_pause_ms, 2) for num in reversed(range(1, height + 1))]
    latency_labels = [str(label) + " ms" for label in latency_labels]

    ## Create a figure, and add data to heatmap. Plot then show heatmap.
    fig, ax = plt.subplots()
    ax.set_title("Latency during runtime.")
    # cmap is the color scheme. To change the heatmap color scheme, use a color scheme from here:
    # https://matplotlib.org/stable/tutorials/colors/colormaps.html
    im = heatmap_make(heatmap, latency_labels, time_labels, ax=ax, cmap="plasma_r", cbarlabel="Frequency")
    if labels:
        __annotate_heatmap(im, valfmt="{x}")
    fig.tight_layout()
    return ax
    ## end new
    """
    fig, ax = plt.subplots()
    im = ax.imshow(np.array(heatmap))

    # EVERYTHING ELSE BELOW IS TAKEN FROM MATPLOTLIB DOCUMENTATION
    # SEE HERE: https://matplotlib.org/stable/gallery/images_contours_and_fields/image_annotated_heatmap.html 

    # We want to show all ticks...
    ax.set_xticks(np.arange(len(time_labels))) # x axis
    ax.set_yticks(np.arange(len(latency_labels))) # y axis
    # ... and label them with the respective list entries
    ax.set_xticklabels(time_labels)
    ax.set_yticklabels(latency_labels)

    # Rotate the tick labels and set their alignment.
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
             rotation_mode="anchor")
    # Loop over data dimensions and create text annotations.
    for i in range(len(latency_labels)):
        for j in range(len(time_labels)):
            text = ax.text(j, i, heatmap[i, j],
                           ha="center", va="center", color="w")

    

    fig.tight_layout()
    plt.show()
    """


################################################
# Gathers data to properly plot a heatmap.
# Parameters:
#   table: a pandas dataframe.  Notable columns:
#       TimeFromStart_seconds - time in seconds from program start. float
#       PauseDuration_miliseconds - time in miliseconds for a pause. float
#   num_b : number of buckets to sort time into.
#       Note: More buckets = more percise heatmap, labels less clear.
################################################
def __get_heatmap(table, width=20, height=20):
    if table.empty:
        return
    # access the two columns from the table with our time/pause info
    timestamps_seconds = table["TimeFromStart_seconds"]
    pauses_ms = table["PauseDuration_miliseconds"]

    # create buckets to store the time information.
    # first, compress into num_b buckets along the time X-axis.
    x_b = [[] for i in range(width)]
    max_time_ms = list(timestamps_seconds)[-1]
    bucket_time_duration = max_time_ms / width

    # populate buckets along the x axis.
    for pause, time in zip(pauses_ms, timestamps_seconds):
        bucket_no = int(time / bucket_time_duration)
        if bucket_no >= width:
            bucket_no = width - 1
        x_b[bucket_no].append(pause)

    max_pause_ms = max(pauses_ms)
    min_pause_ms = min(pauses_ms)

    # calculate the size of the buckets representing a pause
    bucket_pause_duration = (max_pause_ms - min_pause_ms) / height

    # create heatmap, which will be a 2d-array
    heatmap = []

    # go through each time interval, and sort the pauses there into frequency lists
    for bucket in x_b:
        yb = [0 for i in range(height)]  # construct a 0 frequency list
        for time in bucket:
            # determine which ms pause bucket
            y_bucket_no = int((time - min_pause_ms) / bucket_pause_duration)
            if y_bucket_no >= height:
                y_bucket_no = height - 1

            # increase the frequency of that pause in this time interval
            yb[y_bucket_no] += 1

        # Add the data to the 2d array
        heatmap.append(yb)
    heatmap = np.rot90(heatmap)  # fix orientation
    return np.array(heatmap), min_pause_ms, max_pause_ms, max_time_ms  # all data needed to plot a heatmap.


from mpl_toolkits.axes_grid1 import make_axes_locatable

## The following code block was taken directly from matplotlib's documentation
## seen here:
# https://matplotlib.org/stable/gallery/images_contours_and_fields/image_annotated_heatmap.html
def heatmap_make(data, row_labels, col_labels, ax=None, cbar_kw={}, cbarlabel="", **kwargs):
    """
    Create a heatmap from a numpy array and two lists of labels.

    Parameters
    ----------
    data
        A 2D numpy array of shape (N, M).
    row_labels
        A list or array of length N with the labels for the rows.
    col_labels
        A list or array of length M with the labels for the columns.
    ax
        A `matplotlib.axes.Axes` instance to which the heatmap is plotted.  If
        not provided, use current axes or create a new one.  Optional.
    cbar_kw
        A dictionary with arguments to `matplotlib.Figure.colorbar`.  Optional.
    cbarlabel
        The label for the colorbar.  Optional.
    **kwargs
        All other arguments are forwarded to `imshow`.
    """

    if not ax:
        ax = plt.gca()

    # Plot the heatmap
    im = ax.imshow(data, **kwargs)

    # Create colorbar
    #

    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="5%", pad=0.1)
    plt.colorbar(im, cax=cax)

    # cbar = ax.figure.colorbar(im, ax=ax, **cbar_kw)
    cax.set_ylabel(cbarlabel, rotation=-90, va="bottom")

    # We want to show all ticks...

    ax.set_xticks(np.arange(data.shape[1]))
    ax.set_yticks(np.arange(data.shape[0]))
    # ... and label them with the respective list entries.
    ax.set_xticklabels(col_labels)
    ax.set_yticklabels(row_labels)

    # Let the horizontal axes labeling appear on top.
    ax.tick_params(top=False, bottom=True, labeltop=False, labelbottom=True)

    # Rotate the tick labels and set their alignment.
    plt.setp(ax.get_xticklabels(), rotation=-30, ha="left", rotation_mode="anchor")

    # Turn spines off and create white grid.
    ax.spines[:].set_visible(False)

    ax.set_xticks(np.arange(data.shape[1] + 1) - 0.5, minor=True)
    ax.set_yticks(np.arange(data.shape[0] + 1) - 0.5, minor=True)
    ax.grid(which="minor", color="w", linestyle="-", linewidth=3)
    ax.tick_params(which="minor", bottom=False, left=False)

    return im


# The following code example is taken directly from matplotlib documentation
# on heat maps, seen below
# https://matplotlib.org/stable/gallery/images_contours_and_fields/image_annotated_heatmap.html
def __annotate_heatmap(im, data=None, valfmt="{x}", textcolors=("black", "white"), threshold=None, **textkw):
    """
    A function to annotate a heatmap.

    Parameters
    ----------
    im
        The AxesImage to be labeled.
    data
        Data used to annotate.  If None, the image's data is used.  Optional.
    valfmt
        The format of the annotations inside the heatmap.  This should either
        use the string format method, e.g. "$ {x:.2f}", or be a
        `matplotlib.ticker.Formatter`.  Optional.
    textcolors
        A pair of colors.  The first is used for values below a threshold,
        the second for those above.  Optional.
    threshold
        Value in data units according to which the colors from textcolors are
        applied.  If None (the default) uses the middle of the colormap as
        separation.  Optional.
    **kwargs
        All other arguments are forwarded to each call to `text` used to create
        the text labels.
    """

    if not isinstance(data, (list, np.ndarray)):
        data = im.get_array()

    # Normalize the threshold to the images color range.
    if threshold is not None:
        threshold = im.norm(threshold)
    else:
        threshold = im.norm(data.max()) / 2.0

    # Set default alignment to center, but allow it to be
    # overwritten by textkw.
    kw = dict(horizontalalignment="center", verticalalignment="center")
    kw.update(textkw)

    # Get the formatter in case a string is supplied
    if isinstance(valfmt, str):
        valfmt = matplotlib.ticker.StrMethodFormatter(valfmt)

    # Loop over the data and create a `Text` for each "pixel".
    # Change the text's color depending on the data.
    texts = []
    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            kw.update(color=textcolors[int(im.norm(data[i, j]) > threshold)])
            text = im.axes.text(j, i, valfmt(data[i, j], None), **kw)
            texts.append(text)

    return texts

import pandas as pd
###########
#       get_heatmap_data
#
#   Create a 2d numpy array, and dimensions list associated with a gc_event_dataframe, such that
#   the 2d array represents the frequencies of latency events, based on the specified dimensions.
def get_heatmap_data(timestamp_groups, datapoint_groups, labels, dimensions):
    if len(dimensions) != 4:
        print("""Dimensions incorrect.
        Dimensions must be a list following the format:
        dimensions[0] = number of x buckets
        dimensions[1] = number of y buckets
        dimensions[2] = duration of x bucket
        dimensions[3] = duration of y bucket """)   
        return np.array([]), []
    x_bucket_count    = dimensions[0]  # Number of time intervals to group gc events into. INT ONLY
    y_bucket_count    = dimensions[1]  # Number of latency time intervals to group events into. INT ONLY
    x_bucket_duration = dimensions[2]  # Duration in seconds that each time interval bucket has for gc event timestamps
    y_bucket_duration = dimensions[3]  # Duration in miliseconds for the length of each latency interval bucket
    
    for x in [x_bucket_count, y_bucket_count]:
        assert type(x) == int, "Warning: x_bucket_count and y_bucket_count must be integers"

    for x in [x_bucket_duration, y_bucket_duration]:
        assert (
            type(x) == int or type(x) == float
        ), "Warning: x_bucket_duration and y_bucket_duration must be floats or integers"
    for x in [x_bucket_count, y_bucket_count, x_bucket_duration, y_bucket_duration]:
        if x <= 0:
            print("Warning: All dimensions must be greater than zero.")
            return np.array([]), []

    heatmap_list = []
    for times_seconds, pauses_ms, label in zip(timestamp_groups, datapoint_groups, labels):
        if not list(times_seconds) or not list(pauses_ms):
            continue # Skip this loop iteration


        # create buckets to store the time information.
        # first, compress into num_b buckets along the time X-axis.
        x_b = [[] for i in range(x_bucket_count)]

        out_of_range_time = False
        # populate buckets along the x axis.
        for pause, time in zip(pauses_ms, times_seconds):
            bucket_no = int(time / x_bucket_duration)
            
           
            if bucket_no == x_bucket_count:
                bucket_no = x_bucket_count - 1
                x_b[bucket_no].append(pause)
            
            elif bucket_no < x_bucket_count:
                x_b[bucket_no].append(pause)
            else:
                out_of_range_time = True

        # create heatmap, which will be a 2d-array
        heatmap = []
        out_of_range_latency = False
        max_value = 0
        
        for pause in pauses_ms:
            if pause:
                max_value = max(pause, max_value)
        
        # go through each time interval, and sort the pauses there into frequency lists
        for bucket in x_b:
            yb = [0 for i in range(y_bucket_count)]  # construct a 0 frequency list
            for time in bucket:
                # determine which ms pause bucket
                if time:
                    y_bucket_no = int(time / y_bucket_duration)
                
                    
                    
                    if y_bucket_no < y_bucket_count:
                        # increase the frequency of that pause in this time interval
                        yb[y_bucket_no] += 1
                    elif y_bucket_no == y_bucket_count:
                        y_bucket_no = y_bucket_count - 1
                        yb[y_bucket_no] += 1
                    else:
                        out_of_range_latency = True



            # Add the data to the 2d array
            heatmap.append(yb)
        heatmap = np.rot90(heatmap)  # fix orientation
        
        if out_of_range_time:
            print(label + " Warning: At least one value lies outside of the provided time range. Max value outside range: " + str (max(times_seconds)))
        if out_of_range_latency:
            print(label + " Warning: At least one value lies outside the provided range for latency. Max value outside range: " + str(max_value))
        
        heatmap_list.append(heatmap)
        if not heatmap_list:
            print("Warning! No heatmap list analyze_logs_dev 384")
    return heatmap_list, dimensions



# Access a Pandas gc_event_dataframe constructed through parse_data.py with labeled columns.
# Return the timestamps and pauses as a list
def get_time_and_event_durations(gc_event_dataframe):
    assert isinstance(gc_event_dataframe, pd.DataFrame)
    return get_time_in_seconds(gc_event_dataframe), get_event_durations_in_miliseconds(gc_event_dataframe)


#       get_event_durations_in_miliseconds
#
#   Given a pandas dataframe table populated with parsed log information,
#   extract all 'event durations' from the Duration_miliseconds column, and
#   return them as a list of floats.
#
def get_event_durations_in_miliseconds(gc_event_dataframe):
    assert isinstance(gc_event_dataframe, pd.DataFrame)
    if gc_event_dataframe.empty:
        return []
    else:
        durations_miliseconds = []
        for duration in gc_event_dataframe["Duration_miliseconds"]:
            if duration != None:
                durations_miliseconds.append(float(duration))
        return durations_miliseconds


#       get_time_in_seconds
#
#   Given a pandas dataframe table populated with parsed information, exact only
#   the time since program start timestamps, and return them as a list of floats
#
def get_time_in_seconds(gc_event_dataframe):
    assert isinstance(gc_event_dataframe, pd.DataFrame)
    if gc_event_dataframe.empty:
        return []
    else:
        timestamps_seconds = []
        if "TimeFromStart_seconds" in gc_event_dataframe:
            for time in gc_event_dataframe["TimeFromStart_seconds"]:
                if time != None:
                    timestamps_seconds.append(float(time))
        return timestamps_seconds

