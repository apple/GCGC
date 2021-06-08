#############################################################################
##                          plot_data.py
##  Defines functions to plot tables of information collected from logs.
##  
##  Author: Ellis Brown, 6/1
##  TODO: Define a general type chart, plots any table 
#############################################################################
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from scripts import parse_log as pl

# Set the size of the figures that appear in the Jupyter notebook
plt.rcParams['figure.figsize'] = [12, 7]

## # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#                               plot_pauses
#   Purpose:
#       plots the pauses due to gc across full runtime
#   
#   Parameters:
#       table: a table, with columns as categories
#           columns as follows: --
#       datetime (optional), time, [info/debug/...], gc phase, pause time
#   
#   Return:
#       None: Creates multiple tables showing the pauses over runtime, and 
#             table with trends within the data
#
## # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def plot_pauses(table):
    # Obtain X Y list information from the dataframe.
    pauses = list(map(float, table["PauseDuration"]))
    timestamps = list(map(float, table["TimeFromStart"]))

    # Show interesting trends
    total_wait = __find_trends(pauses)
    
    total_time = pl.getTotalProgramRuntime()
    print("Total time: " + str(total_time) + "\n")
    print("Total program runtime: " + str(total_time) + " seconds" + "\n")
    throughput = (total_time - (total_wait)/1000) / (total_time)
    print("Throughput: " + str(round(throughput * 100, 4)) + "%" + "\n")
    __get_percentile_table(pauses)
    
    # # # # # # # # # # # # # # # # # # # #
    # Plot 1: Pauses over program's entire runtime.
    plt.bar(x = np.array(timestamps), height= np.array(pauses), width = 2.0)
    plt.ylabel("Pause duration (miliseconds)");
    plt.xlabel("Time from program start (seconds)")
    plt.title("Pauses for Young Generation GC")
    plt.show()
    # # # # # # # # # # # # # # # # # # # # #
    # # Plot 2: Pauses showing duration, no timestamps
    # timestamps = list(map(int, list(range(len(pauses)))))
    # plt.bar(x = timestamps, height= pauses)
    # plt.ylabel("Pause duration (miliseconds)");
    # plt.xlabel("Pause listed in order")
    # plt.title("Pauses for Young Generation GC")
    # plt.show()
    # # # # # # # # # # # # # # # # # # # # #


## # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#                               __find_trends
#   Purpose:
#       Finds trends for pause data in a dataset
#   
#   Parameters:
#       table: a table, with columns as categories
#       --table should contaain the following columns
#   
#       datetime (optional), time, [info/debug/...], gc phase, pause time
#   
#   Return:
#       None: Creates a table showing the interesting ascii values
#
## # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Finds trends in dataframe. 
# Column 1 must be pause time, (1 indexed)
# Column 4 must be time since start of program.
def __find_trends(pauses):
    
    
    max_wait = max(pauses, key = lambda i : float(i))
    total_wait   = round(sum(float(i) for i in pauses), 4)
    average_wait = round(total_wait / len(pauses), 4)
    
    print("Total pauses: " + str(len(pauses))  + "\n")
    
    print("Max wait: " + str(max_wait) + " ms\n")
    
    print("Total wait: " + str(total_wait) + " ms\n")
    
    print("Average (mean) wait: " + str(average_wait) + " ms\n")

    
    return total_wait


## # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#                           __get_percentile_table
#   Purpose:
#       Given a well formatted table of pause time information, print ascii
#       table showing the percentile of the pause times.
#   
#   Parameters:
#       table: a table, with columns as categories
#       --table should contaain the following columns
#   
#       datetime (optional), time, [info/debug/...], gc phase, pause duration,
#                                                                   pause type
#   Return:
#       None: Creates a table showing the interesting ascii values
## # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def __get_percentile_table(pauses):
    pauses = sorted(pauses, reverse = True)
    print("---------------------------\nPause time in ms\n---------------------------")
    print("50 th percentile: ", round(np.percentile(pauses, 50), 4))
    print("75 th percentile: ", round(np.percentile(pauses, 75), 4))
    print("90 th percentile: ", round(np.percentile(pauses, 90), 4))
    print("95 th percentile: ", round(np.percentile(pauses, 95), 4))
    print("99 th percentile: ", round(np.percentile(pauses, 99), 4))
    print("99.9  percentile: ", round(np.percentile(pauses, 99.9), 4))
    print("99.99 percentile: ", round(np.percentile(pauses, 99.99), 4))
    return 

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
def plot_heap_allocation_breakdown(breakdown_lst, max_heap = 0):
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
    region_names = ["Free", "Young", "Survivor", "Old", "Humongus_start", 
                    "Humongus_continue", "Collection_set",  
                    "Open_archive", "Closed_archive", "TAMS"]

    # Add titles and format style to plot
    colors = ["royalblue", "cyan", "black", "green", "purple", "lime", "brown", "darkmagenta", "lime", "green"]
    plt.xlabel("GC Run number (not based on time)")
    plt.ylabel("Number of memory blocks")
    plt.title("heap allocation throughout runtime")
    plt.legend(region_names)
    # Plot information for each region
    for idx in range(len(allocation_summary[0])):
        plt.plot(x, np.array(list(row[idx] for row in allocation_summary)), color = colors[idx], label = region_names[idx])
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
def __plot_HA_schema0(dd, max_heap = 0):
    
    if (not dd) or (len(dd) < 2) or (not dd[0]) :
        return
    if (not dd):
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
    print("This far")
    data_dictionary = dd[0]
    # get free_memory list of memory during runtime
    free_memory = __calculate_freemem(data_dictionary, dd[1], before = True, after = True) 
    
    # Create integer list [0...n-1] to help plot allocation
    # TODO: Change this to be based on actual time in program.
    x = []
    for item in data_dictionary["Time"]:
        x.append(float(item))
        x.append(float(item))
    x = np.array(x) # *2 for tuples
    
    # Format plot
    plt.xlabel("GC Run : Time in seconds")
    plt.ylabel("Number of memory blocks")
    plt.title("heap allocation throughout runtime")
    plt.legend(list(data_dictionary.keys()))
    # Choose from some color choices. TODO: style colors
    colors = ["royalblue", "cyan", "black", "green", "purple", 
              "lime", "brown", "darkmagenta", "lime", "green"]
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
            plt.plot(np.array(x), np.array(pairs), color = colors[color_index], label = str(key))
            color_index += 1
    
    # Show plot (without memory)
    plt.legend()                    #TODO: test if removing this line does anything
    plt.show()

    # Create second plot: (Just memory during runtime)
    # As heap memory could always be 99% free, seeing the changes in the
    # amonut of free memory in it's own plot is valuable 
    # plt.figure(2)
    # plt.plot(x, np.array(free_memory), color = "red", label = "Free Memory")
    # plt.legend()
    # plt.show() 

    # Create third plot
    plt.figure(3)
    # Add back all information from plot 1
    for key in data_dictionary.keys():
        if str(key) != "Time":
            pairs = []
            for idx in range(len(data_dictionary[key])):
                pairs.append(int(data_dictionary[key][idx][0]))
                pairs.append(int(data_dictionary[key][idx][1]))
            plt.plot(np.array(x), np.array(pairs), color = colors[color_index], label = str(key))
            color_index += 1
    # add the free memory to the plot
    plt.plot(x, np.array(free_memory), color = "red", label = "Free Memory")
    
    # Display plot
    plt.legend()
    plt.show() 


## # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#                   __calculate_freemem                                        #
#   Purpose:                                                                   #
#       Creates a list of the free memory chunks throughout a                  #
#       program's runtime based on the starting values                         #
#   Parameters:                                                                #
#       data_dictionary : dictionary containing the free regions               #
#                           (keys):   name of each type of data region         #
#                         (values):   tuple containing before/after count for  #
#                                     the region.                              #
#       inital_free     : integer value with the inital number of free regions #
#                                                                              #
#   Return: list with the # of free regions sequentially. Memory recorded      #
#           directly before and after each garbage collection pause.           #
## # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def __calculate_freemem(data_dictionary, inital_free, before = False, after = False):
    if not data_dictionary:
        return []

    free_mem = []
    keys = list(data_dictionary.keys())
    # if any sections did not collect data, remove them.
    for i in range(len(keys)):
        if not data_dictionary[keys[i]]:
            del data_dictionary[keys[i]]

    for idx in range(len(data_dictionary["Eden"])):
        
        # Calculate the free memory before the GC runs
        if before:
            temp_val = 0
            for key in data_dictionary.keys():
                if str(key) != "Time":
                                            # access tuple [0] from list
                                            # of tuples associated with key
                    temp_val += int(data_dictionary[key][idx][0])
            free_mem.append(int(inital_free - temp_val))
        
        # Calculate the free memory after the GC runs
        if after:
            temp_val = 0
            for key in data_dictionary.keys():
                if str(key) != "Time":
                    temp_val += int(data_dictionary[key][idx][1])
            free_mem.append(int(inital_free - temp_val))

    return free_mem

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
#                      displayMetadata()                      #
#   Purpose:                                                  #
#       Take the metadata collected, and print in a well      #
#       formatted table using ASCII characters                #
#   Parameters:                                               #
#       metadata : a table containing title-value pairs       #
#                  title :   The type of the metadata item    #
#                  values:  The value of the metadata item    #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def displayMetadata(table):
    # table is a list of lists
    # [ [title, value], [title, value], ... ]
    
    # determine line length for formatting.
    max_title_len = max([len(item[0]) for item in table])

    for item in table:
        # Start with title 
        print(item[0] +" ", end="")
        
        # Determine if an extra whitespace is needed, from even/odd lines
        whitespace_length = max_title_len - len(item[0])
        if (whitespace_length % 2 == 1):
            print(" ", end="")
        
        # Print formatting based on item length, then print the value
        print(int((max_title_len - len(item[0])) / 2) * ". " + "| " + str(item[1]))
    

