import pandas as pd
import re

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


def loglineKey():
    return "^(\[\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d\.\d{3}\+\d{4}\])?\[(\d+\.\d+)s\]\[\w+ ?\]\[gc\s*\] GC\(\d+\) ((?:Pause)|(?:Concurrent)) ((?:\w+ ?){1,3}) (\((?:\w+ ?){1,3}\) ){0,3}(\d+\w->\d+\w\(?\d+?\w?\)?){0,1} ?(\d+\.\d+)ms"


def columnNames():
    return [
        "DateTime",
        "TimeFromStart_seconds",
        "EventType",
        "EventName",
        "AdditionalEventInfo",
        "MemoryChange_MB",
        "Duration_miliseconds",
    ]


def getParsedData(logfile):
    if not logfile:
        print("No logfile provided")
        return
    table = manyMatch_LineSearch(loglineKey(), logfile)
    df = pd.DataFrame(table).transpose()
    df.columns = columnNames()
    return df
