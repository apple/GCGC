#       read_log_file.py
#
#   Given a log file, parse through that file and return a gc_events_dataframe containing all
#   relevant information from the log during runtime
#
#   Ellis Brown, 6/29/2021

import pandas as pd
import re
import glob

#       get_file_names_wildcard
#
#   Given a path including a linux style wildcard search, return the list of all matching files
#   on that path. Each file is a string.
#
def get_file_names_wildcard(path):
    files = []
    for file in glob.glob(path):
        files.append(file)
    return files


#       get_gc_event_tables
#
#   Take a list of list of log file paths/names, and construct a list of tables, one for
#   each log in the list.
#
def get_gc_event_tables(files, time_range_seconds, ignore_crashes = False):
    # Files must be a list of strings
    # Time range in seconds is either a list with 2 values,
    # or a single integer max time.
    if ignore_crashes:
        print("Warning: ignore_crashes takes log files and ignores all crashes.")
    if not files:
        print("Warning: Files list empty in get_parsed_comparions_from_files")
        return []
    # all_runs
    all_runs = []
    for filelist in files:
        gc_event_dataframes = [] # associated with one GC run. 
        for file in filelist:
            # Create each log gc_event_dataframe
            gc_event_dataframe = get_parsed_data_from_file(file, time_range_seconds, ignore_crashes)
            
            if not gc_event_dataframe.empty:
                gc_event_dataframes.append(gc_event_dataframe)
        if gc_event_dataframes:
            df = pd.concat(gc_event_dataframes)
            all_runs.append(df)
        else:
            print("Warning: No collected data for the following files: ", filelist)  
    if not all_runs:
        print("Error: No data collected in get_gc_event_tables.")
    return all_runs



## # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#                               get_parsed_data_from_file
#
# Purpose:
#   Given a filepath to a log file, create a pandas dataframe holding all information
#   for that log file. Each row is a different event.
#
# Parameters:
#   logfile -> a string with the path to the log file to read.
#
# Return:
#   a pandas dataframe, where rows are each an individual event. Columns are labeled, and
#   collect information on each event, such as when it occured, how long it lasted, and the name
## # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
from parse_log_line import event_parsing_string as eps
def get_parsed_data_from_file(logfile, time_range_seconds=None, ignore_crashes = False):
    assert isinstance(logfile, str)  # input must be a string
    
    if not logfile:
        print("No logfile provided in get_parsed_data_from_file")
        return
    table = __manyMatch_LineSearch(eps(), logfile)
    if not any(table):
        print("Unable to parse file " + str(logfile))
        return pd.DataFrame()
    # Some data collected is read in as a string, but needs to be interpreted as a float. Fix.
    
    table[1] = list(map(__number_to_float, table[1]))
    table[7] = list(map(__number_to_float, table[7]))
    table[5] = choose_non_zero(table[5], table[8]) # Before GC collection mem_size
    table[6] = choose_non_zero(table[6], table[9]) # After GC collection mem_size
    table[5] = list(map(__number_to_float, table[5])) 
    table[6] = list(map(__number_to_float, table[6]))
    
    

    # Schema 1 (JDK 16)
    temp = []
    for eventtype, safepoint1, safepoint2 in zip(table[2], table[10], table[16]):
        if safepoint1 or safepoint2:
            temp.append("Safepoint")
        else:
            temp.append(eventtype)
    table[2] = temp
    # table [10]  safepoint_name
    table[11] = list(map(__number_to_float, table[11])) # time_since_last_safepoint
    table[12] = list(map(__number_to_float, table[12])) # reaching_safepoint_time
    table[13] = list(map(__number_to_float, table[13])) # at_safepoint_time
    table[14] = list(map(__number_to_float, table[14])) # total_time_safepoint
    table[15] = list(map(__number_to_float, table[15])) # total_application_thread_stopped_time_seconds
    table[16] = list(map(__number_to_float, table[16])) # total_time_to_stop_seconds