# Currently only defined on Schema 0    
def heap_allocation_beforeafter_gc(breakdown_lst, max_heap = 0):
    if not breakdown_lst:
        return
    data = breakdown_lst[0]
    if not breakdown_lst[1]:
        breakdown_lst[1] = max_heap
    free_memory_before = __calculate_freemem(data, breakdown_lst[1], before = True)
    free_memory_after = __calculate_freemem(data, breakdown_lst[1], after = True)
    x = []
    for item in data["Time"]:
        x.append(float(item))
    x = np.array(x)
    ## basic plot setup ##
    plt.xlabel("Time in seconds")
    plt.ylabel("Number of memory blocks")
    plt.title("Heap allocation BEFORE gc")
    plt.legend(list(data.keys()))
    # Choose from some color choices. TODO: style colors
    colors = ["royalblue", "cyan", "black", "green", "purple", 
              "lime", "brown", "darkmagenta", "lime", "green"]
    color_index = 0
    # Create the first plot
    plt.figure(1)
    afterl = []
    labels = []
    #########################
    for key in data.keys():
        if str(key) != "Time":
            before = []
            after = []
            
            for idx in range(len(data[key])):
                before.append(int(data[key][idx][0]))
                after.append(int(data[key][idx][1]))
            plt.plot(np.array(x), np.array(before), color = colors[color_index], label = str(key))
            color_index += 1
            afterl.append(after)
            labels.append(str(KeysView))
    plt.plot(x, np.array(free_memory_before), color = "red", label = "Free Memory")            
    plt.legend()                    #TODO: test if removing this line does anything
    plt.show()
    print("\n\n")
    ###############
    ### Figure 2 ##
    ###############
    plt.figure(2)
    plt.xlabel("Time in seconds")
    plt.ylabel("Number of memory blocks")
    plt.title("Heap allocation AFTER gc")
    
    color_index = 0
    for i in range(len(afterl)):
        plt.plot(x, np.array(afterl[i]), color = colors[color_index], label = labels[i])
        color_index += 1

    plt.plot(x, np.array(free_memory_after), color = "red", label = "Free Memory")
    plt.legend()
    plt.show()

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
#                     plot_heatmap()                            #
#   Purpose:                                                    #
#       Plot a latency heatmap for pauses during runtime.       #
#   Parameters:                                                 #
#       table : a table containing pause info and time info     #
#       num_b : number of buckets along both axis for heat map  #
#       labels: True means add frequency labels inside heatmap  #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def plot_heatmap(table, num_b = 20, labels = True):
    if not table:
        print("No table passed to function plot_heatmap. Abort")
    
    heatmap, min_pause, max_pause, max_time = __get_heatmap(table, num_b)
    # for column in heatmap:
    #     for item in column:
    #         print(item, end=" ")
    #     print("")
        
    # print("\n\n")
    heatmap = np.rot90(heatmap) # fix orientation
   
    # for column in heatmap:
    #     for item in column:
    #         print(item, end=" ")
    #     print("")
    
    multipler = max_time / num_b  # multipler is the size of a bucket for time direction
    # x labels are the time labels
    x_labels = [num * multipler for num in range(num_b)]# TODO : UPDATE TO BE FASTER
    x_labels = [str(round(label, 2)) + " s" for label in x_labels]

    # size of the buckets for ms pause
    multipler = (max_pause - min_pause) / num_b
    # y labels are ms pause time labels
    y_labels = [round((num * multipler) + min_pause, 2) for num in reversed(range(num_b))] 
    y_labels = [str(label) + " ms" for label in y_labels]
    
    ## Create a figure, and add data to heatmap. Plot then show heatmap.
    fig, ax = plt.subplots()
    ax.set_title("Latency during runtime.")
    im, cbar = heatmap_make(heatmap, y_labels, x_labels, ax=ax,
                   cmap="YlOrRd", cbarlabel="Frequency")
    if labels:
        texts = annotate_heatmap(im, valfmt="{x}")
    fig.tight_layout()
    plt.show()
    ## end new
    '''
    fig, ax = plt.subplots()
    im = ax.imshow(np.array(heatmap))

    # EVERYTHING ELSE BELOW IS TAKEN FROM MATPLOTLIB DOCUMENTATION
    # SEE HERE: https://matplotlib.org/stable/gallery/images_contours_and_fields/image_annotated_heatmap.html 

    # We want to show all ticks...
    ax.set_xticks(np.arange(len(x_labels))) # x axis
    ax.set_yticks(np.arange(len(y_labels))) # y axis
    # ... and label them with the respective list entries
    ax.set_xticklabels(x_labels)
    ax.set_yticklabels(y_labels)

    # Rotate the tick labels and set their alignment.
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
             rotation_mode="anchor")
    # Loop over data dimensions and create text annotations.
    for i in range(len(y_labels)):
        for j in range(len(x_labels)):
            text = ax.text(j, i, heatmap[i, j],
                           ha="center", va="center", color="w")

    

    fig.tight_layout()
    plt.show()
    '''



