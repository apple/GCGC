# process_log.py

# # # # # # # # # # # # # # # # # # # # # # # # # # # 
# Purpose: Creates functions to process a           #
#          gc log file, extracting information      #
#          of specified types, and returning them.  #
#                                                   #
# Ellis Brown, 5/26/2020                            #
# # # # # # # # # # # # # # # # # # # # # # # # # # #
# Public functions                                  #
#                                                   #
# setLogPath          (string  path)                # 
# setLogSchema        (integer logtype)             #
# getPauses           (boolean create_csv)          #
# getHeapAllocation   (boolean create_csv)          #
# getHeapInitialState (boolea create_csv)           #
# # # # # # # # # # # # # # # # # # # # # # # # # # #
import pandas as pd
import re



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
    # Calculate potential Memory leaks? 


path= ""                # path to log data
output_csv_id = "extra" # name-scheme of output data file
log_schema = 0          # type of log formatted file.
'''Current log formats: 
    [0] amzn_workload 
    [1] gc.log
'''
    
 
# Set the path to the log file, which will then be parsed for specific 
# attributes.
def setLogPath(p):
    global path
    path = p

# Set the log schema type, which helps extract information and greatly
# reduce runtime.
# TODO: Implement a "-1" schema, which doesn't know which to use, and searches
# all possible log arrangements
def setLogSchema(logtype):
    global log_schema
    log_schema = logtype

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
            if "Full Pause" in line:
                print("FULL PAUSE WOOOOOOo")
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
    if (log_schema == 0):
        return __getHeapAllocation_schema0(create_csv)
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
    return [parsed_heap_regions]

def __getHeapAllocation_schema0(create_csv = False):
    
    to_search = {}
    to_search["Eden"]     = "\s+Eden regions:\s+(\d+)->(\d+)\(?(\d*)\)?\s*"
    to_search["Survivor"] = "\s+Survivor regions:\s+(\d+)->(\d+)\(?(\d*)\)?\s*"
    to_search["Old"]      = "\s+Old regions:\s+(\d+)->(\d+)\(?(\d*)\)?\s*"
    to_search["Archive"]  = "\s+Archive regions:\s+(\d+)->(\d+)\(?(\d*)\)?\s*"
    to_search["Huge"]     = "\s+Humongous regions:\s+(\d+)->(\d+)\(?(\d*)\)?\s*"

    heap_regions = {} # Create collection to add to
    # Initalize the lists we will append to, based on what is found
    for key in to_search.keys():
        heap_regions[key] = []
    
    # Helps focus search onto "non tag" regions of each log line
    log_line_key = '\[*(.*)\]*\[\d+\.\d+\w+\]\[(.*)\[(.*)\](.*)'
    with open(path, "r") as file:
        for line in file:
            match_info = re.search(log_line_key, line)
            # if found
            if match_info:
                non_tag_text = match_info.group(len(match_info.groups()))
                for key in to_search.keys():
                    # Search for each of the interesting fields.
                    m =  re.search(to_search[key], non_tag_text)
                    # m is a possibe match
                    if m:
                        heap_regions[key].append((m.group(1), m.group(2)))

    # Warning: 
    # The following is O(n)*c runtime, on filesize, where c is fairly large   
    # Calculate the total memory avilable, to correctly display
    # Graph containing 'free' memory
    inital_storage = __getHeapInitialState(False)
    init_cap = __remove_metrx_ending(inital_storage["Max"])
    init_region_size = __remove_metrx_ending(inital_storage["Region"])

    return [heap_regions, int(init_cap/init_region_size)]



# Takes in a number such as "1M" or "255G", and properly scales it 
# to fit the correct size. Deault unit it is 1 Megabyte (M)
# Returns as an int.
def __remove_metrx_ending(string):
    if len(string) >= 2:
        if string[-1] == "G":
            return int(string[:-1]) * 1000
        elif string[-1] == "M":
            return int(string[:-1])
        elif string[-1] == "T":
            print("Enconutered Terrabyte storage. First time, please check math")
            return int(string[:-1]) * 1000000
    else:
        #Im not sure what could hit this case.
        return int(string)

    



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


###############################################################################
#                   __getHeapInitialState_schema0()
#
# Purpose: Returns the heap inital state for a specific log style.
# Returns the information in a dictionary style.
#
# Requirement: Global variable "path" and "log_schema" must match log to analyze
#
# NOTE: Reads all log lines until all information is found.
#       In the case of an incorrect log format (information not found)
#       The runtime for this may take a very long time.
#
def getHeapInitialState(create_csv = False):
    return __getHeapInitialState(create_csv)

