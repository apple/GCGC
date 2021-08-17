# Notebook function documentation

List of functions and the plots they are expected to produce. For each of the provided GCGC original plots, the suggested parameters will be provided.


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

## 1a. STW pauses during program runtime, linear

Uses the function `plot_scatter()`. This function is interchangeable with the function `plot_line()` if a line plot is desired, with the same parameters for each function. The parameters are listed below for the functions, with the expected values to create the plot described by `1a. STW pauses during program runtime, linear` being described in paranthesis. The only required parameter is `gc_event_dataframes` 
    
    gc_event_dataframes (required)
    group_by            (Expected = None) 
    filter_by           (Expected = pauses_only)
    labels              (Expected = labels variable)
    colors              (Expected = None)
    plot                (Expected = None)
    column              (Expected = None)
    column_timing       (Expected = None)

Note: a `gc event log` is a pandas dataframe, containing labeled columns to describe fields in a recorded event, and rows with values describing discrete events. a list of `gc event log`s are returned from thefunction `get_gc_event_tables()` in `read_log_file.py`, which is used to automatically parse log files. 

`plot_scatter()` / `plot_line()` parameters:

- **gc_event_dataframes**: `list` datatype. Each list entry is expected = to be a `gc event log`. The `gc event log`s in the list will be parsed for the columns described by the parameters `column` and `column_timing` for Y and X data respectively, after filters have been applied.

- **group_by**: `str` datatype. Name of a column present in the `gc event logs`. If this parameter is provided, groups all repeated values from the specified column, such that every group has the same value in column '`group_by`'. Leaving this optional parameter as `None` then defaults to creating 1 group per `gc event log` in the `gc_event_dataframes` list. Examples below

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

