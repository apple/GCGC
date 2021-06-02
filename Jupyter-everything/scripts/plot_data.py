#############################################################################
##                          plot_data.py
##  Defines functions to plot tables of information collected from logs.
##  
##  Author: Ellis Brown, 6/1
##  TODO: Define a general type chart, plots any table 
#############################################################################
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scripts import process_log as pl

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
    shift = 5 - len(table) # account for possible empty rows.
    y_values = list(map(float, table[4 - shift]))
    x_values = list(map(__time_to_float, table[0 - shift]))

    # Show interesting trends
    total_wait = __find_trends(table)
    total_time = pl.getTotalProgramRuntime()
    print("Total time: " + str(total_time))
    print("Total program runtime: " + str(total_time) + " seconds")
    throughput = (total_time - (total_wait)/1000) / (total_time)
    print("Throughput: " + str(round(throughput * 100, 4)) + "%")
 
    # # # # # # # # # # # # # # # # # # # #
    # Plot 1: Pauses over program's entire runtime.
    plt.bar(x = np.array(x_values), height= np.array(y_values), width = 2.0)
    plt.ylabel("Pause duration (miliseconds)");
    plt.xlabel("Time from program start (seconds)")
    plt.title("Pauses for Young Generation GC")
    plt.show()
    # # # # # # # # # # # # # # # # # # # #
    # Plot 2: Pauses showing duration, no timestamps
    x_values = list(map(int, list(range(len(y_values)))))
    plt.bar(x = x_values, height= y_values)
    plt.ylabel("Pause duration (miliseconds)");
    plt.xlabel("Pause listed in order")
    plt.title("Pauses for Young Generation GC")
    plt.show()
    # # # # # # # # # # # # # # # # # # # #

    
# Removes trailing 's' character from time in seconds
def __time_to_float(time):
    return float(time[:-1])

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
def __find_trends(table):
    shift = 5 - len(table)
    wait_times = table[4 - shift]
    max_wait = max(wait_times, key = lambda i : float(i))
    total_wait   = round(sum(float(i) for i in wait_times), 4)
    average_wait = round(total_wait / len(wait_times), 4)
    
    print("Total pauses: " + str(len(wait_times)))
    print("Max wait: " + str(max_wait) + " ms")
    print("Total wait: " + str(total_wait) + " ms")
    print("Average wait: " + str(average_wait) + " ms")
    return total_wait

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
    if not dd[1]:
        print("Failed to find inital memory size. Rerun with parameter max_heap = (int)")
    if max_heap != 0:
        dd[1] = max_heap
    print("This far")
    data_dictionary = dd[0]
    # get free_memory list of memory during runtime
    free_memory = __calculate_freemem(data_dictionary, dd[1]) 
    
    # Create integer list [0...n-1] to help plot allocation
    # TODO: Change this to be based on actual time in program.
    x = []
    for item in data_dictionary["Time"]:
        x.append(float(item))
        x.append(float(item))
    x = np.array(x) # *2 for tuples
    
    # Format plot
    plt.xlabel("GC Run number (not based on time)")
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
    plt.figure(2)
    plt.plot(x, np.array(free_memory), color = "red", label = "Free Memory")
    plt.legend()
    plt.show() 

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
def __calculate_freemem(data_dictionary, inital_free):
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
        temp_val = 0
        for key in data_dictionary.keys():
            if str(key) != "Time":
                                        # access tuple [0] from list
                                        # of tuples associated with key
                temp_val += int(data_dictionary[key][idx][0])
        free_mem.append(int(inital_free - temp_val))
        
        # Calculate the free memory after the GC runs
        temp_val = 0
        for key in data_dictionary.keys():
            if str(key) != "Time":
                temp_val += int(data_dictionary[key][idx][1])
        free_mem.append(int(inital_free - temp_val))

    return free_mem

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
#               function displayMetadata()                    #
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