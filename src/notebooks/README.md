# Notebooks



The notebook GCGC.ipynb is a complete analysis notebook, and only requires a user to edit the first cell.  Locally create a copy of this file to do any work, and use the original as a reference. 

Known edge cases documented at the end of this file.


## Important: 
If you do not know how to start a jupyter notebooks server/kernel required for a notebook, follow the setup instructions in [setup.md](../../setup.md)

# GC Analysis provided
The following are a list of automatically generated graphs/tables that are created after filling in the first cell with GC information. Afterwards, a detailed tuning section for each graph can be found. After generating a graph, feel free to change the parameters and labels, and re-run.

> #### 1a. STW Pauses during program runtime, Linear
> #### 1b. STW Pauses during program runtime, Logarithmic

> #### 2a. STW Pauses during program runtime, group by EventName, Linear
> #### 2b. STW Pauses during program runtime, group by AdditionalEventInfo, Logarithmic

> #### 3. Concurrent durations during runtime

> #### 4. Total time spent in STW pauses vs. Concurrent durations

> #### 5a. Pauses trends (max, sum, mean, count, std.dev)
> #### 5b. Pauses trends by name

> #### 6a. Pause percentiles
> #### 6b. Pause percentiles by name

> #### 7a. Mean event durations
> #### 7b. Sum event durations

> #### 8a. Heap Before GC 
> #### 8b. Heap After GC

> #### 9. MB Reclaimed during program runtime

> #### 10. Latency Heatmaps, Linear

> #### 11. Pause frequencies histogram

> #### 12. Latency percentiles over time intervals

> #### 13. Number of times GC invoked over time intervals

> #### 14. Sum of pause durations over intervals

> #### 15. Logarithmic heatmaps.* known bug where start time is always 0

> #### 16. Percentage of heap filled after GC

> #### 17. Heap allocation rate 

> #### 18. Example importing external data
--- 

## Configurations for plots
The following parameters can be found in some of the plotting functions. The list of the parameters for each function can be found below.
- `gc_event_dataframes` a list of pandas dataframes (gc event logs) containing information to be plotted
- `filter_by` You can adjust the filter by using `filter_by` = `function`, where the function takes in a row of a pandas dataframe (gc event log), and returns True or False based on the row's content.
 A typical filter_by function first checks if the column of interest is in the row, then checks if that column is populated with the correct value.
 - `group_by`- a string column name to create groups for each unique value found in that column. Those groups are given their own names and plot. Typical values include None (group by log), "EventName" (group by type of event), and "AdditionalEventInfo" (group by specific event categories).
 - `labels` - a list of strings that describe the list of log files passed in as the `gc_event_dataframes` parameter.
 - `colors` - a list of matplotlib colors, where len(colors) >= len(gc_event_dataframes). If left as None, a set of colors from a deterministic sequence will be plotted.
 - `column` the column in all `gc_event_dataframes` to search for datapoints to plot. Plots data on the Y axis.
 - `column_timing` the list of float or integer data representing the timestamps of the `column` parameter. Note: The expected unit for this column is seconds, and any deviation from this may have unexpected behavior. [ There is a known bug where using "DateTime" information collected from a gc log will cause any function relying on `intervals` of time to fail. This issue is going to be fixed. ]
 - `plot` - a `Matplotlib.axes._subplots.AxesSubplot` object, which is returned from all graphing based functions. Using this as a parameter for a function in the same cell will plot the resulting information onto the same plot. 

---
## Special Parameters

 Some of the functions will also have the following, more specific parameters:

- `interval_duration` - a float or integer timing in seconds to describe the size of groups of data collected from the log file.
- `line_graph` - a boolean. If True, the plot will be in the form of a line graph. If False, then a scatter plot. Default = False
---
To set a plot to logarithimic, use the returned object, and call the function set_yscale('log') on it. Then, use plot.yaxis.set_major_formatter(ScalarFormatter()) to nicely format the  Example:

