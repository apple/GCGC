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
The only gc logging requirement is that the file contains the following information for each event: A section in the log line denoting the time from start in seconds, with the following regex format:
 >/[/d+/./d+s/]

This can be found here in a typical log file entry, possibly after a DateTime line of information.:

>`[1.879s]`[info][gc          ] GC(0) Pause Young (Allocation Failure) 2048M->131M(7851M) 42.134ms

> [2021-08-08T01:57:35.185-0700]`[269118.401s]`[info][gc,start      ] GC(46957) Pause Young (Mixed) (G1 Evacuation Pause)



However, all of the following fields are captured for each event. If a field has 'None' for a particular row in the event table, then no information for that event field was recorded. This is correct, because not all events have the same fields.
```
1 : DateTime                    | string
2 : TimeFromStart_seconds       | float
3 : GGIndex                     | float
4 : EventType                   | string
5 : EventName                   | string
6 : AdditionalEventInfo         | string
7 : HeapBeforeGC                | float
8 : HeapAfterGC                 | float
9 : MaxHeapsize                 | float
10: Duration_miliseconds        | float
11: HeapBeforeGC   (zgc)        | float
12: HeapAfterGC    (zgc)        | float
13: MaxHeapsize    (zgc)        | float
14: SafepointName               | string
15: TimeFromLastSafepoint_ns    | float
16: TimeToReachSafepoint_ns     | float
17: AtSafepoint_ns              | float
18: TotalTimeAtSafepoint_ns     | float
19: TotalApplicationThreadPauseTime_seconds | float
20: TimeStopApplication_seconds | float
```


The program holds a list of these gc_event_dataframes in state, which is then never modified again. The log files will not be read again.

To run analysis on the data, a user runs a cell with a printing function, which takes a grouping & filter as parameters.
A grouping will group all matching values for a column into one place. A filter selects rows from the dataframe, based on conditions. Then, the remaining data is processed and plotted. The resulting plot is returned, so easy labeling can be set for axis and titles. The axis of the plot are automatically adjusted (with the exception of the heatmaps) to fit the plotted data. 

Further manipulation of the data before or after plotting is possible, by using notebook cells. Each cell currently provided in the notebook comes with a link to the documentation of that cell.
