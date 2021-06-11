# parse_log_updated.py

# # # # # # # # # # # # # # # # # # # # # # # # # # # 
# Purpose: Creates functions to process a           #
#          gc log file, extracting information      #
#          of specified types, and returning them.  #
#                                                   #
# Ellis Brown, 5/26/2020                            #
# # # # # # # # # # # # # # # # # # # # # # # # # # #

import re
from numpy import NaN
import pandas as pd 
from scripts import g1version16 as g1f # g1format


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
gctype = ""
'''Current log formats: 
    [0] amzn_workload 
    [1] gc.log
'''


# ################# useful to know ####################
# throughout the code, variables are referenced as a "table"
#
#  table data structure

#  list of lists.
#  table = [ [...] [...] [...] [...] [...] ]
#  the inner lists represent the rows, and the outer lists
#  represent the data 
# len(list) == # number of columns
# len(list[idx])  == number of rows
# Rows all have same length 
# For all i in len(list) - 1, len(list[i]) = len(list[i + 1])

#########################################################
 
# Set the path to the log file, which will then be parsed for specific 
# attributes.
def setLogPath(filename = ''):
    global path
    path = filename
    __setGCType()



# gets the current log path
def getLogPath():
    global path
    return path

# Set the log schema type, which helps extract information and greatly
# reduce runtime.
# TODO: Implement a "-1" schema, which doesn't know which to use, and searches
# all possible log arrangements
def setLogSchema(logtype = 0):
    global log_schema
    log_schema = logtype


# #       -> getPauses
# # Purpose: Returns a CSV style list of all pauses from the Young Generation
# # Parameters : none
# # Requirements: path must be set to the .log file we look to traverse.
# # Return: List of tuples as pauses, with added metadata.
def getPauses(create_csv = False):
    with open(path, "r") as f:
        file_contents = f.readlines()
    
    # Extract metadata and info from each line
    search_term = [g1f.lineMetadata() + g1f.YoungPause(),
                   g1f.lineMetadata() + g1f.PauseRemark(),
                   g1f.lineMetadata() + g1f.PauseCleanup()]
    # note: by reading the g1f documentation, I know there are 6 regex groups.
    table = g1f.manyMatch_LineSearch(match_terms = search_term, 
                                     num_match_groups = 6,
                                     data = [],     #reading from file, no data
                                     filepath = path, #global
                                     in_file = True)
    if not table:
        print("Unable to find young pauses in data set")
        return []
    print("This far line 105")
    # Construct a pandas 2d table to hold returned information
    cols = ["DateTime", "TimeFromStart", "TypeLogLine", "GcPhase", "MemoryChange", "PauseDuration", "PauseType"]
    columns = {cols[i] : table[i] for i in range(len(cols))}
    table = pd.DataFrame(columns)
    
    # remove the ms / s terminology from the ending
    # NOTE: it is important to remember that TimeFromStart is in seconds, while
    # PauseTime is in ms
    table["PauseDuration"] = table["PauseDuration"].map(__remove_non_numbers)
    table["TimeFromStart"] = table["TimeFromStart"].map(__remove_non_numbers)
    
    # remove any possibly completly empty columns    
    table.replace("", NaN, inplace=True)
    table.dropna(how='all', axis=1, inplace=True)
    print("This far line 120")
    
    if create_csv:
        table.to_csv(__get_unique_filename("young_pauses.csv"))

    return table

####
# Purpose: Print the contents of a 'table' as a csv file
# Params : table , and filename. A unique filename will be created.
# returns nothing.
###

def __create_csv(table, filename):
    # Don't overwrite any data : get a unique filename.
    filename = __get_unique_filename(filename)
    with open(filename, "w") as file:
        # iterate through the rows
        for i in range(len(table[0])):
            # for each row, iterate through the columns
            for col in range(len(table)):
                # write in CSV format
                file.write(str(table[col][i]).strip() + ", ")
            file.write("\n")


# Returns a filename that is unique. If filename already exists,
# return the filename with the number 1 appended to the back. If 
# there is already a numbered version of the filename, increase the number.
import os.path 
def __get_unique_filename(filename):
    if not filename:
        return __get_unique_filename("default_filename.csv")

    if not os.path.exists(filename):
        return filename
    else:
        num_chars = len(filename) - 4
        count = num_chars
        digits = 0
        for i in range(num_chars): # -3 for the ".csv" ending
            if filename[i:num_chars].isnumeric():
                digits = int(filename[i:num_chars])
                count = i
                break
        filename = filename[0:count] + str(digits + 1)  + ".csv"
        filename = __get_unique_filename(filename)
    
    return filename



# removes non number (and decimal point) chars.
def __remove_non_numbers(string_with_number):
    return float(re.sub("[^0-9/.]", "", string_with_number))

     
