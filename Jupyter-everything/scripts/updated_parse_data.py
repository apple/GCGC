# Ellis Brown
# Purpose: Temporary parse_data.py, with no reliance on global variables.
import re
from numpy import NaN, number
import pandas as pd
from scripts import g1version16 as g1f  # g1format
from scripts import shenandoah_p as shen  # shenandoah regex

# Updated parse_data does not use global variables
def getPauses(logfile=None, gctype="", create_csv=False):

    if not logfile:
        print("No logfile supplied to function getPauses.")
        return
    if not gctype:
        gctype = get_gc_type(logfile)

    # get the regex search terms to look for based on the garbage collector type
    search_term = []
    if gctype == "G1":
        search_term = [
            g1f.lineMetadata() + g1f.YoungPause(),
            g1f.lineMetadata() + g1f.PauseRemark(),
            g1f.lineMetadata() + g1f.PauseCleanup(),
        ]
    elif gctype == "Shenandoah":
        search_term = shen.pauses()
    else:
        print("GCtype unknown. GcType = (", gctype, ") Abort.")

    # Search every line in the specified file
    table = g1f.manyMatch_LineSearch(
        match_terms=search_term,
        num_match_groups=6,  # check from g1f
        filepath=logfile,
        in_file=True,
    )
    if not table:
        print("Unable to find young pauses in data set")
        return []

    # Construct a pandas 2d table to hold returned information
    cols = [
        "DateTime",
        "TimeFromStart_seconds",
        "TypeLogLine",
        "GcPhase",
        "MemoryChange",
        "PauseDuration_miliseconds",
        "PauseType",
    ]
    columns = {cols[i]: table[i] for i in range(len(cols))}
    table_df = pd.DataFrame(columns)

    # remove the ms / s terminology from the ending
    table_df["PauseDuration_miliseconds"] = table_df["PauseDuration_miliseconds"].map(__remove_non_numbers)
    table_df["TimeFromStart_seconds"] = table_df["TimeFromStart_seconds"].map(__remove_non_numbers)

    # remove any possibly completly empty columns
    table_df.replace("", NaN, inplace=True)
    table_df.dropna(how="all", axis=1, inplace=True)

    # if create_csv:
    #     table_df.to_csv(__get_unique_filename("young_pauses.csv"))

    return table_df


## Returnns a list of all concurrent periods and their durations
def getConcurrentDurations(logfile=None, gctype="", create_csv=False):
    # Verify parameters are correct.
    if not logfile:
        print("No logfile supplied to function getConcurrentDurations.")
        return
    if not gctype:
        gctype = get_gc_type(logfile)

    print(gctype)
    # Use the log type to help parse the file
    if gctype == "Shenandoah":
        match_terms = [shen.ConcurrentLine()]
        num_groups = 8
    else:
        match_terms = [shen.ConcurrentLine()]
        num_groups = 8
        print("Not implemented: getConcurrentDurations on gctype (" + str(gctype) + ")")

    table = g1f.manyMatch_LineSearch(
        match_terms=match_terms,
        num_match_groups=num_groups,
        data=[],
        filepath=logfile,
        in_file=True,
    )

    if not table:
        print("Unable to find young pauses in data set")
        return []
    #### NOTE:  this is curtrently the same as GetPauses(). Consider modularizing
    # Construct a pandas 2d table to hold returned information
    cols = [
        "DateTime",
        "TimeFromStart_seconds",
        "TypeLogLine",
        "GcPhase",
        "ConcurrentPhase",
        "AdditionalNotes",
        "MemoryChange",
        "PauseDuration_miliseconds",
        "PauseType",
    ]
    columns = {cols[i]: table[i] for i in range(len(cols))}
    table = pd.DataFrame(columns)
    # remove the ms / s terminology from the ending
    # NOTE: it is important to remember that TimeFromStart_seconds is in seconds, while
    # PauseTime is in ms
    table["TimeFromStart_seconds"] = table["TimeFromStart_seconds"].map(__remove_non_numbers)
    table["ConcurrentPhase"]

    # remove any possibly completly empty columns
    table.replace("", NaN, inplace=True)
    table.dropna(how="all", axis=1, inplace=True)

    if create_csv:
        table.to_csv(__get_unique_filename("concurrent_pauses_shenandoah.csv"))

    return table


