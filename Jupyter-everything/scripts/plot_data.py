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
    region_names = ["E", "S", "O", "HS", "HC", "CS", "F", "OA", "CA", "TAMS"]
    
    for line in counts:

