# Purpose: Handles all graphing functionality for data.

# NOTE: this is a temporary script
#       TODO: Update documentation, simplify actions.
#       Fix style.
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def plot_pauses(df):
    # Obtain X Y list information from the dataframe.
    x_values = list(df.iloc[:,3])
    x = []
    for entry in x_values:
        x.append(entry[:-1])
    x_values = list(map(float, x))
    y_values = list(map(float, list(df.iloc[:,0])))
    del x #not necesarily needed

    
    # # # # # # # # # # # # # # # # # # # #
    # Plot 1: Pauses over program's entire runtime.
    plt.bar(x = x_values, height= y_values)
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
    __find_trends(df)



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


# Purpose: Print a graph showing the heap breakdown throughout the
#          program
# Parameters/Requirements
def plot_heap_allocation_breakdown(counts):
    if (type(counts)) == dict:
        return __plot_HA_schema0(counts)

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
    plt.show() # commented out during testing.

# Purpose : Plot the heap breakdown throughout program
#
# Counts is a dictionary. Keys = names
# Values = list of tuples
#                  (before, after)
def __plot_HA_schema0(data_dictionary):
    
    free_memory = __calculate_freemem(data_dictionary)
    x = np.array(list(range(len(data_dictionary["Eden"]) * 2))) 
    plt.xlabel("GC Run number (not based on time)")
    plt.ylabel("Number of memory blocks")
    plt.title("heap allocation throughout runtime")
    plt.legend(list(data_dictionary.keys()))
    colors = ["royalblue", "cyan", "black", "green", "purple", "orange", "lime", "brown", "darkmagenta", "lime", "green"]
    color_index = 0
    plt.figure(1)
    for key in data_dictionary.keys():
        pairs = []
        for idx in range(len(data_dictionary[key])):
            pairs.append(int(data_dictionary[key][idx][0]))
            pairs.append(int(data_dictionary[key][idx][1]))
        temp_plot_for_testing_please_remove_after = plt.plot(np.array(x), np.array(pairs), color = colors[color_index], label = str(key))
        color_index += 1
    plt.legend()
    plt.show() # commented out during testing.
    plt.figure(2)
    plt.plot(x, np.array(free_memory), color = "red", label = "Free Memory")
    plt.legend()
    plt.show() # commented out during testing.
    plt.figure(3)
    for key in data_dictionary.keys():
        pairs = []
        for idx in range(len(data_dictionary[key])):
            pairs.append(int(data_dictionary[key][idx][0]))
            pairs.append(int(data_dictionary[key][idx][1]))
        temp_plot_for_testing_please_remove_after = plt.plot(np.array(x), np.array(pairs), color = colors[color_index], label = str(key))
        color_index += 1
    plt.plot(x, np.array(free_memory), color = "red", label = "Free Memory")
    plt.legend()
    plt.show() # commented out during testing.


# Purpose: Because "free" memory is not explicitly captured, must be calculated
def __calculate_freemem(data_dictionary):
    free_mem = []
    inital_free = 0
    # Note: this calculation is temporary
    for key in data_dictionary.keys():
        inital_free += int(data_dictionary[key][0][0])
    
    # Abitrary number of free data so trend line will look reasonable
    # FIX LATER (IMPORTANT TODO)
    #inital_free *= 6
    inital_free = 125
    for idx in range(len(data_dictionary["Eden"])):
        temp_val = 0
        for key in data_dictionary.keys():
            temp_val += int(data_dictionary[key][idx][0])
        free_mem.append(int(inital_free - temp_val))
        temp_val = 0
        for key in data_dictionary.keys():
            temp_val += int(data_dictionary[key][idx][1])
        free_mem.append(int(inital_free - temp_val))
    return free_mem
        


# Purpose: Creates a graphical table to represent the initial heap state
# Parameters: inital_heap_state (hs) : dict
# Return: None
def tableInitialHeapState(hs):
    # create table from data
    if hs:
        table_rows = [[key, hs[key]] for key in hs.keys()]
        for item in table_rows:
            print(item[0] + " \t| " + item[1])
    else:
        print("No found heap state information. Empty dict")