- **colors** : `list` datatype. Each entry in the labels list picks a color for the output groups in the created plot, in order. If None, a set of discrete colors in the same order will be used. Each entry of this list is either a `str` describing one of the [matplotlib named colors](https://matplotlib.org/stable/gallery/color/named_colors.html), or is an (r, g, b) triplet with values between [0-1] representing brightness on a scaled (0-255) range.

      colors = ["black", "darkslateblue", (1, 0.5, 0)]

- **plot** : `matplotlib.axes._subplots.AxesSubplot` datatype. Each graphing function returns an instance of this plot object. Passing None creates a new figure. Passing an instance of a plot will keep all old data on the plot, and add the newly plotted data on top. Typically used to overlay two data sets with different column names.

      plot = plot_scatter(gc_event_dataframes)
      plot = plot_line(gc_event_dataframes, group_by = "EventNames")

- **column** : `str` datatype. The name of a column found in the list of `gc event log`s, and represents the Y coordinate of data to plot. If None is passed, the default value for this parameter is `"Duration_miliseconds"`. 

      column = "Duration_miliseconds"

- **column_timing** :`str` datatype. The name of a column found in the list of `gc event log`s, and represents the X coordinate of the data to plot. If None is passed, the default value for this parameter is `"TimeFromStart_seconds"`. 
      
      column_timing = "TimeFromStart_seconds"

---







## 1b. STW Pauses during program runtime, Logarithmic

Important: The plot generated in `1b` is the same as that generated in `1a`, but with a following modifier applied to the returned variable. 

    plot = plot_scatter(gc_event_dataframes,
                        filter_by = pauses_only,
                        labels = labels)
    plot.set_yscale("log")
    plot.yaxis.set_major_formatter(ScalarFormatter()) # optiona


Uses the function `plot_scatter()`. This function is interchangeable with the function `plot_line()` if a line plot is desired, with the same parameters for each function. The parameters are listed below for the functions, with the expected values to create the plot described by `1a. STW pauses during program runtime, linear` being described in paranthesis. The only required parameter is `gc_event_dataframes`.
    
    gc_event_dataframes (required)
    group_by            (Expected = None) 
    filter_by           (Expected = pauses_only)
    labels              (Expected = labels variable)
    colors              (Expected = None)
    plot                (Expected = None)
    column              (Expected = None)
    column_timing       (Expected = None)

Note: a `gc event log` is a pandas dataframe, containing labeled columns to describe fields in a recorded event, and rows with values describing discrete events. a list of `gc event log`s are returned from thefunction `get_gc_event_tables()` in `read_log_file.py`, which is used to automatically parse log files. 

`plot_scatter()` / `plot_line()` parameters:

- **gc_event_dataframes**: `list` datatype. Each list entry is expected = to be a `gc event log`. The `gc event log`s in the list will be parsed for the columns described by the parameters `column` and `column_timing` for Y and X data respectively, after filters have been applied.

- **group_by**: `str` datatype. Name of a column present in the `gc event logs`. If this parameter is provided, groups all repeated values from the specified column, such that every group has the same value in column '`group_by`'. Leaving this optional parameter as `None` then defaults to creating 1 group per `gc event log` in the `gc_event_dataframes` list. Examples below

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

- **colors** : `list` datatype. Each entry in the labels list picks a color for the output groups in the created plot, in order. If None, a set of discrete colors in the same order will be used. Each entry of this list is either a `str` describing one of the [matplotlib named colors](https://matplotlib.org/stable/gallery/color/named_colors.html), or is an (r, g, b) triplet with values between [0-1] representing brightness on a scaled (0-255) range.

      colors = ["black", "darkslateblue", (1, 0.5, 0)]

- **plot** : `matplotlib.axes._subplots.AxesSubplot` datatype. Each graphing function returns an instance of this plot object. Passing None creates a new figure. Passing an instance of a plot will keep all old data on the plot, and add the newly plotted data on top. Typically used to overlay two data sets with different column names.

      plot = plot_scatter(gc_event_dataframes)
      plot = plot_line(gc_event_dataframes, group_by = "EventNames")

- **column** : `str` datatype. The name of a column found in the list of `gc event log`s, and represents the Y coordinate of data to plot. If None is passed, the default value for this parameter is `"Duration_miliseconds"`. 

      column = "Duration_miliseconds"

- **column_timing** :`str` datatype. The name of a column found in the list of `gc event log`s, and represents the X coordinate of the data to plot. If None is passed, the default value for this parameter is `"TimeFromStart_seconds"`. 
      
      column_timing = "TimeFromStart_seconds"

---







## 2a. STW Pauses during program runtime, group by EventName, Linear

Uses the function `plot_scatter()`. This function is interchangeable with the function `plot_line` if a line plot is desired, with the same parameters for each function. The parameters are listed below for the functions, with the expected values to create the plot described by `2a. STW Pauses during program runtime, group by EventName, Linear` being described in paranthesis. The only required parameter is `gc_event_dataframes`.
    
    gc_event_dataframes (required)
    group_by            (Expected = "EventName") 
    filter_by           (Expected = pauses_only)
    labels              (Expected = labels variable)
    colors              (Expected = None)
    plot                (Expected = None)
    column              (Expected = None)
    column_timing       (Expected = None)

Note: a `gc event log` is a pandas dataframe, containing labeled columns to describe fields in a recorded event, and rows with values describing discrete events. a list of `gc event log`s are returned from thefunction `get_gc_event_tables()` in `read_log_file.py`, which is used to automatically parse log files. 

`plot_scatter()` / `plot_line()` parameters:

- **gc_event_dataframes**: `list` datatype. Each list entry is expected = to be a `gc event log`. The `gc event log`s in the list will be parsed for the columns described by the parameters `column` and `column_timing` for Y and X data respectively, after filters have been applied.

- **group_by**: `str` datatype. Name of a column present in the `gc event logs`. If this parameter is provided, groups all repeated values from the specified column, such that every group has the same value in column '`group_by`'. Leaving this optional parameter as `None` then defaults to creating 1 group per `gc event log` in the `gc_event_dataframes` list. Examples below

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

- **colors** : `list` datatype. Each entry in the labels list picks a color for the output groups in the created plot, in order. If None, a set of discrete colors in the same order will be used. Each entry of this list is either a `str` describing one of the [matplotlib named colors](https://matplotlib.org/stable/gallery/color/named_colors.html), or is an (r, g, b) triplet with values between [0-1] representing brightness on a scaled (0-255) range.

      colors = ["black", "darkslateblue", (1, 0.5, 0)]

- **plot** : `matplotlib.axes._subplots.AxesSubplot` datatype. Each graphing function returns an instance of this plot object. Passing None creates a new figure. Passing an instance of a plot will keep all old data on the plot, and add the newly plotted data on top. Typically used to overlay two data sets with different column names.

      plot = plot_scatter(gc_event_dataframes)
      plot = plot_line(gc_event_dataframes, group_by = "EventNames")

- **column** : `str` datatype. The name of a column found in the list of `gc event log`s, and represents the Y coordinate of data to plot. If None is passed, the default value for this parameter is `"Duration_miliseconds"`. 

      column = "Duration_miliseconds"

- **column_timing** :`str` datatype. The name of a column found in the list of `gc event log`s, and represents the X coordinate of the data to plot. If None is passed, the default value for this parameter is `"TimeFromStart_seconds"`. 
      
      column_timing = "TimeFromStart_seconds"


---







## 2b. STW Pauses during program runtime, group by AdditionalEventInfo, Logarithmic

Important: The plot generated in `2b` is the same as that generated in `2a`, but with a following modifier applied to the returned variable. 

    plot = plot_scatter(gc_event_dataframes,
                        group_by = "AdditionalEventInfo",
                        filter_by = pauses_only,
                        labels = labels)
    plot.set_yscale("log")
    plot.yaxis.set_major_formatter(ScalarFormatter()) # optiona

Uses the function `plot_scatter()`. This function is interchangeable with the function `plot_line` if a line plot is desired, with the same parameters for each function. The parameters are listed below for the functions, with the expected values to create the plot described by `2b. STW Pauses during program runtime, group by AdditionalEventInfo, Logarithmic` being described in paranthesis. The only required parameter is `gc_event_dataframes`.
    
    gc_event_dataframes (required)
    group_by            (Expected = "EventName") 
    filter_by           (Expected = pauses_only)
    labels              (Expected = labels variable)
    colors              (Expected = None)
    plot                (Expected = None)
    column              (Expected = None)
    column_timing       (Expected = None)

Note: a `gc event log` is a pandas dataframe, containing labeled columns to describe fields in a recorded event, and rows with values describing discrete events. a list of `gc event log`s are returned from thefunction `get_gc_event_tables()` in `read_log_file.py`, which is used to automatically parse log files. 

`plot_scatter()` / `plot_line()` parameters:

- **gc_event_dataframes**: `list` datatype. Each list entry is expected = to be a `gc event log`. The `gc event log`s in the list will be parsed for the columns described by the parameters `column` and `column_timing` for Y and X data respectively, after filters have been applied.

- **group_by**: `str` datatype. Name of a column present in the `gc event logs`. If this parameter is provided, groups all repeated values from the specified column, such that every group has the same value in column '`group_by`'. Leaving this optional parameter as `None` then defaults to creating 1 group per `gc event log` in the `gc_event_dataframes` list. Examples below

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

- **colors** : `list` datatype. Each entry in the labels list picks a color for the output groups in the created plot, in order. If None, a set of discrete colors in the same order will be used. Each entry of this list is either a `str` describing one of the [matplotlib named colors](https://matplotlib.org/stable/gallery/color/named_colors.html), or is an (r, g, b) triplet with values between [0-1] representing brightness on a scaled (0-255) range.

      colors = ["black", "darkslateblue", (1, 0.5, 0)]

- **plot** : `matplotlib.axes._subplots.AxesSubplot` datatype. Each graphing function returns an instance of this plot object. Passing None creates a new figure. Passing an instance of a plot will keep all old data on the plot, and add the newly plotted data on top. Typically used to overlay two data sets with different column names.

      plot = plot_scatter(gc_event_dataframes)
      plot = plot_line(gc_event_dataframes, group_by = "EventNames")

- **column** : `str` datatype. The name of a column found in the list of `gc event log`s, and represents the Y coordinate of data to plot. If None is passed, the default value for this parameter is `"Duration_miliseconds"`. 

      column = "Duration_miliseconds"

- **column_timing** :`str` datatype. The name of a column found in the list of `gc event log`s, and represents the X coordinate of the data to plot. If None is passed, the default value for this parameter is `"TimeFromStart_seconds"`. 
      
      column_timing = "TimeFromStart_seconds"


---








## 3. Concurrent durations during runtime

Uses the function `plot_scatter()`. This function is interchangeable with the function `plot_line` if a line plot is desired, with the same parameters for each function. The parameters are listed below for the functions, with the expected values to create the plot described by `3. Concurrent durations during runtime` being described in paranthesis. The only required parameter is `gc_event_dataframes`.
    
    gc_event_dataframes (required)
    group_by            (Expected = None) 
    filter_by           (Expected = concurrent_only)
    labels              (Expected = labels variable)
    colors              (Expected = None)
    plot                (Expected = None)
    column              (Expected = None)
    column_timing       (Expected = None)

Note: a `gc event log` is a pandas dataframe, containing labeled columns to describe fields in a recorded event, and rows with values describing discrete events. a list of `gc event log`s are returned from thefunction `get_gc_event_tables()` in `read_log_file.py`, which is used to automatically parse log files. 

`plot_scatter()` / `plot_line()` parameters:

- **gc_event_dataframes**: `list` datatype. Each list entry is expected = to be a `gc event log`. The `gc event log`s in the list will be parsed for the columns described by the parameters `column` and `column_timing` for Y and X data respectively, after filters have been applied.

- **group_by**: `str` datatype. Name of a column present in the `gc event logs`. If this parameter is provided, groups all repeated values from the specified column, such that every group has the same value in column '`group_by`'. Leaving this optional parameter as `None` then defaults to creating 1 group per `gc event log` in the `gc_event_dataframes` list. Examples below

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

- **colors** : `list` datatype. Each entry in the labels list picks a color for the output groups in the created plot, in order. If None, a set of discrete colors in the same order will be used. Each entry of this list is either a `str` describing one of the [matplotlib named colors](https://matplotlib.org/stable/gallery/color/named_colors.html), or is an (r, g, b) triplet with values between [0-1] representing brightness on a scaled (0-255) range.

      colors = ["black", "darkslateblue", (1, 0.5, 0)]

- **plot** : `matplotlib.axes._subplots.AxesSubplot` datatype. Each graphing function returns an instance of this plot object. Passing None creates a new figure. Passing an instance of a plot will keep all old data on the plot, and add the newly plotted data on top. Typically used to overlay two data sets with different column names.

      plot = plot_scatter(gc_event_dataframes)
      plot = plot_line(gc_event_dataframes, group_by = "EventNames")

- **column** : `str` datatype. The name of a column found in the list of `gc event log`s, and represents the Y coordinate of data to plot. If None is passed, the default value for this parameter is `"Duration_miliseconds"`. 

      column = "Duration_miliseconds"

- **column_timing** :`str` datatype. The name of a column found in the list of `gc event log`s, and represents the X coordinate of the data to plot. If None is passed, the default value for this parameter is `"TimeFromStart_seconds"`. 
      
      column_timing = "TimeFromStart_seconds"

---








## 4. Total time spent in STW pauses vs. Concurrent durations

Uses the function `plot_bar_sum()`. The parameters are listed below for the functions, with the expected values to create the plot described by `4. Total time spent in STW pauses vs. Concurrent durations` being described in paranthesis. The only required parameter is `gc_event_dataframes`.

    gc_event_dataframes (required)
    group_by            (Expected = "EventType") 
    filter_by           (Expected = duration_present)
    labels              (Expected = labels variable)
    colors              (Expected = None)
    plot                (Expected = None)
    column              (Expected = None)
    column_timing       (Expected = None)

Note: a `gc event log` is a pandas dataframe, containing labeled columns to describe fields in a recorded event, and rows with values describing discrete events. a list of `gc event log`s are returned from thefunction `get_gc_event_tables()` in `read_log_file.py`, which is used to automatically parse log files. 

`plot_bar_sum()` parameters:

- **gc_event_dataframes**: `list` datatype. Each list entry is expected = to be a `gc event log`. The `gc event log`s in the list will be parsed for the columns described by the parameters `column` and `column_timing` for Y and X data respectively, after filters have been applied.

- **group_by**: `str` datatype. Name of a column present in the `gc event logs`. If this parameter is provided, groups all repeated values from the specified column, such that every group has the same value in column '`group_by`'. Leaving this optional parameter as `None` then defaults to creating 1 group per `gc event log` in the `gc_event_dataframes` list. Examples below

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

- **colors** : `list` datatype. Each entry in the labels list picks a color for the output groups in the created plot, in order. If None, a set of discrete colors in the same order will be used. Each entry of this list is either a `str` describing one of the [matplotlib named colors](https://matplotlib.org/stable/gallery/color/named_colors.html), or is an (r, g, b) triplet with values between [0-1] representing brightness on a scaled (0-255) range.

      colors = ["black", "darkslateblue", (1, 0.5, 0)]

- **plot** : `matplotlib.axes._subplots.AxesSubplot` datatype. Each graphing function returns an instance of this plot object. Passing None creates a new figure. Passing an instance of a plot will keep all old data on the plot, and add the newly plotted data on top. Typically used to overlay two data sets with different column names.

      plot = plot_scatter(gc_event_dataframes)
      plot = plot_line(gc_event_dataframes, group_by = "EventNames")

- **column** : `str` datatype. The name of a column found in the list of `gc event log`s, and represents the Y coordinate of data to plot. If None is passed, the default value for this parameter is `"Duration_miliseconds"`. 

      column = "Duration_miliseconds"

- **column_timing** :`str` datatype. The name of a column found in the list of `gc event log`s, and represents the X coordinate of the data to plot. If None is passed, the default value for this parameter is `"TimeFromStart_seconds"`. 
      
      column_timing = "TimeFromStart_seconds"

---








## 5a. Pauses trends (max, sum, mean, count, std.dev)
Uses the function `plot_trends()`. The parameters are listed below for the functions, with the expected values to create the plot described by `5a. Pauses trends (max, sum, mean, count, std.dev)` being described in paranthesis. The only required parameter is `gc_event_dataframes`.

    gc_event_dataframes (required)
    group_by            (Expected = None) 
    filter_by           (Expected = pauses_only)
    labels              (Expected = labels variable)
    column              (Expected = None)
    throughput          (Expected = True)

Note: a `gc event log` is a pandas dataframe, containing labeled columns to describe fields in a recorded event, and rows with values describing discrete events. a list of `gc event log`s are returned from thefunction `get_gc_event_tables()` in `read_log_file.py`, which is used to automatically parse log files. 

`plot_trends()` parameters:

- **gc_event_dataframes**: `list` datatype. Each list entry is expected = to be a `gc event log`. The `gc event log`s in the list will be parsed for the columns described by the parameters `column` and `column_timing` for Y and X data respectively, after filters have been applied.

- **group_by**: `str` datatype. Name of a column present in the `gc event logs`. If this parameter is provided, groups all repeated values from the specified column, such that every group has the same value in column '`group_by`'. Leaving this optional parameter as `None` then defaults to creating 1 group per `gc event log` in the `gc_event_dataframes` list. Examples below

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

- **column** : `str` datatype. The name of a column found in the list of `gc event log`s, and represents the Y coordinate of data to plot. If None is passed, the default value for this parameter is `"Duration_miliseconds"`. 

- **throughput** : `bool` datatype. If True, uses the provided timing information to attempt to calculate a throughput (time spent in program execution) / (total program time) * 100. Typically an illogical metric unless each group is all pauses from 1 file.

---







## 5b. Pauses trends by name

Uses the function `plot_trends()`. The parameters are listed below for the functions, with the expected values to create the plot described by `5b. Pauses trends by name` being described in paranthesis. The only required parameter is `gc_event_dataframes`.

    gc_event_dataframes (required)
    group_by            (Expected = "EventName") 
    filter_by           (Expected = pauses_only)
    labels              (Expected = labels variable)
    column              (Expected = None)
    throughput          (Expected = False)

Note: a `gc event log` is a pandas dataframe, containing labeled columns to describe fields in a recorded event, and rows with values describing discrete events. a list of `gc event log`s are returned from thefunction `get_gc_event_tables()` in `read_log_file.py`, which is used to automatically parse log files. 

`plot_trends()` parameters:

- **gc_event_dataframes**: `list` datatype. Each list entry is expected = to be a `gc event log`. The `gc event log`s in the list will be parsed for the columns described by the parameters `column` and `column_timing` for Y and X data respectively, after filters have been applied.

- **group_by**: `str` datatype. Name of a column present in the `gc event logs`. If this parameter is provided, groups all repeated values from the specified column, such that every group has the same value in column '`group_by`'. Leaving this optional parameter as `None` then defaults to creating 1 group per `gc event log` in the `gc_event_dataframes` list. Examples below

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

- **column** : `str` datatype. The name of a column found in the list of `gc event log`s, and represents the Y coordinate of data to plot. If None is passed, the default value for this parameter is `"Duration_miliseconds"`. 

- **throughput** : `bool` datatype. If True, uses the provided timing information to attempt to calculate a throughput (time spent in program execution) / (total program time) * 100. Typically an illogical metric unless each group is all pauses from 1 file.


---







## 6a. Pause percentiles
Uses the function `plot_percentiles()`. The parameters are listed below for the functions, with the expected values to create the plot described by `6a. Pause percentiles` being described in paranthesis. The only required parameter is `gc_event_dataframes`.

    gc_event_dataframes (required)
    group_by            (Expected = None) 
    filter_by           (Expected = pauses_only)
    labels              (Expected = labels variable)
    column              (Expected = None)

Note: a `gc event log` is a pandas dataframe, containing labeled columns to describe fields in a recorded event, and rows with values describing discrete events. a list of `gc event log`s are returned from thefunction `get_gc_event_tables()` in `read_log_file.py`, which is used to automatically parse log files. 

`plot_percentiles()` parameters:

- **gc_event_dataframes**: `list` datatype. Each list entry is expected = to be a `gc event log`. The `gc event log`s in the list will be parsed for the columns described by the parameters `column` and `column_timing` for Y and X data respectively, after filters have been applied.

- **group_by**: `str` datatype. Name of a column present in the `gc event logs`. If this parameter is provided, groups all repeated values from the specified column, such that every group has the same value in column '`group_by`'. Leaving this optional parameter as `None` then defaults to creating 1 group per `gc event log` in the `gc_event_dataframes` list. Examples below

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

- **column** : `str` datatype. The name of a column found in the list of `gc event log`s, and represents the Y coordinate of data to plot. If None is passed, the default value for this parameter is `"Duration_miliseconds"`. 

---







## 6b. Pause percentiles by name

Uses the function `plot_percentiles()`. The parameters are listed below for the functions, with the expected values to create the plot described by `6b. Pause percentiles by name` being described in paranthesis. The only required parameter is `gc_event_dataframes`.

    gc_event_dataframes (required)
    group_by            (Expected = "EventName") 
    filter_by           (Expected = pauses_only)
    labels              (Expected = labels variable)
    column              (Expected = None)

Note: a `gc event log` is a pandas dataframe, containing labeled columns to describe fields in a recorded event, and rows with values describing discrete events. a list of `gc event log`s are returned from thefunction `get_gc_event_tables()` in `read_log_file.py`, which is used to automatically parse log files. 

`plot_bar_sum()` parameters:

- **gc_event_dataframes**: `list` datatype. Each list entry is expected = to be a `gc event log`. The `gc event log`s in the list will be parsed for the columns described by the parameters `column` and `column_timing` for Y and X data respectively, after filters have been applied.

- **group_by**: `str` datatype. Name of a column present in the `gc event logs`. If this parameter is provided, groups all repeated values from the specified column, such that every group has the same value in column '`group_by`'. Leaving this optional parameter as `None` then defaults to creating 1 group per `gc event log` in the `gc_event_dataframes` list. Examples below

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

- **column** : `str` datatype. The name of a column found in the list of `gc event log`s, and represents the Y coordinate of data to plot. If None is passed, the default value for this parameter is `"Duration_miliseconds"`. 

---










## 7a. Mean event durations


Uses the function `plot_bar_sum()`. The parameters are listed below for the functions, with the expected values to create the plot described by `7a. Mean event durations` being described in paranthesis. The only required parameter is `gc_event_dataframes`.
    
    gc_event_dataframes (required)
    group_by            (Expected = "EventType") 
    filter_by           (Expected = concurrent_or_pauses)
    labels              (Expected = labels variable)
    colors              (Expected = None)
    plot                (Expected = None)
    column              (Expected = None)
    column_timing       (Expected = None)

Note: a `gc event log` is a pandas dataframe, containing labeled columns to describe fields in a recorded event, and rows with values describing discrete events. a list of `gc event log`s are returned from thefunction `get_gc_event_tables()` in `read_log_file.py`, which is used to automatically parse log files. 

`plot_bar_sum()` parameters:

- **gc_event_dataframes**: `list` datatype. Each list entry is expected = to be a `gc event log`. The `gc event log`s in the list will be parsed for the columns described by the parameters `column` and `column_timing` for Y and X data respectively, after filters have been applied.

- **group_by**: `str` datatype. Name of a column present in the `gc event logs`. If this parameter is provided, groups all repeated values from the specified column, such that every group has the same value in column '`group_by`'. Leaving this optional parameter as `None` then defaults to creating 1 group per `gc event log` in the `gc_event_dataframes` list. Examples below

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

- **colors** : `list` datatype. Each entry in the labels list picks a color for the output groups in the created plot, in order. If None, a set of discrete colors in the same order will be used. Each entry of this list is either a `str` describing one of the [matplotlib named colors](https://matplotlib.org/stable/gallery/color/named_colors.html), or is an (r, g, b) triplet with values between [0-1] representing brightness on a scaled (0-255) range.

      colors = ["black", "darkslateblue", (1, 0.5, 0)]

- **plot** : `matplotlib.axes._subplots.AxesSubplot` datatype. Each graphing function returns an instance of this plot object. Passing None creates a new figure. Passing an instance of a plot will keep all old data on the plot, and add the newly plotted data on top. Typically used to overlay two data sets with different column names.

      plot = plot_scatter(gc_event_dataframes)
      plot = plot_line(gc_event_dataframes, group_by = "EventNames")

- **column** : `str` datatype. The name of a column found in the list of `gc event log`s, and represents the Y coordinate of data to plot. If None is passed, the default value for this parameter is `"Duration_miliseconds"`. 

      column = "Duration_miliseconds"

- **column_timing** :`str` datatype. The name of a column found in the list of `gc event log`s, and represents the X coordinate of the data to plot. If None is passed, the default value for this parameter is `"TimeFromStart_seconds"`. 
      
      column_timing = "TimeFromStart_seconds"

---







## 7b. Sum event durations

Uses the function `plot_bar_avg()`. The parameters are listed below for the functions, with the expected values to create the plot described by `7a. Mean event durations` being described in paranthesis. The only required parameter is `gc_event_dataframes`.
    
    gc_event_dataframes (required)
    group_by            (Expected = "EventType") 
    filter_by           (Expected = concurrent_or_pauses)
    labels              (Expected = labels variable)
    colors              (Expected = None)
    plot                (Expected = None)
    column              (Expected = None)
    column_timing       (Expected = None)

Note: a `gc event log` is a pandas dataframe, containing labeled columns to describe fields in a recorded event, and rows with values describing discrete events. a list of `gc event log`s are returned from thefunction `get_gc_event_tables()` in `read_log_file.py`, which is used to automatically parse log files. 

`plot_bar_avg()` parameters:

- **gc_event_dataframes**: `list` datatype. Each list entry is expected = to be a `gc event log`. The `gc event log`s in the list will be parsed for the columns described by the parameters `column` and `column_timing` for Y and X data respectively, after filters have been applied.

- **group_by**: `str` datatype. Name of a column present in the `gc event logs`. If this parameter is provided, groups all repeated values from the specified column, such that every group has the same value in column '`group_by`'. Leaving this optional parameter as `None` then defaults to creating 1 group per `gc event log` in the `gc_event_dataframes` list. Examples below

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

- **colors** : `list` datatype. Each entry in the labels list picks a color for the output groups in the created plot, in order. If None, a set of discrete colors in the same order will be used. Each entry of this list is either a `str` describing one of the [matplotlib named colors](https://matplotlib.org/stable/gallery/color/named_colors.html), or is an (r, g, b) triplet with values between [0-1] representing brightness on a scaled (0-255) range.

      colors = ["black", "darkslateblue", (1, 0.5, 0)]

- **plot** : `matplotlib.axes._subplots.AxesSubplot` datatype. Each graphing function returns an instance of this plot object. Passing None creates a new figure. Passing an instance of a plot will keep all old data on the plot, and add the newly plotted data on top. Typically used to overlay two data sets with different column names.

      plot = plot_scatter(gc_event_dataframes)
      plot = plot_line(gc_event_dataframes, group_by = "EventNames")

- **column** : `str` datatype. The name of a column found in the list of `gc event log`s, and represents the Y coordinate of data to plot. If None is passed, the default value for this parameter is `"Duration_miliseconds"`. 

      column = "Duration_miliseconds"

- **column_timing** :`str` datatype. The name of a column found in the list of `gc event log`s, and represents the X coordinate of the data to plot. If None is passed, the default value for this parameter is `"TimeFromStart_seconds"`. 
      
      column_timing = "TimeFromStart_seconds"

---








## 8a. Heap Before GC 

Uses the function `plot_line()`. This function is interchangeable with the function `plot_scatter()` if a line plot is desired, with the same parameters for each function. The parameters are listed below for the functions, with the expected values to create the plot described by `2a. STW Pauses during program runtime, group by EventName, Linear` being described in paranthesis. The only required parameter is `gc_event_dataframes`.
    
    gc_event_dataframes (required)
    group_by            (Expected = "EventName") 
    filter_by           (Expected = pauses_only)
    labels              (Expected = labels variable)
    colors              (Expected = None)
    plot                (Expected = None)
    column              (Expected = None)
    column_timing       (Expected = None)

Note: a `gc event log` is a pandas dataframe, containing labeled columns to describe fields in a recorded event, and rows with values describing discrete events. a list of `gc event log`s are returned from thefunction `get_gc_event_tables()` in `read_log_file.py`, which is used to automatically parse log files. 

`plot_scatter()` / `plot_line()` parameters:

- **gc_event_dataframes**: `list` datatype. Each list entry is expected = to be a `gc event log`. The `gc event log`s in the list will be parsed for the columns described by the parameters `column` and `column_timing` for Y and X data respectively, after filters have been applied.

- **group_by**: `str` datatype. Name of a column present in the `gc event logs`. If this parameter is provided, groups all repeated values from the specified column, such that every group has the same value in column '`group_by`'. Leaving this optional parameter as `None` then defaults to creating 1 group per `gc event log` in the `gc_event_dataframes` list. Examples below

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

- **colors** : `list` datatype. Each entry in the labels list picks a color for the output groups in the created plot, in order. If None, a set of discrete colors in the same order will be used. Each entry of this list is either a `str` describing one of the [matplotlib named colors](https://matplotlib.org/stable/gallery/color/named_colors.html), or is an (r, g, b) triplet with values between [0-1] representing brightness on a scaled (0-255) range.

      colors = ["black", "darkslateblue", (1, 0.5, 0)]

- **plot** : `matplotlib.axes._subplots.AxesSubplot` datatype. Each graphing function returns an instance of this plot object. Passing None creates a new figure. Passing an instance of a plot will keep all old data on the plot, and add the newly plotted data on top. Typically used to overlay two data sets with different column names.

      plot = plot_scatter(gc_event_dataframes)
      plot = plot_line(gc_event_dataframes, group_by = "EventNames")

- **column** : `str` datatype. The name of a column found in the list of `gc event log`s, and represents the Y coordinate of data to plot. If None is passed, the default value for this parameter is `"Duration_miliseconds"`. 

      column = "Duration_miliseconds"

- **column_timing** :`str` datatype. The name of a column found in the list of `gc event log`s, and represents the X coordinate of the data to plot. If None is passed, the default value for this parameter is `"TimeFromStart_seconds"`. 
      
      column_timing = "TimeFromStart_seconds"
---







## 8b. Heap After GC

Uses the function `plot_line()`. This function is interchangeable with the function `plot_scatter()` if a line plot is desired, with the same parameters for each function. The parameters are listed below for the functions, with the expected values to create the plot described by `8b. Heap After GC` being described in paranthesis. The only required parameter is `gc_event_dataframes`.
    
    gc_event_dataframes (required)
    group_by            (Expected = "EventName") 
    filter_by           (Expected = pauses_only)
    labels              (Expected = labels variable)
    colors              (Expected = None)
    plot                (Expected = None)
    column              (Expected = None)
    column_timing       (Expected = None)

Note: a `gc event log` is a pandas dataframe, containing labeled columns to describe fields in a recorded event, and rows with values describing discrete events. a list of `gc event log`s are returned from thefunction `get_gc_event_tables()` in `read_log_file.py`, which is used to automatically parse log files. 

`plot_scatter()` / `plot_line()` parameters:

- **gc_event_dataframes**: `list` datatype. Each list entry is expected = to be a `gc event log`. The `gc event log`s in the list will be parsed for the columns described by the parameters `column` and `column_timing` for Y and X data respectively, after filters have been applied.

- **group_by**: `str` datatype. Name of a column present in the `gc event logs`. If this parameter is provided, groups all repeated values from the specified column, such that every group has the same value in column '`group_by`'. Leaving this optional parameter as `None` then defaults to creating 1 group per `gc event log` in the `gc_event_dataframes` list. Examples below

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

- **colors** : `list` datatype. Each entry in the labels list picks a color for the output groups in the created plot, in order. If None, a set of discrete colors in the same order will be used. Each entry of this list is either a `str` describing one of the [matplotlib named colors](https://matplotlib.org/stable/gallery/color/named_colors.html), or is an (r, g, b) triplet with values between [0-1] representing brightness on a scaled (0-255) range.

      colors = ["black", "darkslateblue", (1, 0.5, 0)]

- **plot** : `matplotlib.axes._subplots.AxesSubplot` datatype. Each graphing function returns an instance of this plot object. Passing None creates a new figure. Passing an instance of a plot will keep all old data on the plot, and add the newly plotted data on top. Typically used to overlay two data sets with different column names.

      plot = plot_scatter(gc_event_dataframes)
      plot = plot_line(gc_event_dataframes, group_by = "EventNames")

- **column** : `str` datatype. The name of a column found in the list of `gc event log`s, and represents the Y coordinate of data to plot. If None is passed, the default value for this parameter is `"Duration_miliseconds"`. 

      column = "Duration_miliseconds"

- **column_timing** :`str` datatype. The name of a column found in the list of `gc event log`s, and represents the X coordinate of the data to plot. If None is passed, the default value for this parameter is `"TimeFromStart_seconds"`. 
      
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

Note: a `gc event log` is a pandas dataframe, containing labeled columns to describe fields in a recorded event, and rows with values describing discrete events. a list of `gc event log`s are returned from thefunction `get_gc_event_tables()` in `read_log_file.py`, which is used to automatically parse log files. 

`plot_reclaimed_bytes()` parameters:

- **gc_event_dataframes**: `list` datatype. Each list entry is expected = to be a `gc event log`. The `gc event log`s in the list will be parsed for the columns described by the parameters `column` and `column_timing` for Y and X data respectively, after filters have been applied.

- **group_by**: `str` datatype. Name of a column present in the `gc event logs`. If this parameter is provided, groups all repeated values from the specified column, such that every group has the same value in column '`group_by`'. Leaving this optional parameter as `None` then defaults to creating 1 group per `gc event log` in the `gc_event_dataframes` list. Examples below

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

- **colors** : `list` datatype. Each entry in the labels list picks a color for the output groups in the created plot, in order. If None, a set of discrete colors in the same order will be used. Each entry of this list is either a `str` describing one of the [matplotlib named colors](https://matplotlib.org/stable/gallery/color/named_colors.html), or is an (r, g, b) triplet with values between [0-1] representing brightness on a scaled (0-255) range.

      colors = ["black", "darkslateblue", (1, 0.5, 0)]

- **plot** : `matplotlib.axes._subplots.AxesSubplot` datatype. Each graphing function returns an instance of this plot object. Passing None creates a new figure. Passing an instance of a plot will keep all old data on the plot, and add the newly plotted data on top. Typically used to overlay two data sets with different column names.

      plot = plot_scatter(gc_event_dataframes)
      plot = plot_line(gc_event_dataframes, group_by = "EventNames")


- **column_timing** :`str` datatype. The name of a column found in the list of `gc event log`s, and represents the X coordinate of the data to plot. If None is passed, the default value for this parameter is `"TimeFromStart_seconds"`. 

---








## 10. Latency Heatmaps, Linear

Uses the function `plot_heatmap()`. The parameters are listed below for the functions, with the expected values to create the plot described by `10. Latency Heatmaps, Linear` being described in paranthesis. There are TWO required parameters: both `gc_event_dataframes`, and `dimensions` are needed for this function.
    
    gc_event_dataframes (required)
    dimensions (Expected = [ 20,  15, 60, 10 ]) 
                                    ### 20 x axis columns
                                    ### 15 y column rows
                                    ### 60 seconds == 1 minute intervals
                                    ### 10 milisecond pause buckets 
    group_by            (Expected = None) 
    filter_by           (Expected = pauses_only)]
    labels              (Expected = labels variable)
    column              (Expected = None)
    column_timing       (Expected = None)
    frequency_ticks     (Expected = True/False)

Note: a `gc event log` is a pandas dataframe, containing labeled columns to describe fields in a recorded event, and rows with values describing discrete events. a list of `gc event log`s are returned from thefunction `get_gc_event_tables()` in `read_log_file.py`, which is used to automatically parse log files. 

`plot_heatmap()` parameters:

- **gc_event_dataframes**: `list` datatype. Each list entry is expected = to be a `gc event log`. The `gc event log`s in the list will be parsed for the columns described by the parameters `column` and `column_timing` for Y and X data respectively, after filters have been applied.

- **-dimensions**-: a 4 length list, with the following values contained within the list
    - dimensions[0] = number of x intervals, or number of columns in the heat map
    - dimensions[1] = number of y intervals, or number of rows in the heat map
    - dimensions[2] = duration of a single x interval in seconds, or time duration of each column on the heatmap
    - dimensions[3] = duration of a single y interval in seconds, or time duration in each row of the heatmap.


- **group_by**: `str` datatype. Name of a column present in the `gc event logs`. If this parameter is provided, groups all repeated values from the specified column, such that every group has the same value in column '`group_by`'. Leaving this optional parameter as `None` then defaults to creating 1 group per `gc event log` in the `gc_event_dataframes` list. Examples below

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


- **column** : `str` datatype. The name of a column found in the list of `gc event log`s, and represents the Y coordinate of data to plot. If None is passed, the default value for this parameter is `"Duration_miliseconds"`. 

      column = "Duration_miliseconds"

- **column_timing** :`str` datatype. The name of a column found in the list of `gc event log`s, and represents the X coordinate of the data to plot. If None is passed, the default value for this parameter is `"TimeFromStart_seconds"`. 
      
      column_timing = "TimeFromStart_seconds"

- **frequency_ticks** : `bool` datatype. If True, the heatmap prints the freuquency reported onto each non-zero cell. Default is False.

        frequency_ticks = False
        
---







## 11. Pause frequencies histogram

---








## 12. Latency percentiles over time intervals

---








## 13. Number of times GC invoked over time intervals

---








## 14. Sum of pause durations over intervals

---








## 15. Logarithmic heatmaps.* known bug where start time is always 0

---








## 16. Percentage of heap filled after GC

---








## 17. Heap allocation rate 

---