# Scema 2 for safepoints:: Appears in JDK11
    # (?: Total time for which application threads were stopped: ([\d\.]+) seconds, Stopping threads took: ([\d\.]+) seconds$) 
 # 16 Total time application threads stopped in seconds
 # 17 Total time to stop in seconds

    table.pop(9) # Used due to 2 types of memory change regex groups & before/after for each
    table.pop(8) # Therefore, we gather before & after into 2 distinct columns, and remove other set

    parsed_data_table = pd.DataFrame(table).transpose() 
    # The data collected is in a 2d array, where table indicies represent a column. However,
    # a pandas dataframe expects each entry of the 2d array to be a row, not a column. Transpose
    # to fix this orientation error.

    parsed_data_table.columns = columnNames()  # add column titles, allow for clear references
    if time_range_seconds:
        min_time, max_time = __get_time_range(time_range_seconds)
        # Get the maximum and minimums and enforce the time range
        in_minimum = parsed_data_table["TimeFromStart_seconds"] >= min_time
        in_maximum = parsed_data_table["TimeFromStart_seconds"] <= max_time
        # Create the combined time table
        parsed_data_table = parsed_data_table[in_minimum & in_maximum] # Uses true from both other sections
    if ignore_crashes:
        return fix_timing_errors(parsed_data_table)
    else:
        if check_no_time_errors(parsed_data_table):
            return parsed_data_table
        else:
            print("Warning: Time error noticed in " + logfile+ ". This is typically due to a crash during runtime. Please locate the reset, split the logs into two sections, and run again.")
            return pd.DataFrame() 

#       check_no_time_errors
#
#   Looks through all rows of a gc_event_dataframe timing, and confirms
#   that there are no timing errors, meaning the time line never decreases.
#   For all lines x, time(x) <= time(x + n), n > 0. Otherwise, return false.
#
def check_no_time_errors(gc_event_dataframe):
    maximum_time = -1
    for time in gc_event_dataframe["TimeFromStart_seconds"]:
        if time < maximum_time:
            return False
        else:
            maximum_time = time
    return True

#       fix_timing_errors
#
#   Given a log file that has a timing error due to a crash,
#   replace all timing "from start" values after the crash with
#   the time they WOULD have been had there been no crash.
#
def fix_timing_errors(gc_event_dataframe):
    maximum_time = 0 
    add_maximum_time = 0

    # Loop through all data
    for index in range(len(gc_event_dataframe["TimeFromStart_seconds"])):
        time = gc_event_dataframe["TimeFromStart_seconds"][index]
        # If we reach a crash reset, keep the maximum time we had before
        
        if time + add_maximum_time < maximum_time:
            add_maximum_time = maximum_time
        

        # Every row keeps their inital value, added to the shift value from any timing errors
        gc_event_dataframe["TimeFromStart_seconds"][index] = time + add_maximum_time
        maximum_time = time + add_maximum_time
    
    
    return gc_event_dataframe
        
    




# Confirms the passed time range, which is either a maximum or a 
# range. Returns the minimum & maximum times, as a float.
def __get_time_range(time_range):
    if type(time_range) == int or type(time_range) == float:
        min_time = 0
        max_time = time_range
    else:
        #   assert len(time_range) == 2
        min_time = time_range[0]
        max_time = time_range[1]
    return min_time, max_time

#   Confirm that the parameter is numeric
def __number_to_float(number):
    if number != None:
        return float(number)
    return None


## # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#                         __manyMatch_LineSearch
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
def __manyMatch_LineSearch(
    match_term=None,  # regex terms to search for
    filepath=None,
):  # TRUE if data in a file
    num_match_groups = re.compile(match_term).groups
    table = [[] for i in range(num_match_groups)]
    # If there has been listed groups of interest within the regex search
    file = open(filepath, "r")
    for line in file:
        # Apply the regex search term to every line. 
        match = re.search(match_term, line)
        if match:
            # Find all matches of interest
            for i in range(0, num_match_groups):
                table[i].append(match.group(i + 1))  # +1 because group(0) is the whole string
            # add the match group number hit, so able to tell what match
    file.close()
    return table



# Access the column names for a parsed file. Note that these are dependent
# on the groups defined in event_string_parsing
# Full descriptions of the columns can be found in the README under /src/
def columnNames():
    return [
        "DateTime",
        "TimeFromStart_seconds",
        "EventType",
        "EventName",
        "AdditionalEventInfo",
        "HeapBeforeGC",
        "HeapAfterGC",
        "Duration_miliseconds",
        "SafepointName",
        "TimeFromLastSafepoint_ns",
        "TimeToReachSafepoint_ns",
        "AtSafepoint_ns",
        "TotalTimeAtSafepoint_ns",
        "TotalApplicationThreadPauseTime_seconds",
        "TimeToStopApplication_seconds"
    ]