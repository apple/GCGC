# # # # # # # # # # # # # # # # 
#  compare_logs.py
#   compare_logs == cl (TODO: update file names)
#   Purpose: Allows for visual comparisons on logs
#
#   Ellis Brown, 6/3
#
# # # # # # # # # # # # # # # # # 
import re
from scripts import parse_log as pl
from matplotlib import pyplot as plt

# files is all paths to logs to be analyzed
files = []
file_titles = []
# Set the log files to be analyzed, as a list.
def setFiles(f = [], titles = []):
    if not f:
        print("No files added to path. Ending")
    
    global files
    files = f   # set files for access throughout program during runtime
    global file_titles
    file_titles = titles


# Does all comparisons
# Returns true on success, false otherwise.
def compareAll():
    if not files:
        print("No files added to path. Ending")
        return False
    compareMetadata()
    comparePauses(True, 20, 20)
    compareHeap()
    return True


# # # # # # # # # # # # # # # # # # # # # # # # #
# Compares the Garbage Collector 
# Metadata from multiple logs, and
# displays the result in an ASCII table 
# printed to stdout
# # # # # # # # # # # # # # # # # # # # # # # #
def compareMetadata():
    if not files or type(files) != list:
        print("No files added. Ending compare pauses.")
        return 
    
    # generate a collection of metadata information
    metadata_list = []
    for file in files:
        __choose(file) # set file in parse_log module.
        metadata = pl.getGCMetadata() 
        metadata_list.append(metadata)
    
    __print_metadata_lists(metadata_list)


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
#   Compares the heap allocation after garbage collection run 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
def compareHeap(old = False, before = False, after = False):
    if not files or type(files) != list:
        print("No files added. Ending compare heap")
    
    # If no parameters were passed (or all passed as false), run everything.
    #   we assume that no parameters wants a full analysis.
    if not (old or before or after):
        old = True
        young = True
        before = True
        after = True
    
    # Gather data from all logs
    heap_alloc_list = []
    colors = ["g", "r", "b", "y", "c", "m", "k", 
             "forestgreen", "lime", "dark_orange",
             "darkred", "coral", "darkgoldenrod"]
    
    for file in files:
        __choose(file) # set file in parse_log module.
        heap_alloc = pl.getHeapAllocation()

        heap_alloc_list.append(heap_alloc[0])
        #initial_free_mem.append(heap_alloc[1]) # TODO: fix this data
    
    global file_titles
    if not file_titles:
        file_titles = [i for i in range(1, len(heap_alloc_list) + 1)]

    
    ## Go through each option and create a new plot. Use different titles and
    ## keyword search parameters.
    # TODO: The following sections can be plotted then output from /scripts/plot_data
    if old:
        fig, ax = plt.subplots()
        for i in range(len(heap_alloc_list)):
            ax = __sum_allocation(heap_alloc_list[i], ["Old"], ax, before = False, 
                color = colors[i], label = file_titles[i])
        ax = __addLabelsHeap(ax, "Number of Old regions throughout runtime after gc")
    if before:
        fig, ax = plt.subplots()
        for i in range(len(heap_alloc_list)):
            ax = __sum_allocation(heap_alloc_list[i], ["Old", "Eden", "Survivor", "Archive"], ax, before = True, 
                color = colors[i], label = file_titles[i])
        ax = __addLabelsHeap(ax, "Number of regions allocated before gc")
    if after:
        fig, ax = plt.subplots()
        for i in range(len(heap_alloc_list)):
            ax = __sum_allocation(heap_alloc_list[i], ["Old", "Eden", "Survivor", "Archive"], ax, before = False, 
                color = colors[i], label = file_titles[i])
        ax = __addLabelsHeap(ax, "Number of regions allocated after gc")
    return 
    
# Takes in a list of regions, and returns the sum of those regions over a 
# given time. Updates the plot (ax) by plotting time vs. sum for words.
# Uses color and label provided.
def __sum_allocation(table, keywords, ax, before = False, color = "", label = ""):
    
    if not table or not keywords:
        print("__sum_allocation parameters incorrect. Abort.")
        return

    heap_alloc = table 
    
    # get timestamps from the time keyword in the table. Convert str->float
    timestamps = list(map(float, heap_alloc["Time"]))
    
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
    ax.plot(timestamps, allocation, color = color, label = label)
    return ax

