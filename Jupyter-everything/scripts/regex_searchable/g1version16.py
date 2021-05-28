
# Defines string formats to be exported
import re # regular expressions
# Returns a regex searchable string.
# Strings are expected to have exactly one group of interest

def EXample_String():
    return "Example"

def YoungPause():
    return ".*Pause Young.*?(\d+\w*->\d+\w*\(*.*\)*) (\d+.*)\s"

def PauseCleanup():
    return ".*Pause Cleanup.*?(\d+\w*->\d+\w*\(*.*\)*) (\d+.*)\s"

def DateTimestamp():
    return "\[\d\d\d\d-\d\d-\d\d.*\]"

def EdenHR():
    return "\s+Eden regions:\s+(\d+)->(\d+)\(?(\d*)\)?\s*"

def SurvivorHR():
    return "\s+Survivor regions:\s+(\d+)->(\d+)\(?(\d*)\)?\s*"

def OldHR():
    return "\s+Old regions:\s+(\d+)->(\d+)\(?(\d*)\)?\s*"

def ArchiveHR():
    return "\s+Archive regions:\s+(\d+)->(\d+)\(?(\d*)\)?\s*"

def HugeHR():
    return "\s+Humongous regions:\s+(\d+)->(\d+)\(?(\d*)\)?\s*"

def HeapRegions_schema1():
    return "[GC]\(\d*\)\s*\|\s*(\d+)\|0x((\d|\w)*),\s*0x((\d|\w)*),\s+0x((\d|\w)*)\|(\s*)(\d*)%\|(\s*)(\w+)"

def HeapMinCapacity():
    return "^\s*Heap\s+Min\s+Capacity:\s*(.+)\s*"

def HeapInitialCapacity():
    return "^\s*Heap\s+Initial\s+Capacity:\s*(.+)\s*"

def HeapMaxCapacity():
    return "^\s*Heap\s+Max\s+Capacity:\s*(.+)\s*"

def HeapRegionSize():
    return "^\s*Heap\s+Region\s+Size:\s*(.+)\s*"

def HeapRegionSize_schema1():
    return "\s*Heap\s+region\s+size:\s*(\d*\w*)\s*"

def HeapInitalMaxMin_schema1():
    return "\s*Minimum\sheap\s(\d+)\s+Initial\sheap\s(\d+\w*)\s+Maximum\sheap\s(\d+)\s*"

# TODO: Document all possible regex groups
def fullLineInfo():
    return  '^\[*(.*)\]*\[(\d+\.\d+\w+)\]\[(.*)\[(.*)\](.*)\s+'

def G1Metadata():
    categories = ["Version", "CPUs", "Memory", "Large Page Support",
                  "NUMA Support", "Compressed Oops", "Pre-touch", 
                  "Parallel Workers", "Heap Region Size",
                  "Heap Initial Capacity", "Heap Max Capacity", 
                  "Heap Min Capacity", "Concurrent Workers", 
                  "Concurrent Refinement Workers", "Periodic GC"]
    return categories


# Accepts a mapping that will iterate over the entire log file
# Expects to find many matches for each term.
# Returns table of results, and number of appended metadata columns (after)
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


                    





# NOTE: assumed all things fall into match group 1
def singleMatch_LineSearch( match_terms = [],        # regex terms to search for   
                            data = [],
                            ordered = False,              # data to search
                            filepath = "",            # filepath of file to read
                            in_file = False):

    if not match_terms:
        return {}
    
    if in_file :
        file = open(filepath, "r")
        data = file.readlines()
    
    toSearch = {}
    for term in match_terms:
        toSearch[term] = term
    
    found = {}

    for line in data:
        search_terms = list(toSearch.keys()) # get all terms to search
        for index in range(len(search_terms)): # iterate through using indicies
            term = search_terms[index]
            match = re.search(term, line)
            if match: 
                del toSearch[term] # remove from searchable set
                found[term] = match.group(1)    # add to found set
        if not toSearch:
            break
    if ordered:
        found = __sort_to_list(found, match_terms)
    return found

def __sort_to_list(dictWords, keysOrder):
    if not dictWords or not keysOrder:
        return 
    ordered = []
    for key in keysOrder:
        ordered.append([key, dictWords[key]])
    return ordered

