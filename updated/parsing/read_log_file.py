# read_log_file.py

# defines functions to parse and extract information from a specified log file
# Ellis Brown, June 2021

import pandas as pd
import re

# Returns a regex-searchable string to handle parsing log lines.
# Defined regex groups are each section of the code
def __get_parsing_string():
    return "Hello"


# Defines a regex string to parse events from a general log file
# The regex defines the following groups
# GROUP 1: "DateTime" -> information on time of recording
# GROUP 2: "TimeFromStart_seconds" -> time of beginning of event in seconds
# GROUP 3: "EventType" -> Either concurrent or stop the world pause
# GROUP 4: "EventName" -> Specific action from the event. Example : "(pause) Young"
# GROUP 5: "AdditionalEventInfo" -> Information about the event
# GROUP 6: "MemoryChange_MB" -> Memory changed, following this patten: before->after(max_heapsize)
# GROUP 7: "Duration_miliseconds" -> How long it took for the event to occur in miliseconds
def event_parsing_string():
    # Implementation note: Be aware that spaces within the strings are intentional.
    datetime = "^(\[\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d\.\d{3}\+\d{4}\])?"
    timefromstart = "\[(\d+\.\d+)s\]"
    outputlevel = "\[\w+ ?\]"
    phase = "\[gc\s*\]"  # NOTE: this does NOT accept anything but gc level outputs
    log_number = " GC\(\d+\) "
    event_type = "((?:Pause)|(?:Concurrent)) "
    event_name = "((?:\w+ ?){1,3}) "
    additional_event_info = "{(\((?:\w+ ?){1,3}\) ){0,3}"
    memory_change = "(\d+\w->\d+\w\(?\d+?\w?\)?){0,1} ?"
    event_duration_ms = "(\d+\.\d+)ms"

    return (
        datetime
        + timefromstart
        + outputlevel
        + phase
        + log_number
        + event_type
        + event_name
        + additional_event_info
        + memory_change
        + event_duration_ms
    )


# Access the column names for a parsed file. Note that these are dependent
# on the groups defined in event_string_parsing
def __columnNames():
    return [
        "DateTime",
        "TimeFromStart_seconds",
        "EventType",
        "EventName",
        "AdditionalEventInfo",
        "MemoryChange_MB",
        "Duration_miliseconds",
    ]


## # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#                         manyMatch_LineSearch
#   Purpose:
#       Search through a file and return a list of matches for a regex search term
#
#   Parameters:
#       search_term      : string-> Terms to search for within data set
#       filepath         : string-> file path to log file
#   Return:
#       2 dimensional list structure. List of group's matches
#       table[index] = list of all matches associated with group at index - 1
#
## # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def manyMatch_LineSearch(
    match_term=None,  # regex terms to search for
    filepath=None,
):  # TRUE if data in a file
    num_match_groups = re.compile(match_term).groups
    table = [[] for i in range(num_match_groups)]
    # If there has been listed groups of interest within the regex search
    file = open(filepath, "r")
    for line in file:
        match = re.search(match_term, line)
        if match:
            # Find all matches of interest
            for i in range(0, num_match_groups):
                table[i].append(match.group(i + 1))  # +1 because group(0) is the whole string
            # add the match group number hit, so able to tell what match

    return table


# Given a filepath to a log file, create a pandas dataframe holding all information
# for that log file. Each row is a different event.
def getParsedData(logfile):
    if not logfile:
        print("No logfile provided")
        return
    table = manyMatch_LineSearch(event_parsing_string(), logfile)
    parsed_data_table = pd.DataFrame(table).transpose()  # transpose to orient correctly
    parsed_data_table.columns = __columnNames()  # add column titles, allow for clear references
    return parsed_data_table
