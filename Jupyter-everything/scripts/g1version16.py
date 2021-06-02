
# Defines string formats to be exported
import re # regular expressions
# Returns a regex searchable string.
# Strings are expected to have exactly one group of interest


## # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#                               YoungPause
#   Purpose:
#       Finds the timing associated with a Young Pause in Garbage Collection
#   
#   Return:
#       A regex searchable string for this particular field
# 
#   Regex Group Info
#       1) Change in memory allocation
#       2) Time spent
#
##  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
def YoungPause():
    return ".*Pause Young.*?(\d+\w*->\d+\w*\(*.*\)*)\s(\d+.*)\s*"


## # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#                               PauseCleanup
#   Purpose:
#       Finds timing associated with a Pause Cleanup GC action
#   
#   Return:
#       A regex searchable string for this particular log field
# 
#   Regex Group Info
#       1) Change in data allocated
#       2) Time spent
#
##  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
def PauseCleanup():
    return ".*Pause Cleanup.*?(\d+\w*->\d+\w*\(*.*\)*) (\d+.*)\s"

## # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#                               PauseRemark
#   Purpose:
#       Finds timing associated with a Pause Remark GC action
#   
#   Return:
#       A regex searchable string for this particular log field
# 
#   Regex Group Info
#       1) Change in data allocated
#       2) Time spent
#
##  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
def PauseRemark():
    return ".*Pause Remark.*?(\d+\w*->\d+\w*\(*.*\)*) (\d+.*)\s"

## # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#                               DateTimestamp
#   Purpose:
#       Finds the date and time information in yyyy-mm-dd(T)hh:mm:ss:mmm
#   
#   Return:
#       A regex searchable string for this particular field
# 
#   Regex Group Info
#       1) Date time stamp info
#
##  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
def DateTimestamp():
    return "\[(\d\d\d\d-\d\d-\d\d.*)\]"


## # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#                               EdenHR
#   Purpose:
#       Finds the number and change in eden regions
#   
#   Return:
#       A regex searchable string for this particular field
# 
#   Regex Group Info
#       1) Initial number of regions
#       2) Final number of regions
#       3) Next anticipated number of young regions before GC runs
##  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
def EdenHR():
    return "\s+Eden regions:\s+(\d+)->(\d+)\(?(\d*)\)?\s*"


## # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#                               SurvivorHR
#   Purpose:
#       Finds the number of Survivor regions before/after GC run
#   
#   Return:
#       A regex searchable string for this particular field
# 
#   Regex Group Info
#       1) Number of survivor regions before gc
#       2) Number of survivor regions after gc
#       3) Number of anticipated survivor regions next gc cycle
#
##  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
def SurvivorHR():
    return "\s+Survivor regions:\s+(\d+)->(\d+)\(?(\d*)\)?\s*"


## # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#                                   OldHR
#   Purpose:
#       Finds the number of Old regions before/after GC run
#   
#   Return:
#       A regex searchable string for this particular field
# 
#   Regex Group Info
#       1) Number of old regions before GC run
#       2) Number of old regions after GC runs
#       
##  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
def OldHR():
    return "\s+Old regions:\s+(\d+)->(\d+)\(?\d*\)?\s*"


## # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#                               ArchiveHR
#   Purpose:
#       Finds the number of archive regions before/after gc run
#   
#   Return:
#       A regex searchable string for this particular field
# 
#   Regex Group Info
#       1) Number of archive regions before gc run
#       2) Number of archive regions after  gc run
#
##  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
def ArchiveHR():
    return "\s+Archive regions:\s+(\d+)->(\d+)\(?\d*\)?\s*"


## # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#                               HugeHR
#   Purpose:
#       Finds the count for Humongus regions before/after gc run
#   
#   Return:
#       A regex searchable string for this particular field
# 
#   Regex Group Info
#       1)
##  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
def HugeHR():
    return "\s+Humongous regions:\s+(\d+)->(\d+)\(?(\d*)\)?\s*"

## # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#                               HeapRegions_schema1
#   Purpose:
#       Finds the heap allocation for a single line (schema1)
#   
#   Return:
#       A regex searchable string for this particular field
# 
#   Regex Group Info
#       1-10) Not needed currently, but each field of the line
#       11) The heap region categorization 
#
##  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
def HeapRegions_schema1():
    return "[GC]\(\d*\)\s*\|\s*(\d+)\|0x((\d|\w)*),\s*0x((\d|\w)*),\s+0x((\d|\w)*)\|(\s*)(\d*)%\|(\s*)(\w+)"


## # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#                               HeapMinCapacity
#   Purpose:
#       Find the minimum heap capacity at runtime start
#   
#   Return:
#       A regex searchable string for this particular field
# 
#   Regex Group Info
#       1) Min Heap capacity (integer with a metric unit)
#
##  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
def HeapMinCapacity():
    return "^\s*Heap\s+Min\s+Capacity:\s*(.+)\s*"


## # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#                               HeapInitialCapacity
#   Purpose:
#       Find the Heap Initial Capacity at runtime start
#   
#   Return:
#       A regex searchable string for this particular field
# 
#   Regex Group Info
#       1) Initial Heap Capacity (integer with a metric unit)
#
##  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
def HeapInitialCapacity():
    return "^\s*Heap\s+Initial\s+Capacity:\s*(.+)\s*"


## # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#                               HeapMaxCapacity
#   Purpose:
#       Find the Heap Max Capacity at runtime start
#   
#   Return:
#       A regex searchable string for this particular field
# 
#   Regex Group Info
#       1) HeapMaxCapacity (integer with a metric unit)
#
##  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
def HeapMaxCapacity():
    return "^\s*Heap\s+Max\s+Capacity:\s*(.+)\s*"


## # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#                               HeapRegionSize
#   Purpose:
#       Find the Heap Region Size at program start
#   
#   Return:
#       A regex searchable string for this particular field
# 
#   Regex Group Info
#       1) Heap Region Size (integer with a metric unit)
#
##  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
def HeapRegionSize():
    return "^\s*Heap\s+Region\s+Size:\s*(.+)\s*"


## # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#                            HeapRegionSize_schema1
#   Purpose:
#       Find the Heap Region Size at program start
#   
#   Return:
#       A regex searchable string for this particular field
# 
#   Regex Group Info
#       1) Program region size (integer with a metric unit)
#
##  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
def HeapRegionSize_schema1():
    return "\s*Heap\s+region\s+size:\s*(\d*\w*)\s*"


## # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#                             HeapInitalMaxMin_schema1
#   Purpose:
#       Find Heap Inital, Max, and Min (schema1) at program start
#   
#   Return:
#       A regex searchable string for this particular field
# 
#   Regex Group Info
#       1) Minimum Heap Size (integer with a metric unit)
#       2) Initial Heap Size (integer with a metric unit)
#       3) Maximum Heap Size (integer with a metric unit)
#
##  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
def HeapInitalMaxMin_schema1():
    return "\s*Minimum\sheap\s(\d+)\s+Initial\sheap\s(\d+\w*)\s+Maximum\sheap\s(\d+)\s*"


## # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#                               fullLineInfo
#   Purpose:
#       Parse an entire log line, and extract each region
#   
#   Return:
#       A regex searchable string for this particular field
# 
#   Regex Group Info
#       1) DateTime information (if present)
#       2) Time since program began (integer with a metric unit)
#       3) Reason for log entry [info/debug/...]
#       4) gc phase
#       5) log line info
#
##  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
def fullLineInfo():
    return  '^\[*(.*)\]*\[(\d+\.\d+\w+)\]\[(.*)\]\[(.*)\](.*)\s+'



## # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#                               lineMetadata
#   Purpose:
#       Parse an entire log line, and extract each and only the metadata 
#   
#   Return:
#       A regex searchable string for this particular field
# 
#   Regex Group Info
#       1) DateTime information (if present)
#       2) Time since program began (integer with a metric unit)
#       3) Reason for log entry [info/debug/...]
#       4) gc phase
#
##  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
def lineMetadata():
    return  '^\[*(.*)\]*\[(\d+\.\d+\w+)\]\[(.*)\]\[(.*)\].*\s*'



# Metadata that can be searched for. TODO: Add formal documentation
def G1Metadata_titles():
    categories = ["Version", "CPUs", "Memory", "Large Page Support",
                  "NUMA Support", "Compressed Oops", "Pre-touch", 
                  "Parallel Workers", "Heap Region Size",
                  "Heap Initial Capacity", "Heap Max Capacity", 
                  "Heap Min Capacity", "Concurrent Workers", 
                  "Concurrent Refinement Workers", "Periodic GC"]
    return categories

