# Project Design : GCGC

1. [Design choices](#design-choices)
2. [Implementation](#implementation)

---

## Design choices

This project is built using Jupyter notebooks with a python3 kernel, rather than as a standalone tool with a graphical interface. Therefore, after collecting the GC log information and storing it into the state variable called `gc_event_dataframes`, it becomes possible for manual manipulation of the data. This was chosen for the project to allow for importing and exporting filtered data easily using well known packages in Python. The data structure used to hold the gc_event_dataframes is a [pandas](https://pandas.pydata.org) dataframe. The filters and groups while plotting provide fast ways to view subsets of the data, and further manipulation is possible due to the Notebook's interactive cell structure. All plots are created using the matplotlib package, which integrates well with inline plotting in Jupyter notebooks.

---

## Implementation

A notebook kernel holds all state information about the program. Upon executing the cell to read the logs, some number of log files are read line by line. Each line is parsed for information according to a regular expression defined in [parse_log_file.py](parse_log_file.py). This regular expression captures the key gc informations output by collectors in JDK11 & JDK16. Then, a `gc_event_dataframe` is created for each log file, holding in state memory the information associated with each gc log run. The creation of these dataframes is defined in `read_log_file.py`. 

Each `gc_event_dataframe` is a [pandas](https://pandas.pydata.org) dataframe.
All gc log files should be capable of being parsed and analyzed. If any gc log file failed to be parsed, open an issue on the topic. Not all log file lines are captured. Also, not all fields for described events are captured in each line. If a field has 'None' for a particular row in the event table, then no information for that event field was recorded. This is correct, because not all events have the same fields.
```
1 : DateTime                    | string
2 : Time                        | float
3 : TimeUnit                    | str
4 : Other fields                | str
5 : GGIndex                     | float
6 : EventType                   | string
7 : EventName                   | string
8 : AdditionalEventInfo         | string
9 : HeapBeforeGC                | float
10 : HeapAfterGC                 | float
11 : MaxHeapsize                 | float
12: Duration_milliseconds        | float
13: HeapBeforeGC   (zgc)        | float
14: HeapAfterGC    (zgc)        | float
15: MaxHeapsize    (zgc)        | float
16: SafepointName               | string
17: TimeFromLastSafepoint_ns    | float
18: TimeToReachSafepoint_ns     | float
19: AtSafepoint_ns              | float
20: TotalTimeAtSafepoint_ns     | float
21: TotalApplicationThreadPauseTime_seconds | float
22: TimeStopApplication_seconds | float
```
Afterwards, the following field will be calculated from "TimeUnit" and "Time" or "DateTime".
```TimeFromStart_seconds```



The program holds a list of these gc_event_dataframes in state, which is then never modified again. The log files will not be read again.

To run analysis on the data, a user runs a cell with a printing function, which takes a grouping & filter as parameters.
A grouping will group all matching values for a column into one place. A filter selects rows from the dataframe, based on conditions. Then, the remaining data is processed and plotted. The resulting plot is returned, so easy labeling can be set for axis and titles. The axis of the plot are automatically adjusted (with the exception of the heatmaps) to fit the plotted data. 

Further manipulation of the data before or after plotting is possible, by using notebook cells. Each cell currently provided in the notebook comes with a link to the documentation of that cell.
