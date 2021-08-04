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
            gc_event_dataframe = get_parsed_data_from_file_updated(file, time_range_seconds, ignore_crashes)
            
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
from src.parse_log_line import event_parsing_string as eps
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
    table[2] = list(map(__number_to_float, table[2]))
    table[1] = list(map(__number_to_float, table[1]))
    table[8] = list(map(__number_to_float, table[8]))
    table[6] = __choose_non_zero(table[6], table[10]) # Before GC collection mem_size
    table[7] = __choose_non_zero(table[7], table[11]) # After GC collection mem_size
    table[8] = __choose_non_zero(table[8], table[12]) # Max heapsize
    table[6] = list(map(__number_to_float, table[6])) 
    table[7] = list(map(__number_to_float, table[7]))
    table[8] = list(map(__number_to_float, table[8])) 
    table[9] = list(map(__number_to_float, table[9])) 
    # Schema 1 (JDK 16)
    temp = []
    table[3] = set_safepoints_eventype(table[3], table[12], table[18])
    
    # table [10]  safepoint_name
    table[12] = list(map(__number_to_float, table[13])) # time_since_last_safepoint
    table[13] = list(map(__number_to_float, table[14])) # reaching_safepoint_time
    table[14] = list(map(__number_to_float, table[15])) # at_safepoint_time
    table[15] = list(map(__number_to_float, table[16])) # total_time_safepoint
    table[16] = list(map(__number_to_float, table[17])) # total_application_thread_stopped_time_seconds
    table[17] = list(map(__number_to_float, table[18])) # total_time_to_stop_seconds

    table.pop(12) # Used due to 2 types of memory change regex groups & before/after for each
    table.pop(11) # Therefore, we gather before & after into 2 distinct columns, and remove other set
    table.pop(10) 

    parsed_data_table = pd.DataFrame(table).transpose() 
    # The data collected is in a 2d array, where table indicies represent a column. However,
    # a pandas dataframe expects each entry of the 2d array to be a row, not a column. Transpose
    # to fix this orientation error.
    parsed_data_table.columns = columnNames()  # add column titles, allow for clear references
    print(parsed_data_table)
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
# on the groups defined in `parse_log_file.py`
# Full descriptions of the columns can be found in the README under /src/
def columnNames():
    return [
        "DateTime",
        "TimeFromStart_seconds",
        "GCIndex",
        "EventType",
        "EventName",
        "AdditionalEventInfo",
        "HeapBeforeGC",
        "HeapAfterGC",
        "MaxHeapsize",
        "Duration_miliseconds",
        "SafepointName",
        "TimeFromLastSafepoint_ns",
        "TimeToReachSafepoint_ns",
        "AtSafepoint_ns",
        "TotalTimeAtSafepoint_ns",
        "TotalApplicationThreadPauseTime_seconds",
        "TimeToStopApplication_seconds"
    ]


#       __choose_non_zero
#
#   Given two lists, choose the value for each zipped index in the list
#   that is non zero, or None if neither have values, and return the combined 
#   list
#
def __choose_non_zero(list1, list2):
    list_non_zero = []
    for item1, item2 in zip(list1, list2):
        if item1:
            list_non_zero.append(item1)
        elif list2:
            list_non_zero.append(item2)
        else:
            list_non_zero.append(None)
    return list_non_zero

#       set_safepoints_eventtype
#
#   Given a list of two possible safepoint formats, and a list of eventtypes, compare
#   each log line to both safepoint formats. If either is populated, update the eventtype for that line
#   to be "Safepoint", rather than "None". Return the updated eventtype list.
#
def set_safepoints_eventype(eventtype_list, safepoint_list1, safepoint_list2):
    # Implementation Note: It is assumed that a row with safepoint information CANNOT have a collected EventType
    temp = []
    for eventtype, safepoint1, safepoint2 in zip(eventtype_list, safepoint_list1, safepoint_list2):
        if safepoint1 or safepoint2:
            temp.append("Safepoint")
        else:
            temp.append(eventtype)
    return temp

from src.temporary_parse_log_file import event_parsing_string_temp
def get_parsed_data_from_file_updated(logfile,  time_range_seconds, ignore_crashes = False):

    
    regex_capture_string, column_names, data_types = event_parsing_string_temp()    
    table = __manyMatch_LineSearch(regex_capture_string, logfile)
    
    # Construct a dictionary to hold column names, and associated data
    table_groups = {}

    
    group_number = 0
    for column, data_type in zip(column_names, data_types):
        if column:
            if column not in table_groups:
                # Create a new column, with the associated indicies of the data & datatype
                table_groups[column] = [group_number], [data_type]
            else:
                # Add to the column of associated indicies, and datatypes
                table_groups[column][0].append(group_number)
                table_groups[column][1].append(data_type)

            group_number += 1 # Not done in for loop, because if not column, then index doesnt changeß
    
    # For each unique column name, select from the table the non-zero values for the associated
    # column(s), and return a list in that correct data type. Then, update the dictionary's value
    # to be that updated list. If no value, 'None' lives in the row
    for column in table_groups:                                            # data_types             # columns indicies
        table_groups[column] = __create_column(table, table_groups[column][1], table_groups[column][0])

    ### Special Case ###
    # Updates the eventtype column to properly put "Safepoint" at the eventtype, rather than None
    table_groups["EventType"] = set_safepoints_eventype(
                                table_groups["EventType"], 
                                table_groups["SafepointName"], 
                                table_groups["TimeToStopApplication_seconds"])

    return pd.DataFrame(table_groups)


#   Given the table of information, the specified datatype, and all columns
#   associated with a particular column, return the 
#
#
def __create_column(table, data_types, table_columns):
    if len(table_columns) == 1:
        datavalues = []
        for idx in range(len(table[table_columns[0]])):
            if table[table_columns[0]][idx]:
                datavalues.append(data_types[0](table[table_columns[0]][idx]))
            else:
                datavalues.append(None)
        return datavalues
    else:
        new_column = []
        for row in range(len(table[table_columns[0]])):
            found = False
            for i, colval in enumerate(table_columns):
                if table[colval][row]:
                    new_column.append(data_types[i](table[colval][row]))
                    found = True
                    break
            if not found:
                new_column.append(None)
        return new_column