`plot = plot_scatter(gc_event_dataframes labels=labels)`

`plot.set_yscale('log')`

`plot.yaxis.set_major_formatter(ScalarFormatter())`

--- 
Note: all functions are defined [src.graphing.plotting](../graphing/plotting.py) unless mentioned otherwise.

List of graphs, their associated plotting function, and parameters.
> #### 1a. STW Pauses during program runtime, Linear
 ### plot_scatter()

- gc_event_dataframes
- group_by
- filter_by = pauses_only
- labels
- colors
- plot
- column
- column_timing

> #### 1b. STW Pauses during program runtime, Logarithmic
### plot_scatter()
- gc_event_dataframes
- group_by
- filter_by = pauses_only
- labels
- colors
- plot
- column
- column_timing

set yscale to log manually

--- 

> #### 2a. STW Pauses during program runtime, group by EventName, Linear
### plot_scatter() 
- gc_event_dataframes
- group_by = "EventName"
- filter_by = pauses_only
- labels
- colors
- plot
- column
- column_timing


> #### 2b. STW Pauses during program runtime, group by AdditionalEventInfo, Logarithmic
### plot_scatter()
- gc_event_dataframes
- group_by = "AdditionalEventInfo"
- filter_by = pauses_only
- labels
- colors
- plot
- column
- column_timing


set yscale to log manually

--- 

> #### 3. Concurrent durations during runtime
- gc_event_dataframes
- group_by
- filter_by = concurrent_only
- labels
- colors
- plot
- column
- column_timing
--- 
> #### 4. Total time spent in STW pauses vs. Concurrent durations
### plot_bar_sum()
- gc_event_dataframes
- group_by = "EventType"
- filter_by
- labels
- colors
- plot
- column
- column_timing

--- 
> #### 5a. Pauses trends (max, sum, mean, count, std.dev)
### plot_trends()
- gc_event_dataframes
- group_by
- filter_by
- labels
- colors
- column
- throughput : If True, then a throughput is calculated from the timestamps provided, and the sum of the event durations for each group/log file.
> #### 5b. Pauses trends by name
### plot_trends()
- gc_event_dataframes
- group_by = "EventName"
- filter_by = pauses_only
- labels
- column
- throughput : If True, then a throughput is calculated from the timestamps provided, and the sum of the event durations for each group/log file.
--- 
> #### 6a. Pause percentiles
### plot_percentiles()
- gc_event_dataframes
- group_by
- filter_by = pauses_only 
- labels
- column

> #### 6b. Pause percentiles by name
### plot_percentiles()
- gc_event_dataframes
- group_by = "EventName"
- filter_by = pauses_only 
- labels
- column
--- 
> #### 7a. Average event durations
### plot_bar_avg()
- gc_event_dataframes,
- group_by = "EventType"
- filter_by
- labels
- colors
- plot
- column
- column_timing


> #### 7b. Sum event durations
### plot_bar_sum()
- gc_event_dataframes,
- group_by = "EventType"
- filter_by
- labels
- colors
- plot
- column
- column_timing

--- 
> #### 8a. Heap Before GC 
### plot_line()
- gc_event_dataframes
- group_by = "EventName"
- filter_by
- labels
- colors
- plot
- column
- column_timing
> #### 8b. Heap After GC
### plot_line()
- gc_event_dataframes
- group_by = "EventName"
- filter_by
- labels
- colors
- plot
- column
- column_timing

--- 
> #### 9. MB Reclaimed during program runtime
### plot_reclaimed_bytes()
Note: Relies on data being stored in columns named "HeapBeforeGC" and "HeapAfterGC".
- gc_event_dataframes
- group_by 
- filter_by = gc_values_present
- labels
- plot
- column_timing
- colors
---
> #### 10. Latency Heatmaps, Linear
### plot_heatmaps()
- gc_event_dataframes
- dimensions : a 4 length list, with the following values
    - dimensions[0] = number of x intervals
    - dimensions[1] = number of y intervals
    - dimensions[2] = duration of a single x interval
    - dimensions[3] = duration of a single y interval
