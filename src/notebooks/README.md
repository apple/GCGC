# Notebook function documentation

List of functions and the plots they are expected to produce. For each of the provided GCGC original plots, the suggested parameters will be provided.

> #### [1. STW Pauses during program runtime ->](./README.md#1-stw-pauses-during-program-runtime)

> #### [2. STW Pauses during program runtime, group by EventName ->](./README.md#2-stw-pauses-during-program-runtime-group-by-eventname)

> #### [3. Latency Heatmaps, Linear ->](./README.md#3-latency-heatmaps-linear)


> #### [4. Logarithmic heatmaps ->](./README.md#4-logarithmic-heatmaps)


> #### [5. Latency percentiles over time intervals ->](./README.md#5-latency-percentiles-over-time-intervals)

> #### [6. Sum of pause durations over intervals ->](./README.md#6-sum-of-pause-durations-over-intervals)

> #### [7. Percentage of heap filled after GC ->](./README.md#7-percentage-of-heap-filled-after-gc)

> #### [8. Heap Before and After GC ->](./README.md#8-heap-before-and-after-gc)

> #### [9. MB Reclaimed during program runtime ->](./README.md#9-mb-reclaimed-during-program-runtime)

> #### [10. Heap allocation rate ->](./README.md#10-heap-allocation-rate)

> #### [11. Percentage Used in Each Code Heap ->](./README.md#11-percentage-used-in-each-code-heap)

> #### [12. Code Cache Flushing Rate ->](./README.md#12-code-cache-flushing-rate)

> #### [13. Used Metaspace After GC ->](./README.md#13-used-metaspace-after-gc)
  
> #### [14. Concurrent durations during runtime ->](./README.md#14-concurrent-durations-during-runtime)
  
> #### [15. Sum of event durations, grouped by EventType ->](./README.md#15-sum-of-event-durations-grouped-by-eventtype)
  
> #### [16. Pauses summary ->](./README.md#16-pauses-summary)
  
> #### [17. Pause percentiles ->](./README.md#17-pause-percentiles)
  
> #### [18. Mean and Sum of event durations ->](./README.md#18-mean-and-sum-of-event-durations)

> #### [19. Pause frequencies histogram ->](./README.md#19-pause-frequencies-histogram)

> #### [20. Number of times GC invoked over time intervals ->](./README.md#20-number-of-times-gc-invoked-over-time-intervals)

                                        
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

<br />

# List of generated plots, and expected parameters


## 1. STW Pauses during program runtime:

Uses the function `plot_scatter()`. This function is interchangeable with the function `plot_line()` if a line plot is desired, with the same parameters for both functions. The parameters are listed below for the functions, with the expected values to create the plot described by `1. STW pauses during program runtime` being described in paranthesis. The only required parameter is `gc_event_dataframes` 
    
    gc_event_dataframes (required)
    group_by            (Expected = None) 
    filter_by           (Expected = pauses_only)
    labels              (Expected = labels variable)
    colors              (Expected = None)
    plot                (Expected = None)
    column              (Expected = None)
    column_timing       (Expected = None)

Note: a `gc event log` is a pandas dataframe, containing labeled columns to describe fields in a recorded event, and each row representing a discerete event. A list of `gc event logs` are returned from the function `get_gc_event_tables()` in `read_log_file.py`, which is used to automatically parse log files. 

`plot_scatter()` / `plot_line()` parameters:

- **gc_event_dataframes**: `list` datatype. Each list entry is expected to be a `gc event log`. The `gc event logs` in the list will be parsed for the columns described by the parameters `column` and `column_timing` for Y and X data respectively, after filters have been applied.

- **group_by**: `str` datatype. Name of a column present in the `gc event logs`. If this parameter is provided, groups all repeated values from the specified column, such that every group has the same value in column '`group_by`'. Leaving this optional parameter as `None` defaults to creating 1 group per `gc event log` in the `gc_event_dataframes` list. Examples below

      group_by = "EventName"
      group_by = "EventType"

