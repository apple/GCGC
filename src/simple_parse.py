# The purpose of this is to RE-implement the regex parsing and searching and transormation functions to clearlyt allow for simple improvements

import re
import pandas as pd
import glob
import numpy as np

# TODO: Handle conflicts on column naming scheme!!!! 

def parse_filelist(filelist):
    # Given a file list, parse all files passed into gc event dataframes, then combine them.
    combined_dataframes = []
    for file in filelist:
        dataframe = create_event_log(file)
        ## Clean data, apply resrictions as needed **
        dataframe.replace({np.nan: None}, inplace= True)   
        combined_dataframes.append(dataframe)
    return pd.concat(combined_dataframes)
    
############################################################
#       get_eventlogs 
#
#   Creates a list of gc event logs, parsing all files passed.
#           
#   Parameters: filelists: a list of strings, each being a unix style filepath
#               to a file or set of files to be parsed. The * wildcard can be used
#               to specify a grouping of files belonging to the same log run.
def get_eventlogs(filelists):
    # each entry in filelists is a list of filenames representing one log run
    combined_eventlogs = []
    for filelist in filelists:
        filenames = get_file_names_wildcard(filelist)
        if filenames: # Make sure we found the files
            df = parse_filelist(filenames)
            combined_eventlogs.append(df)

    return combined_eventlogs




############################################################
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


def create_event_log(file):
    # First, obtain the log lines you would like to target
    # Then, parse the log file for those lines
    # Create a set of pd.DataFrames to hold these parsed log lines
    # Combine those dataframes into a complete event log.
    regex_capture_strings, column_names_lists, datatypes = get_regex_capture_strings()
    matches_database = parse_log(regex_capture_strings, column_names_lists, datatypes, file)    
    combined_event_log = pd.DataFrame()
    
    
    for index in range(len(matches_database)):
        df = pd.DataFrame(matches_database[index])
        
        combined_event_log = pd.concat([combined_event_log, df], axis=1)

    return combined_event_log

###########################################################################################
#       parse_log
#
#   Takes a log file, and parses it for matches in a list of regex capture groups
#
#   Parameters:
#       regex_capture_strings: list of regex strings that look to parse the log file
#       column_names_lists   : list of lists of column names for regex_capture_strings. All MUST be uniuqe.
#       datatypes_list       : list of datatypes for each column.
#       file                 : path to file to be parsed
#   
#   Returns: list of dictionaries, representing event logs for each regex capture string.
#   
def parse_log(regex_capture_strings, column_names_lists, datatypes_lists, file):
    # Regex_capture_strings are a list of regex style strings that target specific lines in the gc log
    # For each capture string, we create a dictionary table, wi with rows/columns associated with lines/capture groups
    # Return a list of these tables.
    # It is required for len(column_names_list) = len(datatypes_lists)

    
    # First, clean the input column names and datatypes for 'None' Values.
    for index in range(len(column_names_lists)):
        # Loop through each list in the passed lists, and remove None values
        column_names_lists[index] = [col for col in column_names_lists[index] if col]
        datatypes_lists[index] = [datatype for datatype in  datatypes_lists[index] if datatype]
    matches_database = [] # holds all match lists (Defined below)
    for string, columns, datatypes in zip(regex_capture_strings, column_names_lists, datatypes_lists):
        matches = {}
        for column_name in columns:
            matches[column_name] = []
        for line in open(file, "r"):
            match = re.match(string, line)
            if match:
                
                for idx in range(len(columns)):
                    if match.group(idx + 1):
                        # print(datatypes[idx])
                        # print(columns[idx])
                        # print([match.group(idx+1)])
                        matches[columns[idx]].append(datatypes[idx](match.group(idx + 1)))
                    else:
                        # print(datatypes[idx])
                        # print(columns[idx])
                        # print([match.group(idx+1)])
                        matches[columns[idx]].append((match.group(idx + 1)))
        matches_database.append(matches)
    
    return matches_database



def get_regex_capture_strings():
    # Defines a regex string to parse. Each group should have a tuple : (regex, column name, data type)
    from src.file import get_format
    al , bl, cl = [], [], []
    a, b, c = get_format()
    al.append(a)
    bl.append(b)
    cl.append(c)
    al.append(a)
    bl.append(b)
    cl.append(c)
    
    return al,bl,cl
    