def __getHeapInitialState(create_csv):
    # Put all needed mappings into a dictionary
    to_search = {}      # regex strings for different fields
    if (log_schema == 0):# Different style logs. Determine which it is from global vars.
        to_search["Min"]    = "^\s*Heap\s+Min\s+Capacity:\s*(.+)\s*"
        to_search["Init"]   = "^\s*Heap\s+Initial\s+Capacity:\s*(.+)\s*"
        to_search["Max"]    = "^\s*Heap\s+Max\s+Capacity:\s*(.+)\s*"
        to_search["Region"] = "^\s*Heap\s+Region\s+Size:\s*(.+)\s*"
    elif (log_schema == 1):
        to_search["Region"] = "\s*Heap\s+region\s+size:\s*(\d*\w*)\s*"
        to_search["Metadata"] = "\s*Minimum\sheap\s(\d+)\s+Initial\sheap\s(\d+\w*)\s+Maximum\sheap\s(\d+)\s*"
    else:
        return "Unable to parse schema: " + str(log_schema)

    # Create a set of found values.
    found_values = {}    
    # Log line key is used to ignore parsing date-time & tag information
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
                        # Every interesting value lives in its own line
                        if log_schema == 0:
                            found_values[keys[i]] = possible_match.group(len(possible_match.groups()))
                        # This log schema has all on one line, so make 3 entries
                        # to the found dictionary, if we found 3. Else, 1
                        elif log_schema == 1:
                            if len(possible_match.groups()) > 2:
                                found_values["Min"]  = possible_match.group(1)
                                found_values["Init"] = possible_match.group(2)
                                found_values["Max"]  = possible_match.group(3)
                            else: 
                                found_values[keys[i]] = possible_match.group(len(possible_match.groups()))
            
            if not to_search: # If the dictionary to search is empty.
                break
    # If create_csv parameter True, write to csv specified format.
    if create_csv:
        with open("inital_state_" + output_csv_id + "_OUT.csv", "w") as file:
            for k in found_values.keys():
                file.write(str(k) + ", " + str(found_values[k]) + "\n")
    
    
    return found_values  # Note: no particular order in return's formation


# Goes to each of the pauses in the garbage collector phases
# and dumps all data. TODO: Fix data and make it simpler
# Requirement: Path is set.
def getGCdataSections(create_csv = False):
    if create_csv == True:
        print("Creating this CSV is currently unimplemented")
    # Helps focus search onto "non tag" regions of each log line
    log_line_key = '\[*(.*)\]*\[\d+\.\d+\w+\]\[(.*)\[(.*)\](.*)'
    gc_data_key = ".*GC\((\d+)\).*"
    data_cards = {}
    with open(path, "r") as file:
        for line in file:
            match_info = re.search(log_line_key, line)
            # if found
            if match_info:
                non_tag_text = match_info.group(len(match_info.groups()))
                m = re.search(gc_data_key, non_tag_text)
                if m:
                    key = m.group(len(m.groups()))
                    if not key in data_cards:
                        data_cards[key] = []
                    data_cards[key].append(non_tag_text)
    ## Temporary testing of idea ##
    
    for k in data_cards.keys():
        print("\n\n\n\n\n")
        for entry in data_cards[k]:
            print(entry)
    return data_cards

# Finds the last GC log timestamp. Uses that to find time in seconds from
# start, and returns it as a float.
# Note: not efficient if looking to optimize
def getTotalProgramRuntime():
    with open(path, "r") as file:
        data = file.readlines()
        
        final_line = data[-1]

        real_time, from_start = __get_timestamps(final_line)
        # Remove the "s" from the time from start. 
        return float(from_start[:-1])

# Purpose: Obtain metadata about a particular version of 
def getGCMetadata(create_csv = False):
    
    if log_schema != 0:
        print("getGCMetadata for log_schema " + str(log_schema) + " unimplemented")
        return
    
    to_search = {}
    categories = ["Version", "CPUs", "Memory", "Large Page Support",
                  "NUMA Support", "Compressed Oops", "Pre-touch", 
                  "Parallel Workers", "Heap Region Size",
                  "Heap Initial Capacity", "Heap Max Capacity", 
                  "Heap Min Capacity", "Concurrent Workers", 
                  "Concurrent Refinement Workers", "Periodic GC"]
    for item in categories:
        to_search[item] = "\s+" + str(item) + ":\s+(.+)\s*"
    metadata = {}
    # Helps focus search onto "non tag" regions of each log line
    log_line_key = '\[*(.*)\]*\[\d+\.\d+\w+\]\[(.*)\[(.*)\](.*)'
    with open(path, "r") as file:
        for line in file:
            match_info = re.search(log_line_key, line)
            # if found
            if match_info:
                non_tag_text = match_info.group(len(match_info.groups()))
                items = list(to_search.keys())

                for idx in range(len(items)):
                    # Search for each of the interesting fields.
                    m =  re.search(to_search[items[idx]], non_tag_text)
                    # m is a possibe match
                    if m:
                        del to_search[items[idx]]
                        metadata[items[idx]] = m.group(1)
            if not to_search:
                break
        
    return metadata