## # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # ##                               lineMetadata
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
    # return  '^\[*(.*)\]*\[(\d+\.\d+\w+)\]\[(.*)\]\[(.*)\].*\s*'
    return "^(\[\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d\.\d{3}\+\d{4}\])?\[(\d+\.\d+\w+)\]\[(\w+ ?)\]\[gc(\w+,?){0,2}\s*\] GC\(\d+\) "


## # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#                               searchActions
#   Purpose:
#       Parse an entire log line, and extract each and only the metadata
#
#   Return:
#       A regex searchable string for this particular field
#
#   Regex Group Info
#       1) Type of action: (concurrent or pause)
#       2) Description of concurrent/pause. (Cleanup? Young GC?)
#       3) Extra info on pause, if any.
#       4) Starting size of region in MB
#       5) Ending size of region in MB
#       6) Heapsize remaining
#       7) Time taken in miliseconds
#
##  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def searchActions():
    # return "((?:Concurrent)|(?:Pause)) ((?:\w+ ?){1,3}) (\((?:\w+ ){1, 3}\) {0, 2})?(\d+\w->\d+\w\(?\d+?\w?\)?){0,1}(\((?:\w+ ?){0,2}\))? ?(\d+\.\d+)ms"
    return "((?:Concurrent)|(?:Pause)) ((?:\w+ ?){1,3}) (\((?:\w+ ?){1,3}\) ){0,3}(\((?:\w+ ){1, 3}\) {0, 2})?(\d+\w->\d+\w\(?\d+?\w?\)?){0,1}(\((?:\w+ ?){0,2}\))? ?(\d+\.\d+)ms"


def getSearchRegex():
    return lineMetadata() + searchActions()


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


def trueString():
    # return "^(\[\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d\.\d{3}\+\d{4}\])?\[(\d+\.\d+\w+)\]\[(\w+ ?)\]\[gc\s*\] GC\(\d+\) ((?:Concurrent)|(?:Pause)) ((?:\w+ ?){1,3}) (\((?:\w+ ?){1,3}\) ){0,3}(\d+\w->\d+\w\(?\d+?\w?\)?){0,1} ?(\d+\.\d+)ms"
    return "^(\[\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d\.\d{3}\+\d{4}\])?\[(\d+\.\d+\w+)\]\[(\w+ ?)\]\[gc(?:,\w+)?\s*\] GC\(\d+\) ((?:Concurrent)|(?:Pause)) ((?:\w+ ?){1,3}) (\((?:\w+ ?){1,3}\) ){0,3}(\d+\w->\d+\w\(?\d+?\w?\)?){0,1} ?(\d+\.\d+)ms"


import re
import time


def main():
    startTime = time.time()
    filename = "/Users/ellisbrown/Desktop/Project/datasets/demo_data/demo_g1_limited.log"
    # filename = "/Users/ellisbrown/Desktop/Project/datasets/gc.log"
    # print("/.../" + filename[43:])
    table = manyMatch_LineSearch(trueString(), filename)
    # for idx in range(len(table)):
    #     print("Idx:", idx)
    #     print("")
    #     print(table[idx])
    #     print("\n\n")
    # print(getSearchRegex())
    print(len(table[0]))
    # print("time: ", time.time() - startTime)


main()