# Add labels to a heap allocation chart. 
# Return updated plot.
def __addLabelsHeap(ax, title):
    ax.set_xlabel("Time passed (seconds)")
    ax.set_ylabel("Regions allocated")
    ax.set_title(title)
    ax.legend()
    return ax 



# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# Compares the GC pauses during runtime by
# inspecting log information. Plots all pauses
# along the time axis of the longest run,
#
#   Parameters:
#   full_p      (boolean) create a plot of all pauses during runtime?
#   sum_p       (int)     number of bars to create for summed pauses during run
#   max_p       (int)     number of bars to create for longest pause during run
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
def comparePauses(full_p = True, sum_p = 0, max_p = 0):
    if not files or type(files) != list:
        print("No files added. Ending compare pauses.")
        return
    
    # Construct a collection of table information from each log
    collection = []
    for file in files:
        __choose(file)
        table = pl.getPauses()
        collection.append(table)
    
    # create plots based on parameters
    if not collection:
        print("No data collected")
        return

    # Plot based on parameters. Each plot type requires a different mapping
    if full_p:
        __gen_comparison(collection, "Pauses during runtime", 0, 
                         mapping = None, file_titles = file_titles)
    if sum_p > 0:
        __gen_comparison(collection, "Sum Pauses during runtime",
                         sum_p, mapping = sum, file_titles = file_titles)
    if max_p > 0:
        __gen_comparison(collection, "Longest pauses during runtime",
                         max_p, mapping = max, file_titles = file_titles)
    
# generate comparison on the same data table, by plotting multiple sets
# of information to the same table.
def __gen_comparison(collection, title, bucket_count, mapping = None, file_titles = []):
    
    if not collection:
        # if no data collected, nothing to plot. Finished.
        return 

    fig, ax = plt.subplots()    # create a subplot for this coomparison
    
    # colors to use for the plot. More colors can be found in the following link
    #https://matplotlib.org/stable/gallery/color/named_colors.html
    colors = ["g", "r", "b", "y", "c", "m", "k", 
             "forestgreen", "lime", "dark_orange",
             "darkred", "coral", "darkgoldenrod"]
    
    # if no file titles have been passed, then simply use numbers for the vals
    if not file_titles:
        file_titles = [i for i in range(1, len(collection) + 1)]

    # Create a combined plot for each thing. Group and plot each item in collection
    for i in range(len(collection)):
        ax = __group_and_plot(collection[i], ax, colors[i], file_titles[i], bucket_count, mapping)
    
    ax = __addLabelsPauses(ax, title)   # add graph labels
    plt.show()


## Take data from a table, appropriately map it if needed, and 
# plot the table to an output figure
def __group_and_plot(table, ax, color, label, bucket_count, mapping):
    
    if table.empty:
        print("No table passed as a parameter. Abort.")
        return

 
    timestamps = table["TimeFromStart"]                 
    pauses = table["PauseDuration"]

    
    # plot data in full, without grouping into buckets
    if not mapping:
        ax = __plot_data(ax, timestamps, pauses, 
                         color, label, x_transformation = False)
    else:
        # get the timestamps and pauses grouped into buckets based on mapping
        timestamps, pauses = __group_buckets(timestamps, 
                                            pauses,
                                            bucket_count,
                                            mapping)
        ax = __plot_data(ax, timestamps, pauses, 
                         color, label, x_transformation = True)
    
    return ax

# Based on a passed mapping, sort groupings of data into buckets, 
# such that they follow a uniform time distribution based on bucket count
def __group_buckets(timestamps, pauses, bucket_count, mapping):
    full_duration  = list(timestamps)[-1]
    pause_duration = full_duration / bucket_count
   
    # Put bottom value of all ranges into hash table. 
    # Actual hash table not needed, because indicies in range [0, n]
    buckets = [[] for i in range(bucket_count)]
    for time, pause in zip(timestamps, pauses):
        
        bucket = int(time / pause_duration) # floor of division to get bucket.
        if bucket == len(buckets):
            bucket = len(buckets) - 1
        buckets[bucket].append(pause)
   
    p = 1 # index of pause
    for i in range(bucket_count):

        # the mapping is a function that may compute the sum, max, or similar
        if buckets[i]:
            buckets[i] = mapping([value for value in buckets[i]]) # update this bucket
        else:
            buckets[i] = 0

    timestamps = [r * pause_duration for r in range(bucket_count)]
    pauses = buckets

    return timestamps, pauses
    # Take values and sort them into hash tables based on values. 


