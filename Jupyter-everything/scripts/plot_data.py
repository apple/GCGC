# Purpose: Handles all graphing functionality for data.

# NOTE: this is a temporary script
#       TODO: Update documentation, simplify actions.
#       Fix style.
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scripts import process_log as pl
plt.rcParams['figure.figsize'] = [14, 8]

def plot_pauses(df):
    # Obtain X Y list information from the dataframe.
    x_values = list(df.iloc[:,3])
    x = []
    for entry in x_values:
        x.append(entry[:-1])
    x_values = list(map(float, x))
    y_values = list(map(float, list(df.iloc[:,0])))
    del x #not necesarily needed
    total_wait = __find_trends(df)
    total_time = pl.getTotalProgramRuntime()
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

    ## Find interesting trends within the data.
    




# Finds trends in dataframe. 
# Column 1 must be pause time, (1 indexed)
# Column 4 must be time since start of program.
def __find_trends(df):
    wait_times = list(df.iloc[:,0])
    max_wait = max(wait_times, key = lambda i : float(i))
    total_wait   = round(sum(float(i) for i in wait_times), 4)
    average_wait = round(total_wait / len(wait_times), 4)
    
    print("Total pauses: " + str(len(wait_times)))
    print("Max wait: " + str(max_wait) + " ms")
    print("Total wait: " + str(total_wait) + " ms")
    print("Average wait: " + str(average_wait) + " ms")
    return total_wait


# Purpose: Print a graph showing the heap breakdown throughout the
#          program
# Parameters/Requirements
def plot_heap_allocation_breakdown(counts):
    
    if (len(counts)) == 2:
        return __plot_HA_schema0(counts)
    counts = counts[0]
    x = np.array(list(range(len(counts))))
    
    #print(counts)
    region_names = ["Young", "Survivor", "Old", "Humongus_start", "Humongus_continue", "Collection_set", "Free", "Open_archive", "Closed_archive", "TAMS"]
    ''' Heap Regions: E=young(eden), S=young(survivor), O=old, HS=humongous(starts)
     HC=humongous(continues), CS=collection set, F=free, OA=open archive
     CA=closed archive, TAMS=top-at-mark-start (previous, next) '''
    colors = ["royalblue", "cyan", "black", "green", "purple", "orange", "lime", "brown", "darkmagenta", "lime", "green"]
    plt.xlabel("GC Run number (not based on time)")
    plt.ylabel("Number of memory blocks")
    plt.title("heap allocation throughout runtime")
    plt.legend(region_names)
    for idx in range(len(counts[0])):
        plt.plot(x, np.array(list(row[idx] for row in counts)), color = colors[idx], label = region_names[idx])
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
def __plot_HA_schema0(dd):
    if (not dd) or (len(dd) < 2) or (not dd[0]) or (not dd[1]):
        return

    
    data_dictionary = dd[0]

    # get free_memory list of memory during runtime
    free_memory = __calculate_freemem(data_dictionary, dd[1]) 
    
    # Create integer list [1...n] to help plot allocation
    x = np.array(list(range(len(data_dictionary["Eden"]) * 2))) # *2 for tuples
    
    # Format plot
    plt.xlabel("GC Run number (not based on time)")
    plt.ylabel("Number of memory blocks")
    plt.title("heap allocation throughout runtime")
    plt.legend(list(data_dictionary.keys()))
    # Choose from some color choices. TODO: style colors
    colors = ["royalblue", "cyan", "black", "green", "purple", 
              "orange", "lime", "brown", "darkmagenta", "lime", "green"]
    color_index = 0
    # Create the first plot
    plt.figure(1)
    
    for key in data_dictionary.keys():
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
    for idx in range(len(data_dictionary["Eden"])):
        
        # Calculate the free memory before the GC runs
        temp_val = 0
        for key in data_dictionary.keys():
                                        # access tuple [0] from list
                                        # of tuples associated with key
            temp_val += int(data_dictionary[key][idx][0])
        free_mem.append(int(inital_free - temp_val))
        
        # Calculate the free memory after the GC runs
        temp_val = 0
        for key in data_dictionary.keys():
            temp_val += int(data_dictionary[key][idx][1])
        free_mem.append(int(inital_free - temp_val))

    return free_mem
        
######################################################################
# Following block is currently unused.
# Rational: It returns the same data as tableMetadata(), just less 
# # Purpose: Creates a graphical table to represent the initial heap state
# # Parameters: inital_heap_state (hs) : dict
# # Return: None
# def tableInitialHeapState(hs):
#     # create table from data
#     if hs:
#         table_rows = [[key, hs[key]] for key in hs.keys()]
#         for item in table_rows:
#             print(item[0] + " \t| " + item[1])
#     else:
#         print("No found heap state information. Empty dict")
######################################################################



# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
#               function tableMetadata()                      #
#   Purpose:                                                  #
#       Take the metadata collected, and print in a well      #
#       formatted table using ASCII characters                #
#   Parameters:                                               #
#       metadata : a dictionary containing key-value pairs    #
#                   keys:   The type of the metadata item     #
#                   values: The value of the metadata item    #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def tableMetadata(metadata):
    
    if not metadata:
        print("No metadata found.")
        return
    
    # Transform into two lists, for easier data formatting
    keys = []
    vals = []
    for key in metadata.keys():
        keys.append(key)
        vals.append(metadata[key])
    # Determine max char length
    max_key_len = max([len(item) for item in keys])
    max_val_len = max([len(item) for item in vals])

    # Add a top to the table box
    table_line = "-" * max_key_len + "-" * max_val_len + "----"
    print(table_line)
    
    # Print each row  
    for idx in range(len(keys)):
        
        # Start with the metadata item 
        print(str(keys[idx]) +" ", end="")
        
        # Determine if an extra whitespace is needed, from even/odd lines
        whitespace_length = max_key_len - len(keys[idx])
        if (whitespace_length % 2 == 1):
            print(" ", end="")
        
        # Print formatting based on item length, then print the value
        print(int((max_key_len - len(keys[idx])) / 2) * ". " + "| " + str(vals[idx]))
        
       