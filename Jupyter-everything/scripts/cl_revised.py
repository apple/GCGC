# # # # # # # # # # # # # # # # 
#  cl_revised.py
#
#   Purpose: Allows for visual comparisons on logs
#
#   Ellis Brown, 6/3
#
# # # # # # # # # # # # # # # # # 
from scripts import process_log as pl
from matplotlib import pyplot as plt

# files is all paths to logs to be analyzed
files = []

# Set the log files to be analyzed, as a list.
def setFiles(f = []):
    if not f:
        print("No files added to path. Ending")
    
    global files
    files = f   # set files for access throughout program during runtime


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
        __choose(file) # set file in process_log module.
        metadata = pl.getGCMetadata() 
        metadata_list.append(metadata)
    
    __print_metadata_lists(metadata_list)

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
        table = pl.getYoungPauses()
        collection.append(table)
    
    # create plots based on parameters
    if not collection:
        print("No data collected")
        return

    if full_p:
        __gen_comparison(collection, "Pauses during runtime", mapping = None)
    if sum_p > 0:
        __gen_comparison(collection, "Sum Pauses during runtime", sum_p, mapping = sum)
    if max_p > 0:
        __gen_comparison(collection, "Longest pauses during runtime", max_p, mapping = max)
    

def __gen_comparison(collection, title, bucket_count, mapping = None):
    if not collection:
        return 

    fig, ax = plt.subplots()    # create a subplot for this coomparison
    ax = __addLabels(ax, title)   # add graph labels

    colors = ["g", "r", "b", "y", "c", "m"] #https://matplotlib.org/stable/gallery/color/named_colors.html
    for i in range(len(tl)):
        ax = func(tl[i], ax, colors[i], str(i), count)
    
    plt.show()


def __addLabels(ax, title):
    ax.set_xlabel("Time passed (seconds)")
    ax.set_ylabel("Pause duration (seconds)")
    ax.set_title(title)
    ax.legend()
    return ax 

# Sets the active file to be checked in the process_log module
# TODO: Update process_log (pl) to allow for schema detection
def __choose(filename):
    pl.setLogPath(filename)
    pl.setLogSchema(0)












# Takes a list of metadata tables, and prints off
# each column of the table together
# TODO: revise and update this functiomn, it is unclear what is happening
# TODO: update output stdout style 
def __print_metadata_lists(metadata_lists):
    
    if not metadata_lists or not metadata_lists[0]:
        print("No metadata in metadata_lists")
    
    doublelist = []
    for i in range(len(metadata_lists)):
        doublelist.append(list(metadata_lists[i].items()))
    metadata_lists = doublelist
    ### First, find the format for the table. Then, print all in that format.
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