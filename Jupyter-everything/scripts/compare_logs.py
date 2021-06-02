# Purpose: Envoke a method of this function to comapare any N number of logs to each other.
from scripts import process_log as pl
import numpy as np
from matplotlib import pyplot as plt
files = []
def setFiles(f = []):
    if not f:
        print("No files added to path. Ending")
    global files
    files = f   # set files for access throughout program during runtime


def comparePauses():
    if not files:
        print("No files added. Ending compare pauses.")
        return 
    collection = []
    for file in files:
        
        choose(file)
        table = pl.getYoungPauses(False)
        collection.append(table)
    generate_table_comparison(collection)

def choose(filename):
    pl.setLogPath(filename)
    # todo, implement this feature
    #pl.setLogSchema(filename)
    pl.setLogSchema(0)

def compareMetadata():
    if not files:
        print("No files added. Ending compare metadata.")
    metadata_list = []
    for file in files:
        choose(file) # set file in pl.
        metadata = pl.getGCMetadata(False)
        metadata_list.append(metadata)
    print_metadata_lists(metadata_list)

def print_metadata_lists(metadata_lists):
    
    
    if not metadata_lists or not metadata_lists[0]:
        print("No metadata in metadata_lists")
    doublelist = []
    for i in range(len(metadata_lists)):
        doublelist.append(list(metadata_lists[i].items()))
    metadata_lists = doublelist
    ### First, find the format for the table. Then, print all in that format.
    max_title_len = max([len(item[0]) for item in metadata_lists[0]])
    
    max_out_len = 0
    for metadata in metadata_lists:
        for item in metadata:
            max_out_len = max(len(item[0]), max_out_len)
   
    
    for index in range(len(metadata_lists[0])): #length of the items to print
                                                # = num rows
        
        # Start with title 
        print(metadata_lists[0][index][0] +" ", end="")
        # Determine if an extra whitespace is needed, from even/odd lines
        whitespace_length = max_title_len - len(metadata_lists[0][index][0])
        if (whitespace_length % 2 == 1):
            print(" ", end="")
       
       # print("num_whitespace = ",int((max_title_len - len(metadata_lists[0][index][0])) / 2) )
        print(int((max_title_len - len(metadata_lists[0][index][0])) / 2) * ". ", end = "")
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

plt.rcParams['figure.figsize'] = [12, 7]    
def plot_pauses(collection):
    fig, ax = plt.subplots() # default 1 row, 1 column
    labels = ["First", "Second", "Third"]
    colors = ["red", "green", "blue"]
    ax.set_ylabel("Pause duration (miliseconds)")
    ax.set_xlabel("Time from program start (seconds)")
    ax.set_title("Pauses for Young Generation GC")
    for file_no in range(len(collection)):
        ax = plot_subplot(collection[file_no], colors[file_no], labels[file_no], ax)
    plt.show()
    

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
def plot_subplot(table, color, label, ax):
 # Obtain X Y list information from the dataframe.
    shift = 5 - len(table) # account for possible empty rows.
    print(len(table))
    print(shift, "Shift")
    y_values = list(map(float, table[4 - shift]))
    x_values = list(map(__time_to_float, table[0 - shift]))
    
    # Create a subplot to apply this effect on.
    
    # Show interesting trends
    total_wait = __find_trends(table)
    total_time = pl.getTotalProgramRuntime()
    print("Total time: " + str(total_time))
    print("Total program runtime: " + str(total_time) + " seconds")
    throughput = (total_time - (total_wait)/1000) / (total_time)
    print("Throughput: " + str(round(throughput * 100, 4)) + "%")
    
    # # # # # # # # # # # # # # # # # # # #
    # Plot 1: Pauses over program's entire runtime.
    ax = ax.plot(np.array(x_values), height= np.array(y_values), width = 2.0, color = color, label = label)

  
    #plt.show()
    # # # # # # # # # # # # # # # # # # # #
    return ax

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

def generate_table_comparison(tl):
    fig, ax = plt.subplots()
    colors = ["g", "r", "b", "y"]
    for i in range(len(tl)):
        ax = plot_pause(tl[i], ax, colors[i], label = str(i))
    ax = addLabels(ax)
    plt.show()



def addLabels(ax):
    ax.set_xlabel("X LABEL")
    ax.set_ylabel("Y LABEL")
    ax.set_title("the coolest")
    ax.legend()
    return ax 

def plot_pause(table, ax, color = "", label = ""):
    
    ########################### setup ######################
    if not table:
        print("No table passed as a parameter. Abort.")
        return
    # Tables may/may not come with datetime information appended.
    # This information is not currently used. Therefore, shift past it
    if (len(table) == 5):
        shift = 0
    elif len(table) == 6:
        shift = 1
    else:
        print("Table length does not match expected.")
        print("Expected num cols: 5 or 6. Recieved: ", len(table))
        return
    
    timestamps = table[0 + shift]       # get timestamps from table information
    timestamps = list(map(__time_to_float, timestamps)) # clean data 

    pause_information = table[-1]       # get pause information duration
    
    ## Create data set that mimimics an up and down line graph based on pause time.
    x_data = []
    y_data = []

    ###### Create X-Y Data. bumps for height based on pause duration #####
    for x,y in zip(timestamps, pause_information):
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
    
    # Plot the data created for this table. #
    ax.plot(x_data, y_data, color = color, label = label),    
    # return the subplot updated with the new information
    return ax
