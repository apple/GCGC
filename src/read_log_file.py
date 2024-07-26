#       read_log_file.py
#
#   Given a log file, parse through that file and return a gc_events_dataframe containing all
#   relevant information from the log during runtime

from src.parse_log_file import get_parsing_groups
import pandas as pd
import numpy as np
import re
import glob
import matplotlib


#       get_file_names_wildcard
#
#   Given a path including a linux style wildcard search, return the list of all matching files
#   on that path. Each file is a string.
#
def get_file_names_wildcard(path):
    files = []
    filelist = glob.glob(path)
    if not filelist:
        print("Warning: No files collected using following path: " + str(path))
        return []
    else:
        for file in filelist:
            files.append(file)
    return files


#       get_gc_event_tables
#
#   Take a list of list of log file paths/names, and construct a list of tables, one for
#   each log in the list. Creates correct TimeFromStart_seconds time column for data, scaling
#   based on unit present in log file
#
def get_gc_event_tables(files, zero_times=True, ignore_crashes = False):
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
            gc_event_dataframe = get_parsed_data_from_file(file, ignore_crashes)
            gc_event_dataframe = scale_time(gc_event_dataframe)
            gc_event_dataframe = scale_heap_percent_full(gc_event_dataframe)
            gc_event_dataframe = generate_new_column_with_values_in_mb(
                gc_event_dataframe,
                "UsedMetaspaceAfterGCWithUnit",
                "UsedMetaspaceAfterGC",
                True
            )
            gc_event_dataframe = generate_columns_for_percent_used_and_max_used_in_each_code_heap(gc_event_dataframe)

            if not gc_event_dataframe.empty:
                gc_event_dataframes.append(gc_event_dataframe)
            else:
                print("No information collected for file: ", file)
        if gc_event_dataframes:
            df = pd.concat(gc_event_dataframes)
            if zero_times:
                zero_start_times(df)

            # Clean data
            df.replace({np.nan: None}, inplace=True)

            all_runs.append(df)
    if not all_runs:
        print("Error: No data collected in get_gc_event_tables.")
    return all_runs


#       takes the units from the dataframe, and recorded times,
#       and creates timestamps in seconds. Scales units appropriately
#
def scale_time(df):
    if df.empty: 
        return df
    time_seconds = []
    if "Time" in df and "TimeUnit" in df:
        unit = df["TimeUnit"].iloc[0]
        if unit == "s":
            divisor = 1
        elif unit == "ms":
            divisor = 1000
        elif unit == "ns": 
            divisor = 1000000000
        elif not unit: # date time            
            times = pd.Series(matplotlib.dates.date2num(df["DateTime"]))
            time_seconds = [time * 86400 for time in times]  # scales matplotlib datetime to seconds.
            df["TimeFromStart_seconds"] = time_seconds
            df = df.drop(columns=["Time", "TimeUnit"], axis = 1)
            return df
        else:
            print("Unknown unit detected: unit = ", unit)
            return df
        for row in df["Time"]:
            time_seconds.append(row / divisor)
    
    df["TimeFromStart_seconds"] = time_seconds
    df = df.drop(columns=["Time", "TimeUnit"], axis = 1)
    return df

# Create a column "HeapPercentFull", and populate it with data if not already populated
def scale_heap_percent_full(df):
    if df.empty:
        return df
    
    # First, check if its already populated with values.
    if "HeapPercentFull" in df:
        for row in df["HeapPercentFull"]:
            if row:
                return df

    if "MaxHeapsize" in df and "HeapAfterGC" in df:
        max_heapsize = df["MaxHeapsize"]
        after_gc = df["HeapAfterGC"]
        heap_percent_full = []

        for occupancy, maxsize in zip(after_gc, max_heapsize):
            percent = None
            # Will be appended as is if not reassigned, to preserve the indices of the percentages in the column

            if occupancy != None and maxsize != None:
                if maxsize > 0:
                    percent = 100 * occupancy / maxsize
                else:
                    percent = 0

            heap_percent_full.append(percent)
        df["HeapPercentFull"] = heap_percent_full
    return df


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




## # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#                               get_parsed_data_from_file
#
# Purpose:
#   Given a filepath to a log file, create a pandas dataframe holding all information
#   for that log file. Each row is a different event.
#
# Parameters:
#   logfile -> a string with the path to the log file to read.
#   time_range_seconds -> The time range to parse. Either a range, or just a max.
#   ignore_crashes -> If true, crashes are ignored, and the program consideres the runtime to be continuous.
#
# Return:
#   a pandas dataframe, where rows are each an individual event. Columns are labeled, and
#   collect information on each event, such as when it occured, how long it lasted, and the name
## # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def get_parsed_data_from_file(logfile, ignore_crashes = False):
    regex_capture_string, column_names, data_types = get_parsing_groups()
       
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
    for column in table_groups:  
        table_groups[column] = __create_column(table, # data
                                               table_groups[column][1],  # DATATYPES
                                               table_groups[column][0])  # table indicies

    ### Special Case ###
    # Updates the eventtype column to properly put "Safepoint" at the eventtype, rather than None
    table_groups["EventType"] = set_safepoints_eventype(
                                table_groups["EventType"], 
                                table_groups["SafepointName"], 
                                table_groups["TimeToStopApplication_seconds"])
    df = pd.DataFrame(table_groups)
    
    ## Apply resrictions as needed **
    if ignore_crashes:
        if not assert_no_timing_errors(df):
            df = fix_timing_errors(df)


    return df


#   Given the table of information, the specified datatype, and all columns
#   associated with a particular column, return the 
#
#
def __create_column(table, data_types, table_columns):
    if len(table_columns) == 1:
        datavalues = []
        for idx in range(len(table[table_columns[0]])):
            if table[table_columns[0]][idx] != None:
                datavalues.append(data_types[0](table[table_columns[0]][idx]))
            else:
                datavalues.append(None)
        return datavalues
    else:
        new_column = []
        for row in range(len(table[table_columns[0]])):
            found = False
            for i, colval in enumerate(table_columns):
                if table[colval][row] != None:
                    new_column.append(data_types[i](table[colval][row]))
                    found = True
                    break
            if not found:
                new_column.append(None)
        return new_column

#       assert_no_timing_errors
#
#   Looks through all rows of a gc_event_dataframe timing, and confirms
#   that there are no timing errors, meaning the time line never decreases.
#   For all lines x, time(x) <= time(x + n), n > 0. Otherwise, return false.
#
#    returns TRUE if no timing errors
def assert_no_timing_errors(gc_event_dataframe):
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

def zero_start_times(dataframe):
    min_time = dataframe["TimeFromStart_seconds"].min()
    new_times = []
    for time in dataframe["TimeFromStart_seconds"]:
        new_times.append(time - min_time)
    dataframe["TimeFromStart_seconds"] = new_times
    # No return needed, as the originals have been updated.


#       generate_new_column_with_values_in_mb
#
# - Adds a new column `new_column_name` to the dataframe, generated from another column
#   `base_column_name`. The values of the fields of the new column are the same as that of the base column
#   but having all sizes unified to MB.
# - Drops the base column if `drop_base_column` is set to `True`.
#
#   returns `gc_event_dataframe`
def generate_new_column_with_values_in_mb(
        gc_event_dataframe,
        base_column_name,
        new_column_name,
        drop_base_column
):
    sizes_in_mb = []

    for size in gc_event_dataframe[base_column_name]:
        if size is None:
            sizes_in_mb.append(None)  # Keep track of `None` values to preserve indices of sizes in the column
        else:
            size_without_unit = float(size[:-1])
            unit = size[len(size) - 1]

            if unit == 'K':
                size_without_unit /= 1024  # Convert KB to MB
            elif unit == 'G':
                size_without_unit *= 1024  # Convert GB to MB
            elif unit != 'M':
                size_without_unit = None  # Already `None` but just to be explicit
                print("Unknown unit detected when converting to MB: unit = ", unit)

            sizes_in_mb.append(size_without_unit)

    gc_event_dataframe[new_column_name] = sizes_in_mb

    if drop_base_column is True:
        gc_event_dataframe.drop(columns=[base_column_name])

    return gc_event_dataframe