# TODO: use? (is working correctly.)
# TODO: CONFIRM OUTPUT. (seems to work) This feature is paused while I go over
# code feedback
def getConcurrentMarkPauses(create_csv = False):
    match_terms = [g1f.lineMetadata() + g1f.PauseRemark(), 
                   g1f.lineMetadata() + g1f.PauseCleanup()]
    table = g1f.manyMatch_LineSearch(match_terms = match_terms,
                                    num_match_groups = 5,
                                    data = [],
                                    filepath = path,
                                    in_file = True)
    if create_csv:
        __create_csv(table, "Concurrent_mark_pauses.csv")
    return table

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
        __create_csv(parsed_heap_regions, "heap_allocation.csv")
    return [parsed_heap_regions]


# This is hard to transform with readable code.
# TODO: transform such that return type is reasonable.
def __getHeapAllocation_schema0(create_csv = False):
    
    to_search = {}
    to_search["Eden"]     = g1f.EdenHR()
    to_search["Survivor"] = g1f.SurvivorHR()
    to_search["Old"]      = g1f.OldHR()
    to_search["Archive"]  = g1f.ArchiveHR()
    to_search["Huge"]     = g1f.HugeHR()

    heap_regions = {} # Create collection to add to
    # Initalize the lists we will append to, based on what is found
    for key in to_search.keys():
        heap_regions[key] = []
    heap_regions["Time"] = []

    # Helps focus search onto "non tag" regions of each log line
    log_line_key = '\[*(.*)\]*\[(\d+\.\d+)\w+\]\[(.*)\[(.*)\](.*)'
 
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
                        if key == "Eden":
                            heap_regions["Time"].append(match_info.group(2))
                        

    
    # Warning: 
    # The following is O(n)*c runtime, on filesize, where c is fairly large   
    # Calculate the total memory avilable, to correctly display
    # Graph containing 'free' memory
    
    initial_storage = __getHeapInitialState(False)
    if initial_storage:
        init_cap = __remove_metrx_ending(initial_storage["Max"])
        init_region_size = __remove_metrx_ending(initial_storage["Region"])
        return [heap_regions, int(init_cap/init_region_size)]
    return [heap_regions, 0]



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

    



# Transforms lines on collected heap_regions into a table of heap allocation
# frequencies. Returns the table
def __simplify_regions(heap_regions):
    pattern = "[GC]\(\d*\)\s*\|\s*(\d+)\|0x((\d|\w)*),\s*0x((\d|\w)*),\s+0x((\d|\w)*)\|(\s*)(\d*)%\|(\s*)(\w+)"
    # Searches for the following string:
        # GC(0) |  1|0x0000abc123, 0x0000abc321, 0x0000234321| 25%|  O|
        # with anything changing (all numbers, ect.) other than non letter-number characters.
    # group we are looking for: 11
    simplified = [] 
    for entry in heap_regions:
        metadata = [] 
        for line in entry:
            match = re.search(pattern, line)
            if match:
                metadata.append(match.group(11))
        simplified.append(metadata)
    regions = ["F", "E", "S", "O", "HS", "HC", "CS", "OA", "CA", "TAMS"]
    
    # create a table with N columns, N = number of regions
    table = [[] for i in range(len(regions))]

    # add to each column of the table.
    for cell in simplified:
        for column in table:
            column.append(0)
        for item in cell:
            for i in range(len(regions)):
                if regions[i] == item:
                    table[i][-1] += 1

    return table    


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

    return data_cards

# Finds the last GC log timestamp. Uses that to find time in seconds from
# start, and returns it as a float.
# Note: not efficient if looking to optimize
def getTotalProgramRuntime():
    with open(path, "r") as file:
        data = file.readlines()        
        # get last logtime to view timestamp at program end
        final_line = data[-1]
        
        # Search for the metadata line match
        columns = g1f.manyMatch_LineSearch( match_terms = [g1f.fullLineInfo()],
                                  num_match_groups = 5,
                                  data = [final_line] )                                    
        # Data is returned in table format. Access table column 1
        # Access the only row, row 0
        # then remove the second "s" character to create a float.
        return float(columns[1][0][:-1])


def getGCMetadata(create_csv = False):
    if log_schema != 0:
        print("getGCMetadata for log_schema " + str(log_schema) + " unimplemented")
        return
    # columns = each metadata term
    table = g1f.singleMatch_LineSearch(match_terms = g1f.G1Metadata_searchable(),
                                      data = [],
                                      search_titles = g1f.G1Metadata_titles(),
                                      filepath = path,
                                      in_file  = True)
    if create_csv:
        __create_csv(table, "gc_metadata.csv")
    return table
    