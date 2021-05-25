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
import pandas as pd
import re

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
def getPauses(create_csv = False):
    pause_data = []
    with open(path, "r") as file:
        for line in file:
            if "Pause Young" in line:
                pause_data.append(line)
    data, timestamps = __extract_pause_metadata(pause_data)
    if create_csv:
        filename = "pauses_" + output_csv_id + "_OUT.csv"
        __export_pause_csv(data, timestamps ,filename)
    return __dataframe_from_pause_lists(data, timestamps)


# Purpose: Creates a file with specific CSV data to the pause
#          gc log information.
def __export_pause_csv(data, timestamps, filename):
    file = open(filename, "w") 
    for line, time in zip(data, timestamps):
        file.write(line[0] + str(", ") + line[1] + str(", "))
        file.write(time[0] + str(", ") + time[1] + str("\n"))
    file.close()



# Purpose: Extracts the useful information from each line of pause_data, 
#          which can then be easily read/displayed
# Parameters: 
        # (pause_data) : lines of the log file that have our desired string
# Return:
        # a list of data, with lines specific only to pauses, as tuples with
        # pause time, and change in allocated bytes in the yonug generation.
def __extract_pause_metadata(pause_data):
    data = []
    timestamps = []
    target_string = "->" # Found any time the bytes change from this pause
    str_len = len(target_string)
    
    for line in pause_data:
        if target_string in line:         
            idx = line.index(target_string)
            left = __find_index_left(idx, line, ")")            
            right = idx +  line[idx:].index("\n")
            # Get the indicies within the large line, extract that information.
            data.append(line[left + 1 : right - 1])
            timestamps.append(__get_timestamps(line))
    
    data = __arrange_cols_pauses(data)
    return data, timestamps



#       -> __find_index_left
# Purpose: Find the index of a particular character to the left passed idx
# Parameters:
        # (idx)  The starting index to begin searching left from
        # (line) The string of text to search
        # (char) The character you are searching for the index of
# Return: 
        # The first index of the (char) in (line), if found.
        # Else, -1
def __find_index_left(idx, line, char):
    for i in range(idx, 0, -1):
        if line[i] == char:
            return i
    return -1



#       -> __arrange_cols_pauses
# Purpose: Given a list of pauses data, create a tuple holding the data nicely
#          in each of the cells. Return that updated, formated tuple list.
# Parameters:
        # (data) a list with entries being a log line formatted to only
        #        contain Time of pause, and block change.
def __arrange_cols_pauses(data):
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
### Returns both time stamps, in their entirety, as a 2 length list.
def __get_timestamps(line):
    if not line[0] == "[":
            return None
    ## We assume we are extracting a line, following the following
    ## format.
    #[2020-11-16T14:54:23.755+0000][7.353s][info ] ...
    '''However, if a line does not contain a Original timestamp, instead format
       by returning time from start twice.'''
    pattern = "\[\d\d\d\d-\d\d-\d\d.*\]"
    match = re.search(pattern, line) # Search the regex line for a match
    index_seperator = line.index("]")
    real_time  = line[1:index_seperator]
    if match:  
        # Now, we assume we have a valid line. Extract information based on this assumption.    
        from_start = line[index_seperator + 2 : index_seperator + 2
                         + line[index_seperator + 2:].index("]")]
        return [real_time, from_start] 
    else: 
        # We assume we have NO date format, but DO have time stamps.
        from_start = real_time # We will just use the same information. 
                               # Let the client detect and handle this case
                               # Rational: Currently, there are no plans for
                               # use of the "real time", but we provide 
                               # infrastructure to allow it.
        return [real_time, from_start]
        





# Purpose: (TEMPORARY FUNCTION) : takes a list of tuples and a list of lists,
# and combines them into one pandas df.
def __dataframe_from_pause_lists(data, timestamps):
    if (len(data) != len(timestamps)):
        print("ERROR: Data list length does not match timestamps list length")
        quit()
    
    combined = [[],[],[],[]]
    for i in range(len(data)):
        combined[0].append(data[i][0])
        combined[1].append(data[i][1])
        combined[2].append(timestamps[i][0])
        combined[3].append(timestamps[i][1])

    df = pd.DataFrame(combined)
    df = pd.DataFrame.transpose(df)
    
    df.columns = ["pause_time", "memory_change",
                 "actual_time", "time_from_start"]
    return df


# Get the contents of the heap at each GC log moment. 
# Note:  UNIMPLEMENTED create_csv = true.
# Example:
# Heap could be 50% free, 25% young, 25% old at a moment in time. This
#   determines that breakdown from the log information, if it exists, and 
#   produces a frequencies list for it.
def getHeapAllocation(create_csv = False):
    accepting = False
    heap_regions = []
    with open(path, "r") as file:
        filedata = file.readlines()
        idx = 0
        filesize = len(filedata)
        while (idx < filesize):
            if "Heap Regions" in filedata[idx]:
                accepting = True
                heap_regions.append([])
            elif accepting and "0x" not in filedata[idx]:
                accepting = False
            elif accepting:
                heap_regions[-1].append(filedata[idx])
            idx += 1
    parsed_heap_regions = __simplify_regions(heap_regions)
    if create_csv:
        print("Creating a CSV is Unimplemented currently")
    return parsed_heap_regions


