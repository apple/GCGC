# /src
Contains the folder of notebooks for log analysis.
Other files define helper functions for this log analysis.

# Project Design : GCGC

1. [Purpose](#purpose)
2. [How to interact with the project](#how-to-interact-with-the-project)
3. [Implementation](#implementation)

> ## Purpose

The purpose of this project is to provide an easy, and modifyable tool for analyzing Java garbage collection logs. 


> ## How to interact with the project
- If you would like to compare any number of logs against each other, then running this tool would work for you. Navigate to [/src/notebooks](/src/notebooks) and run the `GCGC.ipynb` file.

- If you would like to expand off of this tool to create more analysis, or compare the GC data against other program-related events, then creating a copy of the analysis notebook is required: [/src/notebooks](/src/notebooks). 

> ## Implementation

A notebook kernel holds all state information about the program. Upon executing the cell to read the logs, some number of log files is read line by line. Each line is parsed for information according to a regular expression defined in [parse_log_file.py](parse_log_file.py). Then, a `gc_event_dataframe` is created for each log file, holding in state memory the information associated with each gc log run.

Each `gc_event_dataframe` is a [pandas](https://pandas.pydata.org) dataframe.
The columns used during the program, that MUST be present in the data set are:

    - TimeFromStart_seconds
    - Duration_miliseconds

Without these two columns, the notebook will fail to automatically either X or Y information. 

The columns, patterns for them, and the actual regex capture groups are defined in [./read_log_file.py](read_log_file.py).
1. `TimeFromStart_seconds` : Time since program begins. Used for all plots x-axis values. Make sure to enable this metric when creating a log file.

2. `Duration_miliseconds` : Time duration of the event in that row. If missing, most analysis fails, or must have another column value manually selected. 

The program holds a list of these gc_event_dataframes in state, which is then never modified again. The log files will not be read again.

To run analysis on the data, a user specifies a printing function, and a grouping & filter.
a grouping will group all matching values for a column into one place. A filter selects rows from the dataframe, based on conditions. Then, the remaining data is processed and plotted.

(TODO)