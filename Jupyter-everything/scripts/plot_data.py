# Purpose: Handles all graphing functionality for data.

# NOTE: this is a temporary script
#       TODO: Update documentation, simplify actions.
#       Fix style.
import pandas as pd
import matplotlib.pyplot as plt

def plot_pauses(df):
    x_values = list(df.iloc[:,3])
    x = []
    for entry in x_values:
        x.append(entry[:-1])
    y_values = list(df.iloc[:,0])
    ## Only plot the first 5, due to label confusion. TODO.
    max_items = 10 #len(y_values) for max
    plt.bar(x_values[:max_items], heights= y_values[:max_items])

    plt.ylabel("Miliseconds wait");

    ## Find interesting trends within the data.
   
    find_trends(df)

# Finds trends in dataframe. 
# Column 1 must be pause time, (1 indexed)
# Column 4 must be time since start of program.
 def find_trends(df):
        wait_times = list(df.iloc[:,0])
        max_wait = max(wait_times, key = lambda i : float(i))
        print("Max wait: " + str(max_wait) + " ms")
        
        total_wait   = round(sum(float(i) for i in wait_times), 4)
        average_wait = round(total_wait / len(wait_times), 4)
        print("Total wait: " + str(total_wait) + " ms")
        print("Average wait: " + str(average_wait) + " ms")