#       generate_columns_for_percent_used_and_max_used_in_each_code_heap
#
# Adds six new columns (two columns for each code heap) to the dataframe, having values for the percentage used and
# max-used in each code heap
#
#   returns `gc_event_dataframe`
def generate_columns_for_percent_used_and_max_used_in_each_code_heap(gc_event_dataframe):
    non_profiled_nmethods_code_heap_percent_used = []
    profiled_nmethods_code_heap_percent_used = []
    non_nmethods_code_heap_percent_used = []

    non_profiled_nmethods_code_heap_percent_max_used = []
    profiled_nmethods_code_heap_percent_max_used = []
    non_nmethods_code_heap_percent_max_used = []

    for code_heap, size, used, max_used in zip(
        gc_event_dataframe["CodeHeap"],
        gc_event_dataframe["CodeHeapSize"],
        gc_event_dataframe["CodeHeapUsed"],
        gc_event_dataframe["CodeHeapMaxUsed"]
    ):
        # Append `None` to all. The `None` value in the list for the detected code heap will be replaced with the
        # computed percentage. And will be left as is (`None`) in the other lists to preserve the indices of the
        # percentages in their respective columns
        non_profiled_nmethods_code_heap_percent_used.append(None)
        profiled_nmethods_code_heap_percent_used.append(None)
        non_nmethods_code_heap_percent_used.append(None)

        non_profiled_nmethods_code_heap_percent_max_used.append(None)
        profiled_nmethods_code_heap_percent_max_used.append(None)
        non_nmethods_code_heap_percent_max_used.append(None)

        reference_to_list_for_detected_code_heap_used = None
        reference_to_list_for_detected_code_heap_max_used = None
        # Will reference the necessary lists, base on the detected code heap

        if code_heap is not None:
            if size > 0:
                used_percent = 100 * used / size
                max_used_percent = 100 * max_used / size
            else:
                used_percent = 0
                max_used_percent = 0

            # Set the reference to the necessary list
            if code_heap == 'non-profiled nmethods':
                reference_to_list_for_detected_code_heap_used = non_profiled_nmethods_code_heap_percent_used
                reference_to_list_for_detected_code_heap_max_used = non_profiled_nmethods_code_heap_percent_max_used
            elif code_heap == 'profiled nmethods':
                reference_to_list_for_detected_code_heap_used = profiled_nmethods_code_heap_percent_used
                reference_to_list_for_detected_code_heap_max_used = profiled_nmethods_code_heap_percent_max_used
            elif code_heap == 'non-nmethods':
                reference_to_list_for_detected_code_heap_used = non_nmethods_code_heap_percent_used
                reference_to_list_for_detected_code_heap_max_used = non_nmethods_code_heap_percent_max_used

            # Replace the appended `None` value with the computed percentage
            reference_to_list_for_detected_code_heap_used.pop()
            reference_to_list_for_detected_code_heap_used.append(used_percent)

            reference_to_list_for_detected_code_heap_max_used.pop()
            reference_to_list_for_detected_code_heap_max_used.append(max_used_percent)

            # The other lists retain their appended `None` values.

    gc_event_dataframe["NonProfiledNMethodsCodeHeapPercentUsed"] = non_profiled_nmethods_code_heap_percent_used
    gc_event_dataframe["ProfiledNMethodsCodeHeapPercentUsed"] = profiled_nmethods_code_heap_percent_used
    gc_event_dataframe["NonNMethodsCodeHeapPercentUsed"] = non_nmethods_code_heap_percent_used

    gc_event_dataframe["NonProfiledNMethodsCodeHeapPercentMaxUsed"] = non_profiled_nmethods_code_heap_percent_max_used
    gc_event_dataframe["ProfiledNMethodsCodeHeapPercentMaxUsed"] = profiled_nmethods_code_heap_percent_max_used
    gc_event_dataframe["NonNMethodsCodeHeapPercentMaxUsed"] = non_nmethods_code_heap_percent_max_used

    return gc_event_dataframe