################################################
# Gathers data to properly plot a heatmap.
# Parameters:
#   table: 2d array, columns = cateogry, rows = values in each column
#       column [-1] = pause information in ms 
#       column [0 + shift] = timestamp information
#   num_b : number of buckets to sort time into. 
#       Note: More buckets = more percise heatmap, labels less clear.
################################################
def __get_heatmap(table, num_b):

    # access the two columns from the table with our time/pause info
    timestamps = table["TimeFromStart"]
    pauses     = table["PauseDuration"]

    # create buckets to store the time information.
    # first, compress into num_b buckets along the time X-axis.
    x_b = [[] for i in range(num_b)]
    max_time             = timestamps[-1]
    bucket_time_duration = max_time / num_b
   
    # populate buckets along the x axis.
    for pause, time in zip(pauses, timestamps):
        bucket_no = int(time / bucket_time_duration)
        if bucket_no >= num_b:
            bucket_no = num_b - 1
        x_b[bucket_no].append(pause)

   
    max_pause = max(pauses)
    min_pause = min(pauses)

    # calculate the size of the buckets representing a pause
    bucket_pause_duration = (max_pause - min_pause) / num_b
    
    # create heatmap, which will be a 2d-array
    heatmap = []

    #go through each time interval, and sort the pauses there into frequency lists
    for bucket in x_b:
        yb = [0 for i in range(num_b)] # construct a 0 frequency list
        for time in bucket:
            # determine which ms pause bucket
            y_bucket_no = int((time - min_pause) / bucket_pause_duration)
            if y_bucket_no >= num_b:
                y_bucket_no = num_b - 1

            # increase the frequency of that pause in this time interval
            yb[y_bucket_no] += 1

        # Add the data to the 2d array
        heatmap.append(yb)

    return np.array(heatmap), min_pause, max_pause, max_time # all data needed to plot a heatmap.



# Obtain the shift amount from the dimensions of the table
# The shift amount is determined based on the presence of DateTime information
# If present, the shift amount is 1, else zero.
def __getShift(table):
    if (len(table) == 6):
        shift = 0
    elif len(table) == 7:
        shift = 1
    else:
        print("Table length does not match expected.")
        print("Expected num cols: 5 or 6. Recieved: ", len(table))
        return [] #illogical value will cause error during runtime. TODO: fix

    return shift 

## The following code block was taken directly from matplotlib's documentation
## seen here:
# https://matplotlib.org/stable/gallery/images_contours_and_fields/image_annotated_heatmap.html
def heatmap_make(data, row_labels, col_labels, ax=None,
            cbar_kw={}, cbarlabel="", **kwargs):
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
    cbar = ax.figure.colorbar(im, ax=ax, **cbar_kw)
    cbar.ax.set_ylabel(cbarlabel, rotation=-90, va="bottom")

    # We want to show all ticks...
   
    ax.set_xticks(np.arange(data.shape[1]))
    ax.set_yticks(np.arange(data.shape[0]))
    # ... and label them with the respective list entries.
    ax.set_xticklabels(col_labels)
    ax.set_yticklabels(row_labels)

    # Let the horizontal axes labeling appear on top.
    ax.tick_params(top=False, bottom=True,
                   labeltop=False, labelbottom=True)

    # Rotate the tick labels and set their alignment.
    plt.setp(ax.get_xticklabels(), rotation=-30, ha="left",
                    rotation_mode="anchor")

    # Turn spines off and create white grid.
    ax.spines[:].set_visible(False)

    ax.set_xticks(np.arange(data.shape[1]+1)-.5, minor=True)
    ax.set_yticks(np.arange(data.shape[0]+1)-.5, minor=True)
    ax.grid(which="minor", color="w", linestyle='-', linewidth=3)
    ax.tick_params(which="minor", bottom=False, left=False)

    return im, cbar

# The following code example is taken directly from matplotlib documentation
# on heat maps, seen below
# https://matplotlib.org/stable/gallery/images_contours_and_fields/image_annotated_heatmap.html
def annotate_heatmap(im, data=None, valfmt="{x}",
                     textcolors=("black", "white"),
                     threshold=None, **textkw):
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
        threshold = im.norm(data.max())/2.

    # Set default alignment to center, but allow it to be
    # overwritten by textkw.
    kw = dict(horizontalalignment="center",
              verticalalignment="center")
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