- **filter_by** : `function` datatype. A boolean function to be applied to each row of each `gc event log`. If the function evaluates to false, then that event will not be included in the resulting plot. A typical function first checks if the column exists before checking any values, as seen in the example below. If this check is not in place, a `KeyError` may be thrown.
        
      def pauses_only(row):
           if "EventType" in row:
               if row["EventType] == "Pause":
                   return True
       return False
        
       filter_by = pauses_only

- **labels** : `list` datatype. Each entry in the labels list describes the data in `gc_event_dataframes`, in order. Each entry in the labels list should be a `str` datatype. 

      labels = ["Monday log", "Tuesday Log", "Wednesday Log"]

- **colors** : `list` datatype. Each entry in the labels list picks a color for the output groups in the created plot, in order. If `None`, a set of discrete colors in the same order will be used. Each entry of this list is either a `str` describing one of the [matplotlib named colors](https://matplotlib.org/stable/gallery/color/named_colors.html), or is an (r, g, b) triplet with values between [0-1] representing brightness on a scaled (0-255) range.

      colors = ["black", "darkslateblue", (1, 0.5, 0)]

- **plot** : `matplotlib.axes._subplots.AxesSubplot` datatype. Each graphing function returns an instance of this plot object. Passing None creates a new figure. Passing an instance of a plot will keep all old data on the plot, and add the newly plotted data on top. Typically used to overlay two data sets with different column names.

      plot = plot_scatter(gc_event_dataframes)
      plot = plot_line(gc_event_dataframes, group_by = "EventNames")

- **column** : `str` datatype. The name of a column found in the list of `gc event logs`, representing the Y coordinate of data to plot. If `None` is passed, the default value for this parameter is `"Duration_milliseconds"`. 

      column = "Duration_milliseconds"

- **column_timing** :`str` datatype. The name of a column found in the list of `gc event logs`, representing the X coordinate of the data to plot. If `None` is passed, the default value for this parameter is `"TimeFromStart_seconds"`. 
      
      column_timing = "TimeFromStart_seconds"

---











## 2. STW Pauses during program runtime, group by EventName

Uses the function `plot_scatter()`. This function is interchangeable with the function `plot_line` if a line plot is desired, with the same parameters for both functions. The parameters are listed below for the functions, with the expected values to create the plot described by `2. STW Pauses during program runtime, group by EventName` being described in paranthesis. The only required parameter is `gc_event_dataframes`.
    
    gc_event_dataframes (required)
    group_by            (Expected = "EventName") 
    filter_by           (Expected = pauses_only)
    labels              (Expected = labels variable)
    colors              (Expected = None)
    plot                (Expected = None)
    column              (Expected = None)
    column_timing       (Expected = None)

Note: a `gc event log` is a pandas dataframe, containing labeled columns to describe fields in a recorded event, and each row representing a discerete event. A list of `gc event logs` are returned from the function `get_gc_event_tables()` in `read_log_file.py`, which is used to automatically parse log files. 

`plot_scatter()` / `plot_line()` parameters:

- **gc_event_dataframes**: `list` datatype. Each list entry is expected to be a `gc event log`. The `gc event logs` in the list will be parsed for the columns described by the parameters `column` and `column_timing` for Y and X data respectively, after filters have been applied.

- **group_by**: `str` datatype. Name of a column present in the `gc event logs`. If this parameter is provided, groups all repeated values from the specified column, such that every group has the same value in column '`group_by`'. Leaving this optional parameter as `None` defaults to creating 1 group per `gc event log` in the `gc_event_dataframes` list. Examples below

      group_by = "EventName"
      group_by = "EventType"

- **filter_by** : `function` datatype. A boolean function to be applied to each row of each `gc event log`. If the function evaluates to false, then that event will not be included in the resulting plot. A typical function first checks if the column exists before checking any values, as seen in the example below. If this check is not in place, a `KeyError` may be thrown.
        
      def pauses_only(row):
           if "EventType" in row:
               if row["EventType] == "Pause":
                   return True
       return False
        
       filter_by = pauses_only

- **labels** : `list` datatype. Each entry in the labels list describes the data in `gc_event_dataframes`, in order. Each entry in the labels list should be a `str` datatype. 

      labels = ["Monday log", "Tuesday Log", "Wednesday Log"]

- **colors** : `list` datatype. Each entry in the labels list picks a color for the output groups in the created plot, in order. If `None`, a set of discrete colors in the same order will be used. Each entry of this list is either a `str` describing one of the [matplotlib named colors](https://matplotlib.org/stable/gallery/color/named_colors.html), or is an (r, g, b) triplet with values between [0-1] representing brightness on a scaled (0-255) range.

      colors = ["black", "darkslateblue", (1, 0.5, 0)]

- **plot** : `matplotlib.axes._subplots.AxesSubplot` datatype. Each graphing function returns an instance of this plot object. Passing None creates a new figure. Passing an instance of a plot will keep all old data on the plot, and add the newly plotted data on top. Typically used to overlay two data sets with different column names.

      plot = plot_scatter(gc_event_dataframes)
      plot = plot_line(gc_event_dataframes, group_by = "EventNames")

- **column** : `str` datatype. The name of a column found in the list of `gc event logs`, representing the Y coordinate of data to plot. If `None` is passed, the default value for this parameter is `"Duration_milliseconds"`. 

      column = "Duration_milliseconds"

- **column_timing** :`str` datatype. The name of a column found in the list of `gc event logs`, representing the X coordinate of the data to plot. If `None` is passed, the default value for this parameter is `"TimeFromStart_seconds"`. 
      
      column_timing = "TimeFromStart_seconds"




The folloing modifier can be added after to create the logarithmic plot, as described in the commented out code block. 

    plot = plot_scatter(gc_event_dataframes,
                        group_by = "AdditionalEventInfo",
                        filter_by = pauses_only,
                        labels = labels)
    plot.set_yscale("log")
    plot.yaxis.set_major_formatter(ScalarFormatter()) # optional, known bug for displaying values less than 1 on y axis scale.

---




## 3. Latency Heatmaps, Linear

Uses the function `plot_heatmap()`. The parameters are listed below for the functions, with the expected values to create the plot described by `3. Latency Heatmaps, Linear` being described in paranthesis. There are TWO required parameters: both `gc_event_dataframes`, and `dimensions` are needed for this function. The warning from matplotlib is expected. 

Important: The latency and time information is the LOWER bound of the bucket (square) on the heatmap. If you see a frequency of 3 for time = 0s and the next time square is labeled time = 10s, latency = 5ms and the next square above on latency is 10ms, then there were 3 pause events between 0 and 10 seconds, with latency 5-10 seconds.
    
    gc_event_dataframes (required)
    dimensions (Expected = [ 20,  15, 60, 10 ]) 
                                    ### 20 x axis columns
                                    ### 15 y column rows
                                    ### 60 seconds == 1 minute intervals
                                    ### 10 milisecond pause buckets 
    group_by            (Expected = None) 
    filter_by           (Expected = pauses_only)
    labels              (Expected = labels variable)
    column              (Expected = None)
    column_timing       (Expected = None)
    frequency_ticks     (Expected = True/False)

Note: a `gc event log` is a pandas dataframe, containing labeled columns to describe fields in a recorded event, and each row representing a discerete event. A list of `gc event logs` are returned from the function `get_gc_event_tables()` in `read_log_file.py`, which is used to automatically parse log files. 



`plot_heatmap()` parameters:

- **gc_event_dataframes**: `list` datatype. Each list entry is expected to be a `gc event log`. The `gc event logs` in the list will be parsed for the columns described by the parameters `column` and `column_timing` for Y and X data respectively, after filters have been applied.

- **-dimensions**-: a 4 length list, with the following values contained within the list
    - dimensions[0] = number of x intervals, or number of columns in the heat map
    - dimensions[1] = number of y intervals, or number of rows in the heat map
    - dimensions[2] = duration of a single x interval in seconds, or time duration of each column on the heatmap
    - dimensions[3] = duration of a single y interval in seconds, or time duration in each row of the heatmap.

Dimensions were choosen to be a required parameter rather than automatically set during runtime so comparion between multiple iterations of the tool would be easy to visually compare using the same X and Y axis scalings. Currently, there is a known issue where the color-bar frequency ranges may change between plots.

- **group_by**: `str` datatype. Name of a column present in the `gc event logs`. If this parameter is provided, groups all repeated values from the specified column, such that every group has the same value in column '`group_by`'. Leaving this optional parameter as `None` defaults to creating 1 group per `gc event log` in the `gc_event_dataframes` list. Examples below

      group_by = "EventName"
      group_by = "EventType"

- **filter_by** : `function` datatype. A boolean function to be applied to each row of each `gc event log`. If the function evaluates to false, then that event will not be included in the resulting plot. A typical function first checks if the column exists before checking any values, as seen in the example below. If this check is not in place, a `KeyError` may be thrown.
        
      def pauses_only(row):
           if "EventType" in row:
               if row["EventType] == "Pause":
                   return True
       return False
        
       filter_by = pauses_only

- **labels** : `list` datatype. Each entry in the labels list describes the data in `gc_event_dataframes`, in order. Each entry in the labels list should be a `str` datatype. 

      labels = ["Monday log", "Tuesday Log", "Wednesday Log"]


- **column** : `str` datatype. The name of a column found in the list of `gc event logs`, representing the Y coordinate of data to plot. If `None` is passed, the default value for this parameter is `"Duration_milliseconds"`. 

      column = "Duration_milliseconds"

- **column_timing** :`str` datatype. The name of a column found in the list of `gc event logs`, representing the X coordinate of the data to plot. If `None` is passed, the default value for this parameter is `"TimeFromStart_seconds"`. 
      
      column_timing = "TimeFromStart_seconds"

- **frequency_ticks** : `bool` datatype. If True, the heatmap prints the freuquency reported onto each non-zero cell. Default is False.

        frequency_ticks = False
        
---







## 4. Logarithmic heatmaps.

Uses the function `plot_heatmaps_logarithmic()`. The parameters are listed below for the functions, with the expected values to create the plot described by `4. Logarithmic heatmaps` being described in paranthesis. There are TWO required parameters: both `gc_event_dataframes`, and `dimensions` are needed for this function.
    
    gc_event_dataframes (required)
    dimensions (Expected = [ 20,  15, 60, 2 ]) 
                                    ### 20 x axis columns
                                    ### 15 y column rows
                                    ### 60 seconds == 1 minute intervals
                                    ### 2 = log base 2
    group_by            (Expected = None) 
    filter_by           (Expected = pauses_only)]
    labels              (Expected = labels variable)
    column              (Expected = None)
    column_timing       (Expected = None)
    frequency_ticks     (Expected = True/False)

Note: a `gc event log` is a pandas dataframe, containing labeled columns to describe fields in a recorded event, and each row representing a discerete event. A list of `gc event logs` are returned from the function `get_gc_event_tables()` in `read_log_file.py`, which is used to automatically parse log files. 

`plot_heatmaps_logarithmic()` parameters:

- **gc_event_dataframes**: `list` datatype. Each list entry is expected to be a `gc event log`. The `gc event logs` in the list will be parsed for the columns described by the parameters `column` and `column_timing` for Y and X data respectively, after filters have been applied.

- **-dimensions**-: a 4 length list, with the following values contained within the list
    - dimensions[0] = number of x intervals, or number of columns in the heat map
    - dimensions[1] = number of y intervals, or number of rows in the heat map
    - dimensions[2] = duration of a single x interval in seconds, or time duration of each column on the heatmap
    - dimensions[3] = base for logarithmic scaling. (typically 2 or 10)


- **group_by**: `str` datatype. Name of a column present in the `gc event logs`. If this parameter is provided, groups all repeated values from the specified column, such that every group has the same value in column '`group_by`'. Leaving this optional parameter as `None` defaults to creating 1 group per `gc event log` in the `gc_event_dataframes` list. Examples below

      group_by = "EventName"
      group_by = "EventType"

- **filter_by** : `function` datatype. A boolean function to be applied to each row of each `gc event log`. If the function evaluates to false, then that event will not be included in the resulting plot. A typical function first checks if the column exists before checking any values, as seen in the example below. If this check is not in place, a `KeyError` may be thrown.
        
      def pauses_only(row):
           if "EventType" in row:
               if row["EventType] == "Pause":
                   return True
       return False
        
       filter_by = pauses_only

- **labels** : `list` datatype. Each entry in the labels list describes the data in `gc_event_dataframes`, in order. Each entry in the labels list should be a `str` datatype. 

      labels = ["Monday log", "Tuesday Log", "Wednesday Log"]


- **column** : `str` datatype. The name of a column found in the list of `gc event logs`, representing the Y coordinate of data to plot. If `None` is passed, the default value for this parameter is `"Duration_milliseconds"`. 

      column = "Duration_milliseconds"

- **column_timing** :`str` datatype. The name of a column found in the list of `gc event logs`, representing the X coordinate of the data to plot. If `None` is passed, the default value for this parameter is `"TimeFromStart_seconds"`. 
      
      column_timing = "TimeFromStart_seconds"

- **frequency_ticks** : `bool` datatype. If True, the heatmap prints the freuquency reported onto each non-zero cell. Default is False.

        frequency_ticks = False
        

---




## 5. Latency percentiles over time intervals
Uses the function `plot_percentile_intervals()`. The parameters are listed below for the functions, with the expected values to create the plot described by `5. Latency percentiles over time intervals` being described in paranthesis. The only required parameter is `gc_event_dataframes` 
    
    gc_event_dataframes (required)
    group_by            (Expected = None) 
    filter_by           (Expected = pauses_only)
    labels              (Expected = labels variable)
    colors              (Expected = None)
    plot                (Expected = None)
    column              (Expected = None)
    interval_duration   (Expected = 60) # any positive float or integer 
    column_timing       (Expected = None)
    line_graph          (Expected = False)
    different_colors    (Expected = True)

Note: a `gc event log` is a pandas dataframe, containing labeled columns to describe fields in a recorded event, and each row representing a discerete event. A list of `gc event logs` are returned from the function `get_gc_event_tables()` in `read_log_file.py`, which is used to automatically parse log files. 

`plot_percentile_intervals()` parameters:

- **gc_event_dataframes**: `list` datatype. Each list entry is expected to be a `gc event log`. The `gc event logs` in the list will be parsed for the columns described by the parameters `column` and `column_timing` for Y and X data respectively, after filters have been applied.

- **group_by**: `str` datatype. Name of a column present in the `gc event logs`. If this parameter is provided, groups all repeated values from the specified column, such that every group has the same value in column '`group_by`'. Leaving this optional parameter as `None` defaults to creating 1 group per `gc event log` in the `gc_event_dataframes` list. Examples below

      group_by = "EventName"
      group_by = "EventType"

- **filter_by** : `function` datatype. A boolean function to be applied to each row of each `gc event log`. If the function evaluates to false, then that event will not be included in the resulting plot. A typical function first checks if the column exists before checking any values, as seen in the example below. If this check is not in place, a `KeyError` may be thrown.
        
      def pauses_only(row):
           if "EventType" in row:
               if row["EventType] == "Pause":
                   return True
       return False
        
       filter_by = pauses_only

- **labels** : `list` datatype. Each entry in the labels list describes the data in `gc_event_dataframes`, in order. Each entry in the labels list should be a `str` datatype. 

      labels = ["Monday log", "Tuesday Log", "Wednesday Log"]

- **colors** : `list` datatype. Each entry in the labels list picks a color for the output groups in the created plot, in order. If `None`, a set of discrete colors in the same order will be used. Each entry of this list is either a `str` describing one of the [matplotlib named colors](https://matplotlib.org/stable/gallery/color/named_colors.html), or is an (r, g, b) triplet with values between [0-1] representing brightness on a scaled (0-255) range.

      colors = ["black", "darkslateblue", (1, 0.5, 0)]

- **plot** : `matplotlib.axes._subplots.AxesSubplot` datatype. Each graphing function returns an instance of this plot object. Passing None creates a new figure. Passing an instance of a plot will keep all old data on the plot, and add the newly plotted data on top. Typically used to overlay two data sets with different column names.

      plot = plot_scatter(gc_event_dataframes)
      plot = plot_line(gc_event_dataframes, group_by = "EventNames")

- **column** : `str` datatype. The name of a column found in the list of `gc event logs`, representing the Y coordinate of data to plot. If `None` is passed, the default value for this parameter is `"Duration_milliseconds"`. 

      column = "Duration_milliseconds"

- **interval_duration** : `float` or `int` datatype. The duration in seconds for grouping of times. For this function, that would be the size of each grouping on the histogram

      interval_duration = 3600 # 1 hour
      interval_duration = 1.5  # 1.5 seconds

- **column_timing** :`str` datatype. The name of a column found in the list of `gc event logs`, representing the X coordinate of the data to plot. If `None` is passed, the default value for this parameter is `"TimeFromStart_seconds"`. 
      
      column_timing = "TimeFromStart_seconds"

- **line_graph** : `bool` datatype. If True, the graph plotted will be in line graph style, rather than scatter plot. If False or None, then it will remain scatter plot. Default False.

      line_graoh = True

- **different_colors** : `bool` datatype. If True, then each line plotted will be unique. If false, for each group, the opacity of the color will change, but the colors will be the same. It is recommended to use different_colors = False when line_graph is True.

       different_colors = False

---




## 6. Sum of pause durations over intervals
Uses the function `plot_sum_pause_intervals()`. The parameters are listed below for the functions, with the expected values to create the plot described by `6. Sum of pause durations over intervals` being described in paranthesis. The only required parameter is `gc_event_dataframes`.
    
    gc_event_dataframes    (required)
    group_by               (Expected = None) 
    filter_by              (Expected = pauses_only)
    labels                 (Expected = labels variable)
    colors                 (Expected = None)
    plot                   (Expected = None)
    column                 (Expected = "GCIndex")
    interval_duration      (Expected = 60) # any positive integer or float
    column_timing          (Expected = None)
    remove_empty_intervals (Expected = False)
    line_graph             (Expected = False)

Note: a `gc event log` is a pandas dataframe, containing labeled columns to describe fields in a recorded event, and each row representing a discerete event. A list of `gc event logs` are returned from the function `get_gc_event_tables()` in `read_log_file.py`, which is used to automatically parse log files. 

`plot_frequency_of_gc_intervals()` parameters:

- **gc_event_dataframes**: `list` datatype. Each list entry is expected to be a `gc event log`. The `gc event logs` in the list will be parsed for the columns described by the parameters `column` and `column_timing` for Y and X data respectively, after filters have been applied.

- **group_by**: `str` datatype. Name of a column present in the `gc event logs`. If this parameter is provided, groups all repeated values from the specified column, such that every group has the same value in column '`group_by`'. Leaving this optional parameter as `None` defaults to creating 1 group per `gc event log` in the `gc_event_dataframes` list. Examples below

      group_by = "EventName"
      group_by = "EventType"

- **filter_by** : `function` datatype. A boolean function to be applied to each row of each `gc event log`. If the function evaluates to false, then that event will not be included in the resulting plot. A typical function first checks if the column exists before checking any values, as seen in the example below. If this check is not in place, a `KeyError` may be thrown.
        
      def pauses_only(row):
           if "EventType" in row:
               if row["EventType] == "Pause":
                   return True
       return False
        
       filter_by = pauses_only

- **labels** : `list` datatype. Each entry in the labels list describes the data in `gc_event_dataframes`, in order. Each entry in the labels list should be a `str` datatype. 

      labels = ["Monday log", "Tuesday Log", "Wednesday Log"]

- **colors** : `list` datatype. Each entry in the labels list picks a color for the output groups in the created plot, in order. If `None`, a set of discrete colors in the same order will be used. Each entry of this list is either a `str` describing one of the [matplotlib named colors](https://matplotlib.org/stable/gallery/color/named_colors.html), or is an (r, g, b) triplet with values between [0-1] representing brightness on a scaled (0-255) range.

      colors = ["black", "darkslateblue", (1, 0.5, 0)]

- **plot** : `matplotlib.axes._subplots.AxesSubplot` datatype. Each graphing function returns an instance of this plot object. Passing None creates a new figure. Passing an instance of a plot will keep all old data on the plot, and add the newly plotted data on top. Typically used to overlay two data sets with different column names.

      plot = plot_scatter(gc_event_dataframes)
      plot = plot_line(gc_event_dataframes, group_by = "EventNames")

- **column** : `str` datatype. The name of a column found in the list of `gc event logs`, representing the Y coordinate of data to plot. If `None` is passed, the default value for this parameter is `"Duration_milliseconds"`. 

      column = "Duration_milliseconds"

- **interval_duration** : `float` or `int` datatype. The duration in seconds for grouping of times. For this function, that would be the period of time in which the gc events durations are summed

      interval_duration = 3600 # 1 hour
      interval_duration = 1.5  # 1.5 seconds

- **column_timing** :`str` datatype. The name of a column found in the list of `gc event logs`, representing the X coordinate of the data to plot. If `None` is passed, the default value for this parameter is `"TimeFromStart_seconds"`. 
      
      column_timing = "TimeFromStart_seconds"

- **remove_empty_intervals** : `bool` datatype. if True, then intervals where the sum of pauses = 0 will not be plotted. Default = False.

      remove_empty_intervals = False

- **line_graph** : `bool` datatype. If True, the graph plotted will be in line graph style, rather than scatter plot. If False or None, then it will remain scatter plot. Default False.

      line_graph = False
---








## 7. Percentage of heap filled after GC
Uses the function `plot_scatter()`. This function is interchangeable with the function `plot_line()` if a line plot is desired, with the same parameters for both functions. The parameters are listed below for the functions, with the expected values to create the plot described by ` 7. Percentage of heap filled after GC` being described in paranthesis. The only required parameter is `gc_event_dataframes` 
    
    gc_event_dataframes (required)
    group_by            (Expected = None) 
    filter_by           (Expected = heap_percent_full_filter)
    labels              (Expected = labels variable)
    colors              (Expected = None)
    plot                (Expected = None)
    column              (Expected = "HeapPercentFull") 
    column_timing       (Expected = None)

Note: a `gc event log` is a pandas dataframe, containing labeled columns to describe fields in a recorded event, and each row representing a discerete event. A list of `gc event logs` are returned from the function `get_gc_event_tables()` in `read_log_file.py`, which is used to automatically parse log files. 

`plot_scatter()` / `plot_line()` parameters:

- **gc_event_dataframes**: `list` datatype. Each list entry is expected to be a `gc event log`. The `gc event logs` in the list will be parsed for the columns described by the parameters `column` and `column_timing` for Y and X data respectively, after filters have been applied.

- **group_by**: `str` datatype. Name of a column present in the `gc event logs`. If this parameter is provided, groups all repeated values from the specified column, such that every group has the same value in column '`group_by`'. Leaving this optional parameter as `None` defaults to creating 1 group per `gc event log` in the `gc_event_dataframes` list. Examples below

      group_by = "EventName"
      group_by = "EventType"

- **filter_by** : `function` datatype. A boolean function to be applied to each row of each `gc event log`. If the function evaluates to false, then that event will not be included in the resulting plot. A typical function first checks if the column exists before checking any values, as seen in the example below. If this check is not in place, a `KeyError` may be thrown.
        
      def pauses_only(row):
           if "EventType" in row:
               if row["EventType] == "Pause":
                   return True
       return False
        
       filter_by = pauses_only

- **labels** : `list` datatype. Each entry in the labels list describes the data in `gc_event_dataframes`, in order. Each entry in the labels list should be a `str` datatype. 

      labels = ["Monday log", "Tuesday Log", "Wednesday Log"]

- **colors** : `list` datatype. Each entry in the labels list picks a color for the output groups in the created plot, in order. If `None`, a set of discrete colors in the same order will be used. Each entry of this list is either a `str` describing one of the [matplotlib named colors](https://matplotlib.org/stable/gallery/color/named_colors.html), or is an (r, g, b) triplet with values between [0-1] representing brightness on a scaled (0-255) range.

      colors = ["black", "darkslateblue", (1, 0.5, 0)]

- **plot** : `matplotlib.axes._subplots.AxesSubplot` datatype. Each graphing function returns an instance of this plot object. Passing None creates a new figure. Passing an instance of a plot will keep all old data on the plot, and add the newly plotted data on top. Typically used to overlay two data sets with different column names.

      plot = plot_scatter(gc_event_dataframes)
      plot = plot_line(gc_event_dataframes, group_by = "EventNames")

- **column** : `str` datatype. The name of a column found in the list of `gc event logs`, representing the Y coordinate of data to plot. If `None` is passed, the default value for this parameter is `"Duration_milliseconds"`. 

      column = "Duration_milliseconds"

- **column_timing** :`str` datatype. The name of a column found in the list of `gc event logs`, representing the X coordinate of the data to plot. If `None` is passed, the default value for this parameter is `"TimeFromStart_seconds"`. 
      
      column_timing = "TimeFromStart_seconds"

---

## 8. Heap Before and After GC
Uses the function `plot_line()`. This function is interchangeable with the function `plot_scatter()` if a line plot is desired, with the same parameters for both functions. The parameters are listed below for the functions, with the expected values to create the plot described by `8a. Heap Before GC` being described in paranthesis. The only required parameter is `gc_event_dataframes`.
    
    gc_event_dataframes (required)
    group_by            (Expected = "EventName") 
    filter_by           (Expected = pauses_only)
    labels              (Expected = labels variable)
    colors              (Expected = None)
    plot                (Expected = None)
    column              (Expected = None)
    column_timing       (Expected = None)

Note: a `gc event log` is a pandas dataframe, containing labeled columns to describe fields in a recorded event, and each row representing a discerete event. A list of `gc event logs` are returned from the function `get_gc_event_tables()` in `read_log_file.py`, which is used to automatically parse log files. 

`plot_scatter()` / `plot_line()` parameters:

- **gc_event_dataframes**: `list` datatype. Each list entry is expected to be a `gc event log`. The `gc event logs` in the list will be parsed for the columns described by the parameters `column` and `column_timing` for Y and X data respectively, after filters have been applied.

- **group_by**: `str` datatype. Name of a column present in the `gc event logs`. If this parameter is provided, groups all repeated values from the specified column, such that every group has the same value in column '`group_by`'. Leaving this optional parameter as `None` defaults to creating 1 group per `gc event log` in the `gc_event_dataframes` list. Examples below

      group_by = "EventName"
      group_by = "EventType"

- **filter_by** : `function` datatype. A boolean function to be applied to each row of each `gc event log`. If the function evaluates to false, then that event will not be included in the resulting plot. A typical function first checks if the column exists before checking any values, as seen in the example below. If this check is not in place, a `KeyError` may be thrown.
        
      def pauses_only(row):
           if "EventType" in row:
               if row["EventType] == "Pause":
                   return True
       return False
        
    filter_by = pauses_only

- **labels** : `list` datatype. Each entry in the labels list describes the data in `gc_event_dataframes`, in order. Each entry in the labels list should be a `str` datatype. 

      labels = ["Monday log", "Tuesday Log", "Wednesday Log"]

- **colors** : `list` datatype. Each entry in the labels list picks a color for the output groups in the created plot, in order. If `None`, a set of discrete colors in the same order will be used. Each entry of this list is either a `str` describing one of the [matplotlib named colors](https://matplotlib.org/stable/gallery/color/named_colors.html), or is an (r, g, b) triplet with values between [0-1] representing brightness on a scaled (0-255) range.

      colors = ["black", "darkslateblue", (1, 0.5, 0)]

- **plot** : `matplotlib.axes._subplots.AxesSubplot` datatype. Each graphing function returns an instance of this plot object. Passing None creates a new figure. Passing an instance of a plot will keep all old data on the plot, and add the newly plotted data on top. Typically used to overlay two data sets with different column names.

      plot = plot_scatter(gc_event_dataframes)
      plot = plot_line(gc_event_dataframes, group_by = "EventNames")

- **column** : `str` datatype. The name of a column found in the list of `gc event logs`, representing the Y coordinate of data to plot. If `None` is passed, the default value for this parameter is `"Duration_milliseconds"`. 

      column = "Duration_milliseconds"

- **column_timing** :`str` datatype. The name of a column found in the list of `gc event logs`, representing the X coordinate of the data to plot. If `None` is passed, the default value for this parameter is `"TimeFromStart_seconds"`. 
      
      column_timing = "TimeFromStart_seconds"
---



## 9. MB Reclaimed during program runtime

> Important: This function relies on data being stored in columns named "HeapBeforeGC" and "HeapAfterGC". 

Uses the function `plot_reclaimed_bytes()`. The parameters are listed below for the functions, with the expected values to create the plot described by `9. MB Reclaimed during program runtime` being described in paranthesis. The only required parameter is `gc_event_dataframes`.
    
    gc_event_dataframes (required)
    group_by            (Expected = None) 
    filter_by           (Expected = gc_values_present)
    labels              (Expected = labels variable)
    colors              (Expected = None)
    plot                (Expected = None)
    column_timing       (Expected = None)

Note: a `gc event log` is a pandas dataframe, containing labeled columns to describe fields in a recorded event, and each row representing a discerete event. A list of `gc event logs` are returned from the function `get_gc_event_tables()` in `read_log_file.py`, which is used to automatically parse log files. 

`plot_reclaimed_bytes()` parameters:

- **gc_event_dataframes**: `list` datatype. Each list entry is expected to be a `gc event log`. The `gc event logs` in the list will be parsed for the columns described by the parameters `column` and `column_timing` for Y and X data respectively, after filters have been applied.

- **group_by**: `str` datatype. Name of a column present in the `gc event logs`. If this parameter is provided, groups all repeated values from the specified column, such that every group has the same value in column '`group_by`'. Leaving this optional parameter as `None` defaults to creating 1 group per `gc event log` in the `gc_event_dataframes` list. Examples below

      group_by = "EventName"
      group_by = "EventType"

- **filter_by** : `function` datatype. A boolean function to be applied to each row of each `gc event log`. If the function evaluates to false, then that event will not be included in the resulting plot. A typical function first checks if the column exists before checking any values, as seen in the example below. If this check is not in place, a `KeyError` may be thrown.
        
      def pauses_only(row):
           if "EventType" in row:
               if row["EventType] == "Pause":
                   return True
       return False
        
    filter_by = pauses_only

- **labels** : `list` datatype. Each entry in the labels list describes the data in `gc_event_dataframes`, in order. Each entry in the labels list should be a `str` datatype. 

      labels = ["Monday log", "Tuesday Log", "Wednesday Log"]

- **colors** : `list` datatype. Each entry in the labels list picks a color for the output groups in the created plot, in order. If `None`, a set of discrete colors in the same order will be used. Each entry of this list is either a `str` describing one of the [matplotlib named colors](https://matplotlib.org/stable/gallery/color/named_colors.html), or is an (r, g, b) triplet with values between [0-1] representing brightness on a scaled (0-255) range.

      colors = ["black", "darkslateblue", (1, 0.5, 0)]

- **plot** : `matplotlib.axes._subplots.AxesSubplot` datatype. Each graphing function returns an instance of this plot object. Passing None creates a new figure. Passing an instance of a plot will keep all old data on the plot, and add the newly plotted data on top. Typically used to overlay two data sets with different column names.

      plot = plot_scatter(gc_event_dataframes)
      plot = plot_line(gc_event_dataframes, group_by = "EventNames")


- **column_timing** :`str` datatype. The name of a column found in the list of `gc event logs`, representing the X coordinate of the data to plot. If `None` is passed, the default value for this parameter is `"TimeFromStart_seconds"`. 

---


## 10. Heap allocation rate
Uses the function `allocation_rate()`. The parameters are listed below for the functions, with the expected values to create the plot described by `10. Heap allocation rate ` being described in paranthesis. The only required parameter is `gc_event_dataframes`.
    
    gc_event_dataframes (required)
    group_by            (Expected = None) 
    filter_by           (Expected = diff_in_entries_filter)
    labels              (Expected = labels variable)
    interval_duration   (Expected = 60) # some int or float number
    colors              (Expected = None)
    plot                (Expected = None)
    column_before       (Expected = None)
    column_after        (Expected = None)
    column_timing       (Expected = None)
    percentile          (Expected = 100) 
    line_graph          (Expected = False)

Note: a `gc event log` is a pandas dataframe, containing labeled columns to describe fields in a recorded event, and each row representing a discerete event. A list of `gc event logs` are returned from the function `get_gc_event_tables()` in `read_log_file.py`, which is used to automatically parse log files. 

`allocation_rate()` parameters:

- **gc_event_dataframes**: `list` datatype. Each list entry is expected to be a `gc event log`. The `gc event logs` in the list will be parsed for the columns described by the parameters `column` and `column_timing` for Y and X data respectively, after filters have been applied.

- **group_by**: `str` datatype. Name of a column present in the `gc event logs`. If this parameter is provided, groups all repeated values from the specified column, such that every group has the same value in column '`group_by`'. Leaving this optional parameter as `None` defaults to creating 1 group per `gc event log` in the `gc_event_dataframes` list. Examples below

      group_by = "EventName"
      group_by = "EventType"

- **filter_by** : `function` datatype. A boolean function to be applied to each row of each `gc event log`. If the function evaluates to false, then that event will not be included in the resulting plot. A typical function first checks if the column exists before checking any values, as seen in the example below. If this check is not in place, a `KeyError` may be thrown.
        
      def pauses_only(row):
           if "EventType" in row:
               if row["EventType] == "Pause":
                   return True
       return False
        
       filter_by = pauses_only

- **labels** : `list` datatype. Each entry in the labels list describes the data in `gc_event_dataframes`, in order. Each entry in the labels list should be a `str` datatype. 

      labels = ["Monday log", "Tuesday Log", "Wednesday Log"]

- **interval_duration** : `float` or `int` datatype. The duration in seconds for grouping of times. For this function, that would be the size of each grouping on the histogram

      interval_duration = 3600 # 1 hour
      interval_duration = 1.5  # 1.5 seconds


- **colors** : `list` datatype. Each entry in the labels list picks a color for the output groups in the created plot, in order. If `None`, a set of discrete colors in the same order will be used. Each entry of this list is either a `str` describing one of the [matplotlib named colors](https://matplotlib.org/stable/gallery/color/named_colors.html), or is an (r, g, b) triplet with values between [0-1] representing brightness on a scaled (0-255) range.

      colors = ["black", "darkslateblue", (1, 0.5, 0)]

- **plot** : `matplotlib.axes._subplots.AxesSubplot` datatype. Each graphing function returns an instance of this plot object. Passing None creates a new figure. Passing an instance of a plot will keep all old data on the plot, and add the newly plotted data on top. Typically used to overlay two data sets with different column names.

      plot = plot_scatter(gc_event_dataframes)
      plot = plot_line(gc_event_dataframes, group_by = "EventNames")

- **column_before** : `str` datatype. The name of a column found in the list of `gc event logs`, representing the Y coordinate of data to plot before the event. If `None` is passed, the default value for this parameter is `"HeapBeforeGC"`. 

      column_before = "HeapBeforeGC"

- **column_after** :`str` datatype. The name of a column found in the list of `gc event logs`, representing the Y coordinate of the data to plot after the event. If `None` is passed, the default value for this parameter is `"HeapAfterGC"`. 
      
      column_after = "HeapAfterGC"

- **column_timing** :`str` datatype. The name of a column found in the list of `gc event logs`, representing the X coordinate of the data to plot. If `None` is passed, the default value for this parameter is `"TimeFromStart_seconds"`. 
      
      column_timing = "TimeFromStart_seconds"

- **line_graph** : `bool` datatype. If True, the graph plotted will be in line graph style, rather than scatter plot. If False or None, then it will remain scatter plot. Default False.

      line_graph = False
---

## 11. Percentage Used in Each Code Heap
Uses the function `plot_line()` and `plot_scatter()`. These function are interchangeable if desired, with the same parameters for both functions. The parameters for the functions, and their expected values are listed below. The only required parameter is `gc_event_dataframes`.

    gc_event_dataframes (required)
    group_by            (Expected = None) 
    filter_by           (Expected = non_profiled_nmethods_code_heap_percent_used_filter /
    filter_by           (Expected = non_profiled_nmethods_code_heap_percent_max_used_filter /
                                    profiled_nmethods_code_heap_percent_used_filter /
                                    profiled_nmethods_code_heap_percent_max_used_filter /
                                    non_nmethods_code_heap_percent_used_filter /
                                    non_nmethods_code_heap_percent_max_used_filter)
    labels              (Expected = labels variable)
    colors              (Expected = None)
    plot                (Expected = None)
    column              (Expected = "NonProfiledNMethodsCodeHeapPercentUsed" /
    column              (Expected = "NonProfiledNMethodsCodeHeapPercentMaxUsed" /
                                    "ProfiledNMethodsCodeHeapPercentUsed" /
                                    "ProfiledNMethodsCodeHeapPercentMaxUsed" /
                                    "NonNMethodsCodeHeapPercentUsed" / 
                                    "NonNMethodsCodeHeapPercentMaxUsed") 
    column_timing       (Expected = None)

Note: a `gc event log` is a pandas dataframe, containing labeled columns to describe fields in a recorded event, and each row representing a discerete event. A list of `gc event logs` are returned from the function `get_gc_event_tables()` in `read_log_file.py`, which is used to automatically parse log files.

`plot_scatter()` / `plot_line()` parameters:

- **gc_event_dataframes**: `list` datatype. Each list entry is expected to be a `gc event log`. The `gc event logs` in the list will be parsed for the columns described by the parameters `column` and `column_timing` for Y and X data respectively, after filters have been applied.

- **group_by**: `str` datatype. Name of a column present in the `gc event logs`. If this parameter is provided, groups all repeated values from the specified column, such that every group has the same value in column '`group_by`'. Leaving this optional parameter as `None` defaults to creating 1 group per `gc event log` in the `gc_event_dataframes` list. Examples below

      group_by = "EventName"
      group_by = "EventType"

- **filter_by** : `function` datatype. A boolean function to be applied to each row of each `gc event log`. If the function evaluates to false, then that event will not be included in the resulting plot. A typical function first checks if the column exists before checking any values, as seen in the example below. If this check is not in place, a `KeyError` may be thrown.

      def pauses_only(row):
           if ("EventType" in row) and (row["EventType] == "Pause"):
               return True
      return False

      filter_by = pauses_only

- **labels** : `list` datatype. Each entry in the labels list describes the data in `gc_event_dataframes`, in order. Each entry in the labels list should be a `str` datatype.

      labels = ["Monday log", "Tuesday Log", "Wednesday Log"]

- **colors** : `list` datatype. Each entry in the labels list picks a color for the output groups in the created plot, in order. If `None`, a set of discrete colors in the same order will be used. Each entry of this list is either a `str` describing one of the [matplotlib named colors](https://matplotlib.org/stable/gallery/color/named_colors.html), or is an (r, g, b) triplet with values between [0-1] representing brightness on a scaled (0-255) range.

      colors = ["black", "darkslateblue", (1, 0.5, 0)]

- **plot** : `matplotlib.axes._subplots.AxesSubplot` datatype. Each graphing function returns an instance of this plot object. Passing None creates a new figure. Passing an instance of a plot will keep all old data on the plot, and add the newly plotted data on top. Typically used to overlay two data sets with different column names.

      plot = plot_scatter(gc_event_dataframes)
      plot = plot_line(gc_event_dataframes, group_by = "EventNames")

- **column** : `str` datatype. The name of a column found in the list of `gc event logs`, representing the Y coordinate of data to plot. If `None` is passed, the default value for this parameter is `"Duration_milliseconds"`.

      column = "Duration_milliseconds"

- **column_timing** :`str` datatype. The name of a column found in the list of `gc event logs`, representing the X coordinate of the data to plot. If `None` is passed, the default value for this parameter is `"TimeFromStart_seconds"`.

      column_timing = "TimeFromStart_seconds"

---

## 12. Code Cache Flushing Rate
Uses the function `plot_code_cache_flushing_rate()`. The parameters are listed below for the functions, with the expected values to create the plot described by `12. Code Cache Flushing Rate` being described in paranthesis. The only required parameters are `gc_event_dataframes` and `interval_duration`.

    gc_event_dataframes (required)
    labels              (Expected = labels variable)
    colors              (Expected = None)
    plot                (Expected = None)
    line_graph          (Expected = False)

Note: a `gc event log` is a pandas dataframe, containing labeled columns to describe fields in a recorded event, and each row representing a discerete event. A list of `gc event logs` are returned from the function `get_gc_event_tables()` in `read_log_file.py`, which is used to automatically parse log files.

`plot_code_cache_flushing_rate()` parameters:

- **gc_event_dataframes**: `list` datatype. Each list entry is expected to be a `gc event log`. The `gc event logs` in the list will be parsed for the columns described by the parameters `column` and `column_timing` for Y and X data respectively, after filters have been applied.

- **labels** : `list` datatype. Each entry in the labels list describes the data in `gc_event_dataframes`, in order. Each entry in the labels list should be a `str` datatype.

      labels = ["Monday log", "Tuesday Log", "Wednesday Log"]

- **colors** : `list` datatype. Each entry in the labels list picks a color for the output groups in the created plot, in order. If `None`, a set of discrete colors in the same order will be used. Each entry of this list is either a `str` describing one of the [matplotlib named colors](https://matplotlib.org/stable/gallery/color/named_colors.html), or is an (r, g, b) triplet with values between [0-1] representing brightness on a scaled (0-255) range.

      colors = ["black", "darkslateblue", (1, 0.5, 0)]

- **plot** : `matplotlib.axes._subplots.AxesSubplot` datatype. Each graphing function returns an instance of this plot object. Passing None creates a new figure. Passing an instance of a plot will keep all old data on the plot, and add the newly plotted data on top. Typically used to overlay two data sets with different column names.

      plot = plot_scatter(gc_event_dataframes)
      plot = plot_line(gc_event_dataframes, group_by = "EventNames")

- **line_graph** : `bool` datatype. If True, the graph plotted will be in line graph style, rather than scatter plot. If False or None, then it will remain scatter plot. Default False.

      line_graph = False
---

## 13. Used Metaspace After GC
Uses the function `plot_line()`. This function is interchangeable with the function `plot_scatter()` if a scatter plot is desired, with the same parameters for both functions. The parameters for the functions, and their expected values are listed below. The only required parameter is `gc_event_dataframes`.

    gc_event_dataframes (required)
    group_by            (Expected = None) 
    filter_by           (Expected = used_metaspace_after_gc_filter)
    labels              (Expected = labels variable)
    colors              (Expected = None)
    plot                (Expected = None)
    column              (Expected = "UsedMetaspaceAfterGC") 
    column_timing       (Expected = None)

Note: a `gc event log` is a pandas dataframe, containing labeled columns to describe fields in a recorded event, and each row representing a discerete event. A list of `gc event logs` are returned from the function `get_gc_event_tables()` in `read_log_file.py`, which is used to automatically parse log files.

`plot_scatter()` / `plot_line()` parameters:

- **gc_event_dataframes**: `list` datatype. Each list entry is expected to be a `gc event log`. The `gc event logs` in the list will be parsed for the columns described by the parameters `column` and `column_timing` for Y and X data respectively, after filters have been applied.

- **group_by**: `str` datatype. Name of a column present in the `gc event logs`. If this parameter is provided, groups all repeated values from the specified column, such that every group has the same value in column '`group_by`'. Leaving this optional parameter as `None` defaults to creating 1 group per `gc event log` in the `gc_event_dataframes` list. Examples below

      group_by = "EventName"
      group_by = "EventType"

- **filter_by** : `function` datatype. A boolean function to be applied to each row of each `gc event log`. If the function evaluates to false, then that event will not be included in the resulting plot. A typical function first checks if the column exists before checking any values, as seen in the example below. If this check is not in place, a `KeyError` may be thrown.

      def pauses_only(row):
           if ("EventType" in row) and (row["EventType] == "Pause"):
               return True
      return False

      filter_by = pauses_only

- **labels** : `list` datatype. Each entry in the labels list describes the data in `gc_event_dataframes`, in order. Each entry in the labels list should be a `str` datatype.

      labels = ["Monday log", "Tuesday Log", "Wednesday Log"]

- **colors** : `list` datatype. Each entry in the labels list picks a color for the output groups in the created plot, in order. If `None`, a set of discrete colors in the same order will be used. Each entry of this list is either a `str` describing one of the [matplotlib named colors](https://matplotlib.org/stable/gallery/color/named_colors.html), or is an (r, g, b) triplet with values between [0-1] representing brightness on a scaled (0-255) range.

      colors = ["black", "darkslateblue", (1, 0.5, 0)]

- **plot** : `matplotlib.axes._subplots.AxesSubplot` datatype. Each graphing function returns an instance of this plot object. Passing None creates a new figure. Passing an instance of a plot will keep all old data on the plot, and add the newly plotted data on top. Typically used to overlay two data sets with different column names.

      plot = plot_scatter(gc_event_dataframes)
      plot = plot_line(gc_event_dataframes, group_by = "EventNames")

- **column** : `str` datatype. The name of a column found in the list of `gc event logs`, representing the Y coordinate of data to plot. If `None` is passed, the default value for this parameter is `"Duration_milliseconds"`.

      column = "Duration_milliseconds"

- **column_timing** :`str` datatype. The name of a column found in the list of `gc event logs`, representing the X coordinate of the data to plot. If `None` is passed, the default value for this parameter is `"TimeFromStart_seconds"`.

      column_timing = "TimeFromStart_seconds"

---

## 14. Concurrent durations during runtime


Uses the function `plot_scatter()`. This function is interchangeable with the function `plot_line()` if a line plot is desired, with the same parameters for both functions. The parameters are listed below for the functions, with the expected values to create the plot described by `11. Concurrent durations during runtime` being described in paranthesis. The only required parameter is `gc_event_dataframes` 
    
    gc_event_dataframes (required)
    group_by            (Expected = None) 
    filter_by           (Expected = concurrent_only)
    labels              (Expected = labels variable)
    colors              (Expected = None)
    plot                (Expected = None)
    column              (Expected = None)
    column_timing       (Expected = None)

Note: a `gc event log` is a pandas dataframe, containing labeled columns to describe fields in a recorded event, and each row representing a discerete event. A list of `gc event logs` are returned from the function `get_gc_event_tables()` in `read_log_file.py`, which is used to automatically parse log files. 

`plot_scatter()` / `plot_line()` parameters:

- **gc_event_dataframes**: `list` datatype. Each list entry is expected to be a `gc event log`. The `gc event logs` in the list will be parsed for the columns described by the parameters `column` and `column_timing` for Y and X data respectively, after filters have been applied.

- **group_by**: `str` datatype. Name of a column present in the `gc event logs`. If this parameter is provided, groups all repeated values from the specified column, such that every group has the same value in column '`group_by`'. Leaving this optional parameter as `None` defaults to creating 1 group per `gc event log` in the `gc_event_dataframes` list. Examples below

      group_by = "EventName"
      group_by = "EventType"

- **filter_by** : `function` datatype. A boolean function to be applied to each row of each `gc event log`. If the function evaluates to false, then that event will not be included in the resulting plot. A typical function first checks if the column exists before checking any values, as seen in the example below. If this check is not in place, a `KeyError` may be thrown.
        
      def concurrent_only(row):
           if "EventType" in row:
               if row["EventType] == "Concurrent":
                   return True
       return False
        
       filter_by = concurrent_only

- **labels** : `list` datatype. Each entry in the labels list describes the data in `gc_event_dataframes`, in order. Each entry in the labels list should be a `str` datatype. 

      labels = ["Monday log", "Tuesday Log", "Wednesday Log"]

- **colors** : `list` datatype. Each entry in the labels list picks a color for the output groups in the created plot, in order. If `None`, a set of discrete colors in the same order will be used. Each entry of this list is either a `str` describing one of the [matplotlib named colors](https://matplotlib.org/stable/gallery/color/named_colors.html), or is an (r, g, b) triplet with values between [0-1] representing brightness on a scaled (0-255) range.

      colors = ["black", "darkslateblue", (1, 0.5, 0)]

- **plot** : `matplotlib.axes._subplots.AxesSubplot` datatype. Each graphing function returns an instance of this plot object. Passing None creates a new figure. Passing an instance of a plot will keep all old data on the plot, and add the newly plotted data on top. Typically used to overlay two data sets with different column names.

      plot = plot_scatter(gc_event_dataframes)
      plot = plot_line(gc_event_dataframes, group_by = "EventNames")

- **column** : `str` datatype. The name of a column found in the list of `gc event logs`, representing the Y coordinate of data to plot. If `None` is passed, the default value for this parameter is `"Duration_milliseconds"`. 

      column = "Duration_milliseconds"

- **column_timing** :`str` datatype. The name of a column found in the list of `gc event logs`, representing the X coordinate of the data to plot. If `None` is passed, the default value for this parameter is `"TimeFromStart_seconds"`. 
      
      column_timing = "TimeFromStart_seconds"

---


## 15. Sum of event durations, grouped by EventType


Uses the function `plot_bar_sum()`. The parameters are listed below for the functions, with the expected values to create the plot described by `12. Mean event durations` being described in paranthesis. The only required parameter is `gc_event_dataframes`.
    
    gc_event_dataframes (required)
    group_by            (Expected = "EventType") 
    filter_by           (Expected = concurrent_or_pauses)
    labels              (Expected = labels variable)
    colors              (Expected = None)
    plot                (Expected = None)
    column              (Expected = None)
    column_timing       (Expected = None)

Note: a `gc event log` is a pandas dataframe, containing labeled columns to describe fields in a recorded event, and each row representing a discerete event. A list of `gc event logs` are returned from the function `get_gc_event_tables()` in `read_log_file.py`, which is used to automatically parse log files. 

`plot_bar_sum()` parameters:

- **gc_event_dataframes**: `list` datatype. Each list entry is expected to be a `gc event log`. The `gc event logs` in the list will be parsed for the columns described by the parameters `column` and `column_timing` for Y and X data respectively, after filters have been applied.

- **group_by**: `str` datatype. Name of a column present in the `gc event logs`. If this parameter is provided, groups all repeated values from the specified column, such that every group has the same value in column '`group_by`'. Leaving this optional parameter as `None` defaults to creating 1 group per `gc event log` in the `gc_event_dataframes` list. Examples below

      group_by = "EventName"
      group_by = "EventType"

- **filter_by** : `function` datatype. A boolean function to be applied to each row of each `gc event log`. If the function evaluates to false, then that event will not be included in the resulting plot. A typical function first checks if the column exists before checking any values, as seen in the example below. If this check is not in place, a `KeyError` may be thrown.
        
      def pauses_only(row):
           if "EventType" in row:
               if row["EventType] == "Pause":
                   return True
       return False
        
       filter_by = pauses_only

- **labels** : `list` datatype. Each entry in the labels list describes the data in `gc_event_dataframes`, in order. Each entry in the labels list should be a `str` datatype. 

      labels = ["Monday log", "Tuesday Log", "Wednesday Log"]

- **colors** : `list` datatype. Each entry in the labels list picks a color for the output groups in the created plot, in order. If `None`, a set of discrete colors in the same order will be used. Each entry of this list is either a `str` describing one of the [matplotlib named colors](https://matplotlib.org/stable/gallery/color/named_colors.html), or is an (r, g, b) triplet with values between [0-1] representing brightness on a scaled (0-255) range.

      colors = ["black", "darkslateblue", (1, 0.5, 0)]

- **plot** : `matplotlib.axes._subplots.AxesSubplot` datatype. Each graphing function returns an instance of this plot object. Passing None creates a new figure. Passing an instance of a plot will keep all old data on the plot, and add the newly plotted data on top. Typically used to overlay two data sets with different column names.

      plot = plot_scatter(gc_event_dataframes)
      plot = plot_line(gc_event_dataframes, group_by = "EventNames")

- **column** : `str` datatype. The name of a column found in the list of `gc event logs`, representing the Y coordinate of data to plot. If `None` is passed, the default value for this parameter is `"Duration_milliseconds"`. 

      column = "Duration_milliseconds"

- **column_timing** :`str` datatype. The name of a column found in the list of `gc event logs`, representing the X coordinate of the data to plot. If `None` is passed, the default value for this parameter is `"TimeFromStart_seconds"`. 
      
      column_timing = "TimeFromStart_seconds"

---




## 16. Pauses summary

Uses the function `plot_summary()`. The parameters are listed below for the functions, with the expected values to create the plot described by `13. Pauses summary` being described in paranthesis. The only required parameter is `gc_event_dataframes`.

    gc_event_dataframes (required)
    group_by            (Expected = None) 
    filter_by           (Expected = pauses_only)
    labels              (Expected = labels variable)
    column              (Expected = None)
    throughput          (Expected = True)

Note: a `gc event log` is a pandas dataframe, containing labeled columns to describe fields in a recorded event, and each row representing a discerete event. A list of `gc event logs` are returned from the function `get_gc_event_tables()` in `read_log_file.py`, which is used to automatically parse log files. 

`plot_summary()` parameters:

- **gc_event_dataframes**: `list` datatype. Each list entry is expected to be a `gc event log`. The `gc event logs` in the list will be parsed for the columns described by the parameters `column` and `column_timing` for Y and X data respectively, after filters have been applied.

- **group_by**: `str` datatype. Name of a column present in the `gc event logs`. If this parameter is provided, groups all repeated values from the specified column, such that every group has the same value in column '`group_by`'. Leaving this optional parameter as `None` defaults to creating 1 group per `gc event log` in the `gc_event_dataframes` list. Examples below

      group_by = "EventName"
      group_by = "EventType"

- **filter_by** : `function` datatype. A boolean function to be applied to each row of each `gc event log`. If the function evaluates to false, then that event will not be included in the resulting plot. A typical function first checks if the column exists before checking any values, as seen in the example below. If this check is not in place, a `KeyError` may be thrown.
        
      def pauses_only(row):
           if "EventType" in row:
               if row["EventType] == "Pause":
                   return True
       return False
        
       filter_by = pauses_only

- **labels** : `list` datatype. Each entry in the labels list describes the data in `gc_event_dataframes`, in order. Each entry in the labels list should be a `str` datatype. 

      labels = ["Monday log", "Tuesday Log", "Wednesday Log"]

- **column** : `str` datatype. The name of a column found in the list of `gc event logs`, representing the Y coordinate of data to plot. If `None` is passed, the default value for this parameter is `"Duration_milliseconds"`. 

- **throughput** : `bool` datatype. If True, uses the provided timing information to attempt to calculate a throughput (time spent in program execution) / (total program time) * 100. Typically an illogical metric unless each group is all pauses from 1 file.

---



## 17. Pause percentiles
Uses the function `plot_percentiles()`. The parameters are listed below for the functions, with the expected values to create the plot described by `14. Pause percentiles` being described in paranthesis. The only required parameter is `gc_event_dataframes`.

    gc_event_dataframes (required)
    group_by            (Expected = None) 
    filter_by           (Expected = pauses_only)
    labels              (Expected = labels variable)
    column              (Expected = None)

Note: a `gc event log` is a pandas dataframe, containing labeled columns to describe fields in a recorded event, and each row representing a discerete event. A list of `gc event logs` are returned from the function `get_gc_event_tables()` in `read_log_file.py`, which is used to automatically parse log files. 

`plot_percentiles()` parameters:

- **gc_event_dataframes**: `list` datatype. Each list entry is expected to be a `gc event log`. The `gc event logs` in the list will be parsed for the columns described by the parameters `column` and `column_timing` for Y and X data respectively, after filters have been applied.

- **group_by**: `str` datatype. Name of a column present in the `gc event logs`. If this parameter is provided, groups all repeated values from the specified column, such that every group has the same value in column '`group_by`'. Leaving this optional parameter as `None` defaults to creating 1 group per `gc event log` in the `gc_event_dataframes` list. Examples below

      group_by = "EventName"
      group_by = "EventType"

- **filter_by** : `function` datatype. A boolean function to be applied to each row of each `gc event log`. If the function evaluates to false, then that event will not be included in the resulting plot. A typical function first checks if the column exists before checking any values, as seen in the example below. If this check is not in place, a `KeyError` may be thrown.
        
      def pauses_only(row):
           if "EventType" in row:
               if row["EventType] == "Pause":
                   return True
       return False
        
       filter_by = pauses_only

- **labels** : `list` datatype. Each entry in the labels list describes the data in `gc_event_dataframes`, in order. Each entry in the labels list should be a `str` datatype. 

      labels = ["Monday log", "Tuesday Log", "Wednesday Log"]

- **column** : `str` datatype. The name of a column found in the list of `gc event logs`, representing the Y coordinate of data to plot. If `None` is passed, the default value for this parameter is `"Duration_milliseconds"`. 

---

## 18. Mean and Sum of event durations

Uses the function `plot_bar_sum()` and `plot_bar_avg()`. The parameters are listed below for the functions, with the expected values to create the plot described by `15.  Mean and Sum of event durations` being described in paranthesis. The only required parameter is `gc_event_dataframes`.
    
    gc_event_dataframes (required)
    group_by            (Expected = "EventType") 
    filter_by           (Expected = concurrent_or_pauses)
    labels              (Expected = labels variable)
    colors              (Expected = None)
    plot                (Expected = None)
    column              (Expected = None)
    column_timing       (Expected = None)

Note: a `gc event log` is a pandas dataframe, containing labeled columns to describe fields in a recorded event, and each row representing a discerete event. A list of `gc event logs` are returned from the function `get_gc_event_tables()` in `read_log_file.py`, which is used to automatically parse log files. 

`plot_bar_sum() / plot_bar_avg()` parameters:

- **gc_event_dataframes**: `list` datatype. Each list entry is expected to be a `gc event log`. The `gc event logs` in the list will be parsed for the columns described by the parameters `column` and `column_timing` for Y and X data respectively, after filters have been applied.

- **group_by**: `str` datatype. Name of a column present in the `gc event logs`. If this parameter is provided, groups all repeated values from the specified column, such that every group has the same value in column '`group_by`'. Leaving this optional parameter as `None` defaults to creating 1 group per `gc event log` in the `gc_event_dataframes` list. Examples below

      group_by = "EventName"
      group_by = "EventType"

- **filter_by** : `function` datatype. A boolean function to be applied to each row of each `gc event log`. If the function evaluates to false, then that event will not be included in the resulting plot. A typical function first checks if the column exists before checking any values, as seen in the example below. If this check is not in place, a `KeyError` may be thrown.
        
      def pauses_only(row):
           if "EventType" in row:
               if row["EventType] == "Pause":
                   return True
       return False
        
       filter_by = pauses_only

- **labels** : `list` datatype. Each entry in the labels list describes the data in `gc_event_dataframes`, in order. Each entry in the labels list should be a `str` datatype. 

      labels = ["Monday log", "Tuesday Log", "Wednesday Log"]

- **colors** : `list` datatype. Each entry in the labels list picks a color for the output groups in the created plot, in order. If `None`, a set of discrete colors in the same order will be used. Each entry of this list is either a `str` describing one of the [matplotlib named colors](https://matplotlib.org/stable/gallery/color/named_colors.html), or is an (r, g, b) triplet with values between [0-1] representing brightness on a scaled (0-255) range.

      colors = ["black", "darkslateblue", (1, 0.5, 0)]

- **plot** : `matplotlib.axes._subplots.AxesSubplot` datatype. Each graphing function returns an instance of this plot object. Passing None creates a new figure. Passing an instance of a plot will keep all old data on the plot, and add the newly plotted data on top. Typically used to overlay two data sets with different column names.

      plot = plot_scatter(gc_event_dataframes)
      plot = plot_line(gc_event_dataframes, group_by = "EventNames")

- **column** : `str` datatype. The name of a column found in the list of `gc event logs`, representing the Y coordinate of data to plot. If `None` is passed, the default value for this parameter is `"Duration_milliseconds"`. 

      column = "Duration_milliseconds"

- **column_timing** :`str` datatype. The name of a column found in the list of `gc event logs`, representing the X coordinate of the data to plot. If `None` is passed, the default value for this parameter is `"TimeFromStart_seconds"`. 
      
      column_timing = "TimeFromStart_seconds"

---


## 19. Pause frequencies histogram

Uses the function `plot_frequency_intervals()`. The parameters are listed below for the functions, with the expected values to create the plot described by `16. Pause frequencies histogram` being described in paranthesis. The only required parameter is `gc_event_dataframes` 
    
    gc_event_dataframes (required)
    group_by            (Expected = None) 
    filter_by           (Expected = pauses_only)
    labels              (Expected = labels variable)
    colors              (Expected = None)
    plot                (Expected = None)
    column              (Expected = None)
    interval_duration   (Expected = 60) # any positive float or integer 
    column_timing       (Expected = None)

Note: a `gc event log` is a pandas dataframe, containing labeled columns to describe fields in a recorded event, and each row representing a discerete event. A list of `gc event logs` are returned from the function `get_gc_event_tables()` in `read_log_file.py`, which is used to automatically parse log files. 

`plot_frequency_intervals()` parameters:

- **gc_event_dataframes**: `list` datatype. Each list entry is expected to be a `gc event log`. The `gc event logs` in the list will be parsed for the columns described by the parameters `column` and `column_timing` for Y and X data respectively, after filters have been applied.

- **group_by**: `str` datatype. Name of a column present in the `gc event logs`. If this parameter is provided, groups all repeated values from the specified column, such that every group has the same value in column '`group_by`'. Leaving this optional parameter as `None` defaults to creating 1 group per `gc event log` in the `gc_event_dataframes` list. Examples below

      group_by = "EventName"
      group_by = "EventType"

- **filter_by** : `function` datatype. A boolean function to be applied to each row of each `gc event log`. If the function evaluates to false, then that event will not be included in the resulting plot. A typical function first checks if the column exists before checking any values, as seen in the example below. If this check is not in place, a `KeyError` may be thrown.
        
      def pauses_only(row):
           if "EventType" in row:
               if row["EventType] == "Pause":
                   return True
       return False
        
       filter_by = pauses_only

- **labels** : `list` datatype. Each entry in the labels list describes the data in `gc_event_dataframes`, in order. Each entry in the labels list should be a `str` datatype. 

      labels = ["Monday log", "Tuesday Log", "Wednesday Log"]

- **colors** : `list` datatype. Each entry in the labels list picks a color for the output groups in the created plot, in order. If `None`, a set of discrete colors in the same order will be used. Each entry of this list is either a `str` describing one of the [matplotlib named colors](https://matplotlib.org/stable/gallery/color/named_colors.html), or is an (r, g, b) triplet with values between [0-1] representing brightness on a scaled (0-255) range.

      colors = ["black", "darkslateblue", (1, 0.5, 0)]

- **plot** : `matplotlib.axes._subplots.AxesSubplot` datatype. Each graphing function returns an instance of this plot object. Passing None creates a new figure. Passing an instance of a plot will keep all old data on the plot, and add the newly plotted data on top. Typically used to overlay two data sets with different column names.

      plot = plot_scatter(gc_event_dataframes)
      plot = plot_line(gc_event_dataframes, group_by = "EventNames")

- **column** : `str` datatype. The name of a column found in the list of `gc event logs`, representing the Y coordinate of data to plot. If `None` is passed, the default value for this parameter is `"Duration_milliseconds"`. 

      column = "Duration_milliseconds"

- **interval_duration** : `float` or `int` datatype. The duration in seconds for grouping of times. For this function, that would be the size of each grouping on the histogram

      interval_duration = 3600 # 1 hour
      interval_duration = 1.5  # 1.5 seconds

- **column_timing** :`str` datatype. The name of a column found in the list of `gc event logs`, representing the X coordinate of the data to plot. If `None` is passed, the default value for this parameter is `"TimeFromStart_seconds"`. 
      
      column_timing = "TimeFromStart_seconds"

---


## 20. Number of times GC invoked over time intervals
Uses the function `plot_frequency_of_gc_intervals()`. The parameters are listed below for the functions, with the expected values to create the plot described by `17. Number of times GC invoked over time intervals` being described in paranthesis. The only required parameter is `gc_event_dataframes`.
    
    gc_event_dataframes (required)
    group_by            (Expected = None) 
    filter_by           (Expected = pauses_only)
    labels              (Expected = labels variable)
    colors              (Expected = None)
    plot                (Expected = None)
    column              (Expected = "GCIndex")
    interval_duration   (Expected = 60) # any positive integer or float
    column_timing       (Expected = None)

Note: a `gc event log` is a pandas dataframe, containing labeled columns to describe fields in a recorded event, and each row representing a discerete event. A list of `gc event logs` are returned from the function `get_gc_event_tables()` in `read_log_file.py`, which is used to automatically parse log files. 

`plot_frequency_of_gc_intervals()` parameters:

- **gc_event_dataframes**: `list` datatype. Each list entry is expected to be a `gc event log`. The `gc event logs` in the list will be parsed for the columns described by the parameters `column` and `column_timing` for Y and X data respectively, after filters have been applied.

- **group_by**: `str` datatype. Name of a column present in the `gc event logs`. If this parameter is provided, groups all repeated values from the specified column, such that every group has the same value in column '`group_by`'. Leaving this optional parameter as `None` defaults to creating 1 group per `gc event log` in the `gc_event_dataframes` list. Examples below

      group_by = "EventName"
      group_by = "EventType"

- **filter_by** : `function` datatype. A boolean function to be applied to each row of each `gc event log`. If the function evaluates to false, then that event will not be included in the resulting plot. A typical function first checks if the column exists before checking any values, as seen in the example below. If this check is not in place, a `KeyError` may be thrown.
        
      def pauses_only(row):
           if "EventType" in row:
               if row["EventType] == "Pause":
                   return True
       return False
        
       filter_by = pauses_only

- **labels** : `list` datatype. Each entry in the labels list describes the data in `gc_event_dataframes`, in order. Each entry in the labels list should be a `str` datatype. 

      labels = ["Monday log", "Tuesday Log", "Wednesday Log"]

- **colors** : `list` datatype. Each entry in the labels list picks a color for the output groups in the created plot, in order. If `None`, a set of discrete colors in the same order will be used. Each entry of this list is either a `str` describing one of the [matplotlib named colors](https://matplotlib.org/stable/gallery/color/named_colors.html), or is an (r, g, b) triplet with values between [0-1] representing brightness on a scaled (0-255) range.

      colors = ["black", "darkslateblue", (1, 0.5, 0)]

- **plot** : `matplotlib.axes._subplots.AxesSubplot` datatype. Each graphing function returns an instance of this plot object. Passing None creates a new figure. Passing an instance of a plot will keep all old data on the plot, and add the newly plotted data on top. Typically used to overlay two data sets with different column names.

      plot = plot_scatter(gc_event_dataframes)
      plot = plot_line(gc_event_dataframes, group_by = "EventNames")

- **column** : `str` datatype. The name of a column found in the list of `gc event logs`, representing the Y coordinate of data to plot. If `None` is passed, the default value for this parameter is `"Duration_milliseconds"`. 

      column = "Duration_milliseconds"

- **interval_duration** : `float` or `int` datatype. The duration in seconds for grouping of times. For this function, that would be the period of time in which the gc events are summed

      interval_duration = 3600 # 1 hour
      interval_duration = 1.5  # 1.5 seconds

- **column_timing** :`str` datatype. The name of a column found in the list of `gc event logs`, representing the X coordinate of the data to plot. If `None` is passed, the default value for this parameter is `"TimeFromStart_seconds"`. 
      
      column_timing = "TimeFromStart_seconds"

