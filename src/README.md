# /src
Contains the folder of notebooks for log analysis.
Other files define helper functions for this log analysis.

# Project Design

1. [Purpose](#purpose)
2. [How to interact with the project](#how-to-interact-with-the-project)
3. [Implementation](#implementation)

> ## Purpose

The purpose of this project is to provide an easy, and modifyable tool for analyzing Java garbage collection logs. 


> ## How to interact with the project
- If you would like to compare any number of logs against each other, then running this tool would work for you. Navigate to [/src/notebooks](/src/notebooks) and run the `analyze_logs_simple.ipynb` file.

- If you would like to expand off of this tool to create more analysis, or compare the GC data against other program-related events, then creating a copy of the analysis notebook is required: [/src/notebooks](/src/notebooks). You are encouraged to use the [tutorials](../tutorials/) to familarize yourself with the Notebook soruce code. Use `analyze_logs_dev.ipynb` as a model, which has more documentation to what & how analysis is being run.

> ## Implementation

A notebook kernel holds all state information about the program. Upon executing the cell to read the logs, some number of log files is read line by line. Each line is parsed for information according to a regular expression defined in [read_log_file.py](read_log_file.py). Then, a `gc_event_dataframe` is created for each log file, holding in state memory the information associated with each gc log run.

Each `gc_event_dataframe` is a [pandas](https://pandas.pydata.org) dataframe, containing the following columns.
> DateTime, TimeFromStart_seconds , EventType , EventName , AdditionalEventInfo , HeapBeforeGC , HeapAfterGC , Duration_miliseconds
The columns used during the program, that MUST be present in the data set are:
    - TimeFromStart_seconds
    - Duration_miliseconds

Without these two columns, the notebook will faill to gather either X or Y information. An update in the near futurue will allow for overriding of these columns, but currently they are necessary.

The columns, patterns for them, and the actual regex capture groups are defined in [./read_log_file.py](read_log_file.py).
1. `DateTime` : Collected real world Clock Date & Time. Currently unusued in analysis, but collected for manual checking
2. `TimeFromStart_seconds` : Time since program begins. Used for all plots x-axis values. Make sure to enable this metric when creating a log file.
3. `EventType` : Describes a row (event) in the gc_event_dataframe. Any value is acceptable, used by a user to search/filter.
4. `EventName` : Describes percisely the event in the gc_event_dataframe. Any value is acceptable, used by a user to search/filter.
5. `AdditionalEventInfo` : Additional information collected automatically on an invent. Currently unusued in any cases, may be used for a specific search.
6. `HeapBeforeGC` : MB count of the heap size used before the gc run. Often left as 'None' if no value present.
7. `HeapAfterGC` : MB count of the heap size used after the gc run. Often left as 'None' if no value present.
8. `Duration_miliseconds` : Time duration of the event in that row. If missing, most analysis fails, or must have another column value manually selected. 

The program holds a list of these gc_event_dataframes in state, which is then never modified again. The log files will not be read again.

To do analysis on the data, a user specifies a printing function, and a grouping & filter.
a grouping will group all matching values for a column into one place. A filter selects rows from the dataframe, based on conditions. Then, the remaining data is processed and plotted.

The runtime for all operations are linear at best, with the exception of the logrithmic heatmap functions, whose runtime is O(nlogn). The plotting functions are not analyzed or optimized for runtime, but do not provide significant enough overhead to currently be the bottleneck. The space used during the program is typically `2n`, where `n` is all data in all log files. This is because a copy of the data is created when filters are applied to select the collect rows. However, because the lines are parsed from the logfile, the `n` data is typically much smaller than the size of the provided log file.

Next steps for the project include easier use for analysis, more summaries of data created for analysis, easier input of external data for analysis, and gc specific metrics, such as heap region allocation in g1.