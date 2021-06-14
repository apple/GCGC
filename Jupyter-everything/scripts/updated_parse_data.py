# Ellis Brown
# Purpose: Temporary parse_data.py, with no reliance on global variables.
import re
from numpy import NaN, number
import pandas as pd 
from scripts import g1version16 as g1f # g1format
from scripts import shenandoah_p as shen #shenandoah regex
# Updated parse_data does not use global variables
def getPauses(logfile = None, gctype = "", create_csv = False):
    
    if not logfile:
        print("No logfile supplied to function getPauses.")
        return
    if not gctype:
        gctype = __set_gc_type(logfile)
    
    
    # get the regex search terms to look for based on the garbage collector type
    search_term = []
    if gctype == "G1":
        search_term = [g1f.lineMetadata() + g1f.YoungPause(),
                       g1f.lineMetadata() + g1f.PauseRemark(),
                       g1f.lineMetadata() + g1f.PauseCleanup()]
    elif gctype == "Shenandoah":
        search_term = shen.pauses()
    else:
        print("GCtype unknown. GcType = (", gctype, ") Abort.")

    # Search every line in the specified file
    table = g1f.manyMatch_LineSearch(match_terms = search_term, 
                                     num_match_groups = 6, # check from g1f
                                     filepath = logfile, 
                                     in_file = True)
    if not table:
        print("Unable to find young pauses in data set")
        return []
    
    # Construct a pandas 2d table to hold returned information
    cols = ["DateTime", "TimeFromStart_seconds", "TypeLogLine", "GcPhase", "MemoryChange", "PauseDuration_miliseconds", "PauseType"]
    columns = {cols[i] : table[i] for i in range(len(cols))}
    table_df = pd.DataFrame(columns)
    
    # remove the ms / s terminology from the ending
    table_df["PauseDuration_miliseconds"] = table_df["PauseDuration_miliseconds"].map(__remove_non_numbers)
    table_df["TimeFromStart_seconds"] = table_df["TimeFromStart_seconds"].map(__remove_non_numbers)
    
    # remove any possibly completly empty columns    
    table_df.replace("", NaN, inplace=True)
    table_df.dropna(how='all', axis=1, inplace=True)
    
    
    # if create_csv:
    #     table_df.to_csv(__get_unique_filename("young_pauses.csv"))

    return table_df





############### ############### ###############
#      Private functions defined below        #
############### ############### ###############
# Determines the type of file being read
def __set_gc_type(filepath):
    
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
            return
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
        lines_read += 1
    print("Warning: GC Type not set, defaulting to G1")
    gctype = "G1"
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
        for i in range(num_chars): # -3 for the ".csv" ending
            if filename[i:num_chars].isnumeric():
                digits = int(filename[i:num_chars])
                count = i
                break
        filename = filename[0:count] + str(digits + 1)  + ".csv"
        # make sure the new created filename is unique.
        filename = __get_unique_filename(filename)
    
    return filename