- group_by 
- filter_by = pauses_only
- labels
- column
- column_timing
- frequency_ticks : If True, the heatmap prints the frequency as a number onto each cell. If False, it does not. Default = False.

---
> #### 11. Pause frequencies histogram
### plot_frequency_intervals() 
- gc_event_dataframes
- group_by 
- filter_by = pauses_only
- labels
- colors
- plot
- column
- interval_duration
- column_timing
---
> #### 12. Latency percentiles over time intervals
### plot_percentile_intervals()
- gc_event_dataframes
- group_by 
- filter_by = pauses_only
- labels
- colors
- plot
- column
- interval_duration
- percentiles : List of float or int values that represent the percentiles to be plotted on the chart. Prefered in decreasing order
- column_timing 
- line_graph
- different_colors : if True, each individual percentile line has its own color. If false, the percentiles for one log / group share the same color.

---
> #### 13. Number of times GC invoked over time intervals
### plot_frequency_of_gc_intervals()
- gc_event_dataframes
- group_by 
- filter_by = pauses_only
- labels
- colors
- plot
- column = "GCIndex"
- interval_duration
- column_timing
---
> #### 14. Sum of pause durations over intervals
### plot_sum_pause_intervals()
- gc_event_dataframes
- group_by 
- filter_by = pauses_only
- labels
- colors
- plot
- column
- interval_duration
- column_timing
- remove_empty_intervals : if True, then intervals where the sum of pauses = 0 will not be plotted. Default = False.
- line_graph 

---
> #### 15. Logarithmic heatmaps.* known bug where start time is always 0
### plot_heatmaps_logarithmic()
- gc_event_dataframes
- dimensions : list with 4 values:
    - dimensions[0] = number of x intervals
    - dimensions[1] = number of y intervals
    - dimensions[2] = duration of an x interval
    - dimensions[3] = base for logarithmic scaling.
- group_by
- filter_by = pauses_only
- labels
- column
- column_timing
- frequency_ticks : If True, the heatmap prints the frequency as a number onto each cell. If False, it does not. Default = False.

---
> #### 16. Percentage of heap filled after GC
### plot_percentages()
- gc_event_dataframes
- group_by
- filter_by = pauses_only
- labels
- colors
- plot
- column
- column_timing
- max_percentage_values : a list of the max heapsize in MB for each of the passed lists for gc_event_dataframes. (coming soon! Automatic detection of the max heapsize!)
- line_graph

---
> #### 17. Heap allocation rate 
### src.graphing.allocation_rate.allocation_rate()
- gc_event_dataframes
- group_by
- filter_by = diff_in_entries_filter
- labels
- interval_seconds
- colors
- plot
- column_before : the column in the gc_event_dataframe to find the heapsize before gc run
- column_after : the column in the gc_event_dataframe to find the heapsize after gc run
- percentile : if a percentile is provided, and an interval_seconds, then the passed percentile for allocation rate is plotted for each of the intervals.
- line_graph

--- 

### Known edge cases:

Note: The following edge cases are known and not handled automatically:

1) Shenandoah has two phases reporting Heap allocation: Does not imply twice the GC runs.
2) ZGC in JDK16 Puts information in safepoints, does not AUTOMATICALLY print these in log analysis as it currently stands. These safepoints have comparable metrics to pause times, but ZGC does not report them in the same fashion, so manual manipulation is needed.
3) ZGC bytes reclaimed calculation (This may extend to Shenandoah) may be negative, if the rate of allocation exceeds the rate of gc collection. Information is correctly provided in logs, not properly analyzed here.
4) Trying to plot a graph declared in another cell does not show up inline in Jupyter notebooks
5) Using column_timing = "DateTime" in any function that requires as an "interval_duration" breaks the tool's analysis features, since DateTime represents each day with about 0.25 float value percision, not the expected unit of seconds.