def G1Metadata_searchable():
    sections = G1Metadata_titles()
    searchables = []
    for section in sections:
        searchables.append(".*\s" + section + ":\s(.+)\s*")
    return searchables

## # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#                         manyMatch_LineSearch
#   Purpose:
#       Search through a data set, and return a list of all matches
#   
#   Parameters:
#       match_terms      : Terms to search for within data set
#       num_match_groups : Integer representing number groups to remember
#       data             : List of data to be searched
#       filepath         : string File path to file containing data to be read
#       in_file          : If True, open filepath specified for reading data.
#                          If false, the data is passsed in parameter "Data"       
#   Return:
#       List of lists:
#           ->  Outer list contains N lists, where N = num_match_groups.
#               The outer list can be described as the columns
#           -> Inner list contains all matches, for each associated group
#
## # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def manyMatch_LineSearch(match_terms = [],        # regex terms to search for
                        num_match_groups = 0,     
                        data = [],                # data to search
                        filepath = "",            # filepath of file to read
                        in_file = False):         # TRUE if data in a file
    if not match_terms or num_match_groups == 0:
        return []
    if in_file :
        file = open(filepath, "r")
        data = file.readlines()
    
    table = [[] for i in range(num_match_groups)]
    # If there has been listed groups of interest within the regex search
    for line in data:
        for term in match_terms:
            match = re.search(term, line)
            if match:
                # Find all matches of interest
                for i in range(1, num_match_groups + 1):
                    table[i - 1].append(match.group(i))
    return table


                    
## # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#                         singleMatch_LineSearch                               #
#   Purpose:                                                                   #
#       Search through a data set, return the first of all matches             #
#                                                                              #
#   Parameters:                                                                #
#       match_terms      : Terms to search for within data set                 #
#       data             : List of data to be searched                         #
#       search_titles    : Names for the search terms passed. Optional.        #
#       filepath         : string File path to file containing data to be read #
#       in_file          : If True, open filepath specified for reading data.  #
#                          If false, the data is passsed in parameter "Data"   #  
#   Return:                                                                    #    
#      A list containing the match terms with their corresponding output vals  #
#           where match term could be the actual match term, or the            #
#           corresponding "search_title" for that term                         #
#                                                                              #
## # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def singleMatch_LineSearch( match_terms = [],        # regex terms to search for   
                            data = [],
                            search_titles =[],              # data to search
                            filepath = "",            # filepath of file to read
                            in_file = False):
    # if nothing to search, done.
    if not match_terms:
        return {}
    # Obtain data, if needed
    if in_file :
        file = open(filepath, "r")
        data = file.readlines()
    
    # initalize dictionarys for searching/finding
    toSearch = {}
    found    = {}
    for term in match_terms:
        toSearch[term] = term

    for line in data:
        search_terms = list(toSearch.keys()) # get all terms to search
        for index in range(len(search_terms)): # iterate through using indicies
            term = search_terms[index]
            match = re.search(term, line)
            # if match, move from toSearch -> found
            if match: 
                del toSearch[term] # remove from searchable set
                found[term] = match.group(1)    # add to found set
        
        # Check if all things have been found (save runtime)
        if not toSearch:
            break

    # loop end. Transform dictionary into organized list. 
    return __sort_to_list(found, match_terms, search_titles)
    

## # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
#                            __sort_to_list()                                  #
#   Purpose:                                                                   #
#       Takes a dictionary, and turns it into a list in a particular order     #
#                                                                              #
#   Parameters:                                                                #
#       dictWords     : dictionary of key value pairs to be transformed        #
#       keysOrder     : all keys for the dictionary, in a specific order       #
#       search_titles : alternative titles for the keys, if wanted             #
#                                                                              #
#   Return:                                                                    #
#       Returns a list, where list[idx] = [key, value] from                    #
#       original dictionary.                                                   #
## # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def __sort_to_list(dictWords, keysOrder, search_titles):
    if not dictWords or not keysOrder:
        return 
    ordered = []
    if search_titles:
        for i in range(len(keysOrder)):
            ordered.append([search_titles[i], dictWords[keysOrder[i]]])
    else:
        for key in keysOrder:
            ordered.append([key, dictWords[key]])

    return ordered