# Take the data as pairs of (time, pause), and turn those into a line graph
# showing the pause times throughout runtime.
def __plot_data(ax, timestamps, pauses, color, label, x_transformation):
    ## Create data set that mimimics an up and down line graph based on pause time.
    x_data = []
    y_data = []
    if not x_transformation:
        ###### Create X-Y Data. bumps for height based on pause duration #####
        for x,y in zip(timestamps, pauses):
            # convert y from ms to seconds
            y = y / 1000

            # first, create a point at time before pause
            x_data.append(x)
            y_data.append(0)

            # next, create a point of y height, at that initial time
            x_data.append(x)
            y_data.append(y)

            # last point in pause duration high
            x_data.append(x + y)
            y_data.append(y)

            # end pause duration high
            x_data.append(x + y)
            y_data.append(0)
    else:
        
        # Create buckets of the same size, placed uniformly over time.
        pt_uniform = timestamps[1] * 0.7 # 0.7 constant for bar width
                                         # 1 means bars indistinguishable
                                         # 0 means no bars
        for x,y in zip(timestamps, pauses):
            
            y = y / 1000

            x_data.append(x)
            y_data.append(0)
           
            x_data.append(x)
            y_data.append(y)
           
            x_data.append(x + pt_uniform)
            y_data.append(y)

            x_data.append(x + pt_uniform)
            y_data.append(0)

    # Plot the data created for this table. #
    ax.plot(x_data, y_data, color = color, label = label),    
    # return the subplot updated with the new information
    return ax


# Take numbers formatted with a trailing 's' character to signify seconds unit
# and remove the s. Return the result as a float.
def __time_from_float(time):
    return float(time[:-1])


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


# Add labels to a pause graph
def __addLabelsPauses(ax, title):
    ax.set_xlabel("Time passed (seconds)")
    ax.set_ylabel("Pause duration (seconds)")
    ax.set_title(title)
    ax.legend()
    return ax 


# Sets the active file to be checked in the parse_log module
# TODO: Update parse_log (pl) to allow for schema detection
def __choose(filename):
    pl.setLogPath(filename)
    pl.setLogSchema(0)


# Takes a list of metadata tables, and prints off
# each column of the table together
# TODO: revise and update this functiomn, it is unclear what is happening
# TODO: update output stdout style 
# input is metadata_list
    # metadata_lists =  [ [a] [b] [c] ... ]
# where a, b, c,.... z are tables
    # where table    = [ [x] [y] [z] ... ]
# where x, y, z , .... z are '[category, value]' pairs,
# where cateogry = metadata info piece (such as gc versopm)
# and value is the value for that metadata (such as version 16.0.1+9)
# NOTE: This function DOES NOT WORK AS INTENDED
# However, this accidentially made an oK output, so it will be prioritized
# later to fix. Until then, however, this is TODO: fix broken.
def __print_metadata_lists(metadata_lists):
    
    if not metadata_lists or not metadata_lists[0]:
        print("No metadata in metadata_lists")

    max_title_len = max([len(item[0]) for item in metadata_lists[0]])
    
    max_out_len = 0
    # Calculate the max metadata length 
    for metadata in metadata_lists:
        for item in metadata:
            max_out_len = max(len(item[1]), max_out_len)
    
    for index in range(len(metadata_lists[0])): #length of the items to print
                                                # = num rows
        # Start with title 
        print(metadata_lists[0][index][0] +" ", end="")
        # Determine if an extra whitespace is needed, from even/odd lines
        whitespace_length = max_title_len - len(metadata_lists[0][index][0]) + 4
        if (whitespace_length % 2 == 1):
            print(" ", end="")
       
       # print("num_whitespace = ",int((max_title_len - len(metadata_lists[0][index][0])) / 2) )
        print(int((max_title_len - len(metadata_lists[0][index][0])) / 2 - 4) * ". ", end = "")
        for i in range(len(metadata_lists)): # number of columns
            
            # check if that column has any values
            if metadata_lists[i]:
                thing = metadata_lists[i][index]
                print(thing, end="")

                if not (max_out_len - len(thing) % 2):
                    print(" ", end="")
                
                print("")

                print((int(max_out_len - len(thing) / 2 ) * " ") + " | ", end="")
        print("")

