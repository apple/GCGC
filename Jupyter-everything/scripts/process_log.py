# process_log.py

# # # # # # # # # # # # # # # # # # # # # # # # # # # 
# Purpose: Creates functions to process a           #
#          gc log file, extracting information      #
#          of specified types, and returning them.  #
#                                                   #
# Ellis Brown, 5/21/2020                            #
# # # # # # # # # # # # # # # # # # # # # # # # # # #

'''TODO: The following are catogries of information to parse from the log '''
# I would like to be able to produce
# Currently, this assumes usage on "gc1"
    # JVM Memory size
    # (allocated vs peak)
    # Throughput
    # Latency (average pause time, Max pause time)
    # Heap usage after GC
    # Heap usage before GC
    # GC Duration time (over runtime of program, when run? how long run?)
    # Pause GC Duration
    # Reclaimed bytes
    # Young generation allocated space before/after GC
    # Old   generation allocated space before/after GC
    # Allocation and promotion (from young->old)
    # Average time per task compared to all gc tasks
    # Total time (seconds)
    # Memory leaks? 

path= ""                # path to log data
output_csv_id = "extra" # name-scheme of output data file
 
# Set the path to the log file, which will then be parsed for specific 
# attributes.
def setLogPath(p):
    global path
    path = p


#       -> getPauses
# Purpose: Returns a CSV style list of all pauses from the Young Generation
# Parameters : none
# Requirements: path must be set to the .log file we look to traverse.
# Return: List of tuples as pauses, with added metadata.
def getPauses():
    pause_data = []
    with open(path, "r") as file:
        for line in file:
            if "Pause Young" in line:
                pause_data.append(line)
    return extract_pause_metadata(pause_data)

def export_pause_csv(data, timestamps, filename):
    file = open(filename, "w") 
    for line, time in zip(data, timestamps):
        file.write(line[0] + str(", ") + line[1] + str(", "))
        file.write(time[0] + str(", ") + time[1] + str("\n"))
    file.close()

main()

# Purpose: Extracts the useful information from each line of pause_data, 
#          which can then be easily read/displayed
# Parameters: 
        # (pause_data) : lines of the log file that have our desired string
# Return:
        # a list of data, with lines specific only to pauses, as tuples with
        # pause time, and change in allocated bytes in the yonug generation.
def extract_pause_metadata(pause_data):
    data = []
    timestamps = []
    target_string = "->" # Found any time the bytes change from this pause
    str_len = len(target_string)
    
    for line in pause_data:
        if target_string in line:         
            idx = line.index(target_string)
            left = find_index_left(idx, line, ")")            
            right = idx +  line[idx:].index("\n")
            # Get the indicies within the large line, extract that information.
            data.append(line[left + 1 : right - 1])
            timestamps.append(get_timestamps(line))
    
    data = arrange_cols_pauses(data)
    return data



#       -> find_index_left
# Purpose: Find the index of a particular character to the left passed idx
# Parameters:
        # (idx)  The starting index to begin searching left from
        # (line) The string of text to search
        # (char) The character you are searching for the index of
# Return: 
        # The first index of the (char) in (line), if found.
        # Else, -1
def find_index_left(idx, line, char):
    for i in range(idx, 0, -1):
        if line[i] == char:
            return i
    return -1



#       -> arrange_cols_pauses
# Purpose: Given a list of pauses data, create a tuple holding the data nicely
#          in each of the cells. Return that updated, formated tuple list.
# Parameters:
        # (data) a list with entries being a log line formatted to only
        #        contain Time of pause, and block change.
def arrange_cols_pauses(data):
    pause_data = []
    for row in data:
        # We assume all rows fit this description, but it is good to check
        if ")" in row:        
            idx = row.index(")")
            tup = (row[idx+2:-1],row[1:idx+1])
            pause_data.append(tup)
        else:
            print("Error in arrange_col_pauses: Incorrectly formatted line")
    return pause_data



### Purpose: Extracts the time information for any GC log line.
### Returns both time stamps, in their entirety.
def get_timestamps(line):
    ## We assume we are extracting a line, following the following
    ## format.
    #[2020-11-16T14:54:23.755+0000][7.353s][info ] ...
    if not line[0] == "[":
        return None
    # Now, we assume we have a valid line. Extract information based on this assumption.    
    index_seperator = line.index("]")
    real_time  = line[1:index_seperator]
    from_start = line[index_seperator + 2 : index_seperator + 2 + line[index_seperator + 2:].index("]")]
    return [real_time, from_start] 