# Goes to each of the pauses in the garbage collector phases
# and dumps all data. TODO: Fix data and make it simpler
# Requirement: Path is set.
def getGCdataSections(logfile=None, gctype="", create_csv=False):
    # Verify parameters are correct.
    if not logfile:
        print("No logfile supplied to function getGCdataSections.")
        return
    if not gctype:
        gctype = get_gc_type(logfile)

    search_term = g1f.fullLineInfo()
    table = g1f.manyMatch_LineSearch(match_terms=[search_term], num_match_groups=6, filepath=logfile, in_file=True)
    table = table[:-1]  # remove column of only zeros.
    table_df = pd.DataFrame(table).transpose()
    if create_csv:
        table.to_csv(__get_unique_filename("all_data_" + str(logfile) + ".csv"))
    return table_df


# Finds the last GC log timestamp. Uses that to find time in seconds from
# start, and returns it as a float.
# Note: not efficient if looking to optimize
def getTotalProgramRuntime(logfile=None):
    # Verify parameters are correct.
    if not logfile:
        print("No logfile supplied to function getTotalProgramRuntime.")
        return
    # The following 5 lines are borrowed from this stack over flow question source
    # https://stackoverflow.com/questions/46258499/how-to-read-the-last-line-of-a-file-in-python/54278929#54278929
    with open(logfile, "rb") as file:
        file.seek(-2, os.SEEK_END)
        while file.read(1) != b"\n":
            file.seek(-2, os.SEEK_CUR)
        last_line = file.readline().decode()
        print(last_line)

        # Search for the metadata line match
        match_term = ".*\[(\d+\.\d+)s\].*"
        columns = g1f.manyMatch_LineSearch(match_terms=[match_term], num_match_groups=1, data=[last_line])
        # The columns is a list, contaning a list of columsn
        # enter column zero to get access to the associated match term
        # in column zero, enter row zero, to access the first and only entry
        return float(columns[0][0])


def getGCMetadata(logfile="", create_csv=False):
    if not logfile:
        print("No logfile supplied to function getGCMetadata.")
    # columns = each metadata term
    table = g1f.singleMatch_LineSearch(
        match_terms=g1f.G1Metadata_searchable(),
        search_titles=g1f.G1Metadata_titles(),
        filepath=logfile,
        in_file=True,
    )
    if create_csv:
        __create_csv(table, "gc_metadata.csv")
    return table


# Get the contents of the heap at each GC log moment.
# Note:  UNIMPLEMENTED create_csv = true.
# Example:
# Heap could be 50% free, 25% young, 25% old at a moment in time. This
#   determines that breakdown from the log information, if it exists, and
#   produces a frequencies list for it.
def getHeapAllocation(logfile="", gctype=None, create_csv=False, robust=False):
    # Verify parameters are correct.
    if not logfile:
        print("No logfile supplied to function getHeapAllocation.")
        return
    if not gctype:
        gctype = get_gc_type(logfile)

    if not robust:
        return __getHeapAllocation(logfile, gctype, create_csv)
    accepting = False
    heap_regions = []
    with open(logfile, "r") as file:
        for line in file:
            if "Heap Regions" in line:
                accepting = True
                heap_regions.append([])
            elif accepting and "0x" not in line:
                accepting = False
            elif accepting:
                heap_regions[-1].append(line)

    parsed_heap_regions = __simplify_regions(heap_regions)
    if create_csv:
        __create_csv(parsed_heap_regions, "heap_allocation.csv")
    return parsed_heap_regions


############### ############### ###############
#      Private functions defined below        #
############### ############### ###############


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


# This is hard to transform with readable code.
# TODO: transform such that return type is reasonable.
def __getHeapAllocation(logfile="", gctype="", create_csv=False):

    to_search = {}
    to_search["Eden"] = g1f.EdenHR()
    to_search["Survivor"] = g1f.SurvivorHR()
    to_search["Old"] = g1f.OldHR()
    to_search["Archive"] = g1f.ArchiveHR()
    to_search["Huge"] = g1f.HugeHR()

    heap_regions = {}  # Create collection to add to
    # Initalize the lists we will append to, based on what is found
    for key in to_search.keys():
        heap_regions[key] = []
    heap_regions["Time"] = []

    # Helps focus search onto "non tag" regions of each log line
    log_line_key = "\[*(.*)\]*\[(\d+\.\d+)\w+\]\[(.*)\[(.*)\](.*)"

    with open(logfile, "r") as file:
        for line in file:
            match_info = re.search(log_line_key, line)
            # if found
            if match_info:
                non_tag_text = match_info.group(len(match_info.groups()))
                for key in to_search.keys():
                    # Search for each of the interesting fields.
                    m = re.search(to_search[key], non_tag_text)
                    # m is a possibe match
                    if m:
                        heap_regions[key].append((m.group(1), m.group(2)))
                        if key == "Eden":
                            heap_regions["Time"].append(match_info.group(2))

    # Warning:
    # The following is O(n)*c runtime, on filesize, where c is fairly large
    # Calculate the total memory avilable, to correctly display
    # Graph containing 'free' memory

    return heap_regions


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
        # Im not sure what could hit this case.
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