def __simplify_regions(heap_regions):
    # https://regex101.com 
    pattern = "[GC]\(\d*\)\s*\|\s*(\d+)\|0x((\d|\w)*),\s*0x((\d|\w)*),\s+0x((\d|\w)*)\|(\s*)(\d*)%\|(\s*)(\w+)"
    # Searches for the following string:
        # GC(0) |  1|0x0000abc123, 0x0000abc321, 0x0000234321| 25%|  O|
        # with anything changing (all numbers, ect.) other than non letter-number characters.
    # group we are looking for: 11
    simplifed = [] 
    for entry in heap_regions:
        metadata = [] 
        for line in entry:
            match = re.search(pattern, line)
            if match:
                metadata.append(match.group(11))
        simplifed.append(metadata)
    
    ## List contains the different categories of memory blocks.
    
    ''' Heap Regions: E=young(eden), S=young(survivor), O=old, HS=humongous(starts)
     HC=humongous(continues), CS=collection set, F=free, OA=open archive
     CA=closed archive, TAMS=top-at-mark-start (previous, next) '''

    
    regions = ["E", "S", "O", "HS", "HC", "CS", "F", "OA", "CA", "TAMS"]
    counts = [] # will hold all frequency lists
    for heap_state in simplifed:
        frequencies = []
        [frequencies.append(0) for i in regions]
        for mem_block in heap_state:
            for i in range(len(regions)):
                if regions[i] == mem_block:
                    frequencies[i] += 1
                    break
        counts.append(frequencies)
    
    return counts


def getHeapInitialState(create_csv = False):
    
    
    # I will attempt two approaches
    #1) Finding the  'text' using regex groups, then searching for 
    # keywords there
    line_key = '\[*(.*)\]*\[\d+\.\d+\w+\]\[(.*)\[(.*)\](.*)'
    important_info = "Heap\sMin\sCapacity:\s*(.+)\s|Heap\sRegion Size:\s(.+)\s|Heap\sInitial Capacity:\s(.+)\s|Heap\sMax\sCapacity:\s(.+)\s|\s*Minimum\sheap\s(\d+)\s+Initial\sheap\s(\d+\w*)\s+Maximum\sheap\s(\d+)\s*|\s*Heap\s+region\s+size:\s*(\d*\w*)\s*"
                 # Min, Init, Max, Curr
    categories = [ 0,    0,    0,    0 ] 
    found_values = list([False for i in range(len(categories))])
    search_min  = "^\s*Heap\sMin\sCapacity:\s*(.+)\s*"
    search_init = "^\s*Heap\sInitial Capacity:\s(.+)\s*"
    search_max  = "^\s*Heap\sMax\sCapacity:\s(.+)\s*"
    search_region_size = "^\s*Heap\sRegion Size:\s(.+)\s*|\s*Heap\s+region\s+size:\s*(\d*\w*)\s*"
    search_three = "^\s*Minimum\sheap\s(\d+)\s+Initial\sheap\s(\d+\w*)\s+Maximum\sheap\s(\d+)\s*"
    searchables = [search_min, search_init, search_max, search_region_size]
    my_dictionary = {k: f(v) for k, v in my_dictionary.items()}

    with open(path, "r") as file:
        for line in file:
            match = re.search(line_key, line)
            if match:
                line_text = match.group(len(match.groups()))
                for idx in range(len(searchables)):
                    match = re.search(str(searchables[idx]), line_text)
                    if match:
                        print(str(match) + "~" +  str(searchables[idx]))
                    
                match = re.search(search_three, line_text)
                if match:
                    print(match)    

    #2) Matching directly with regex.
    # to compare runtime. :) 
    
def getHeapInitialState2(create_csv = False):

    # Put all needed mappings into a dictionary
    to_search = {}
    
    to_search["Min"]    = "^\s*Heap\s+Min\s+Capacity:\s*(.+)\s*"
    to_search["Init"]   = "^\s*Heap\s+Initial\s+Capacity:\s*(.+)\s*"
    to_search["Max"]    = "^\s*Heap\s+Max\s+Capacity:\s*(.+)\s*"
    to_search["Region"] = "^\s*Heap\s+Region\s+Size:\s*(.+)\s*"

#########TODO: Compare runtime after removing the wildcards######## 
#    to_search["Min"]    = "^\s*Heap\s+Min\s+Capacity:\s*(.+)\s*"
#    to_search["Init"]   = "^\s*Heap\s+Initial\s+Capacity:\s*(.+)\s*"
#    to_search["Max"]    = "^\s*Heap\s+Max\s+Capacity:\s*(.+)\s*"
#    to_search["Region"] = "^\s*Heap\s+Region\s+Size:\s*(.+)\s*"
#####################################################################
    #|\s*Heap\s+region\s+size:\s*(\d*\w*)\s* <- extra
    
    
    dict_keys = ["Min", "Init", "Max", "Region"]
    found_values = {}
    for key in dict_keys:
        found_values[key] = 0
    

    log_line_key = '\[*(.*)\]*\[\d+\.\d+\w+\]\[(.*)\[(.*)\](.*)'
    with open(path, "r") as file:
        # read every line in the log file
        for line in file:
            # find the "non tag" region of each line
            match_info = re.search(log_line_key, line)
            # if found
            if match_info:
                # access the "non tag" region of that line
                non_tag_text = match_info.group(len(match_info.groups()))
                # get all things we are still searching for 
                keys = list(to_search.keys())

                for i in range(len(keys)): # use index because changes size
                    # for all possible search categories, check if line has a 
                    # match
                    possible_match = re.search(to_search[keys[i]], non_tag_text)
                    # If there is a match, we can remove this from our list to
                    # search. Save the value found to the array.
                    if possible_match:
                        del to_search[keys[i]]
                        found_values[keys[i]] = possible_match.group(len(possible_match.groups()))
            
            if not to_search: # If the dictionary to search is empty.
                break
            
    print(found_values)


                
    
    
    