def __getHeapInitialState(filepath, create_csv, robust):
    # Put all needed mappings into a dictionary
    to_search = {}  # regex strings for different fields
    if not robust:  # Different style logs. Determine which it is from global vars.
        to_search["Min"] = "^\s*Heap\s+Min\s+Capacity:\s*(.+)\s*"
        to_search["Init"] = "^\s*Heap\s+Initial\s+Capacity:\s*(.+)\s*"
        to_search["Max"] = "^\s*Heap\s+Max\s+Capacity:\s*(.+)\s*"
        to_search["Region"] = "^\s*Heap\s+Region\s+Size:\s*(.+)\s*"
    else:
        to_search["Region"] = "\s*Heap\s+region\s+size:\s*(\d*\w*)\s*"
        to_search["Metadata"] = "\s*Minimum\sheap\s(\d+)\s+Initial\sheap\s(\d+\w*)\s+Maximum\sheap\s(\d+)\s*"

    # Create a set of found values.
    found_values = {}
    # Log line key is used to ignore parsing date-time & tag information
    log_line_key = "\[*(.*)\]*\[\d+\.\d+\w+\]\[(.*)\[(.*)\](.*)"
    with open(filepath, "r") as file:
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

                for i in range(len(keys)):  # use index because changes size
                    # for all possible search categories, check if line has a
                    # match
                    possible_match = re.search(to_search[keys[i]], non_tag_text)
                    # If there is a match, we can remove this from our list to
                    # search. Save the value found to the array.
                    if possible_match:
                        del to_search[keys[i]]
                        # Every interesting value lives in its own line
                        if not robust:
                            found_values[keys[i]] = possible_match.group(len(possible_match.groups()))
                        # This log schema has all on one line, so make 3 entries
                        # to the found dictionary, if we found 3. Else, 1
                        elif robust:
                            if len(possible_match.groups()) > 2:
                                found_values["Min"] = possible_match.group(1)
                                found_values["Init"] = possible_match.group(2)
                                found_values["Max"] = possible_match.group(3)
                            else:
                                found_values[keys[i]] = possible_match.group(len(possible_match.groups()))

            if not to_search:  # If the dictionary to search is empty.
                break
    # If create_csv parameter True, write to csv specified format.
    if create_csv:
        with open(__get_unique_filename("heap_initial_state.csv"), "w") as file:
            for k in found_values.keys():
                file.write(str(k) + ", " + str(found_values[k]) + "\n")

    return found_values  # Note: no particular order in return's formation


# Determines the type of file being read
def get_gc_type(filepath):

    file = open(filepath, "r")
    lines_read = 0
    # Look through the first 100 log lines to find
    # what garbage collector being used
    while lines_read < 100:
        line = file.readline()
        if "Using G1" in line:
            return "G1"
        if "Using Shenandoah" in line:
            gctype = "Shenandoah"
            return "Shenandoah"
        lines_read += 1

    # if none found, use a more general search to look for used garbage collectors
    # reopen the file to begin search from start.
    lines_read = 0
    file.close()
    file = open(filepath, "r")
    line = file.readline()
    while lines_read < 100:
        if "G1" in line:
            return "G1"
        if "Shenandoah" in line:
            return "G1"
        lines_read += 1
    print("Warning: GC Type not set, defaulting to G1")
    return "G1"


# removes non number (and decimal point) chars.
def __remove_non_numbers(string_with_number):
    # regex string, remove anything thats not 0-9, or a "."
    return float(re.sub("[^0-9/.]", "", string_with_number))


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
        for i in range(num_chars):  # -3 for the ".csv" ending
            if filename[i:num_chars].isnumeric():
                digits = int(filename[i:num_chars])
                count = i
                break
        filename = filename[0:count] + str(digits + 1) + ".csv"
        # make sure the new created filename is unique.
        filename = __get_unique_filename(filename)

    return filename
