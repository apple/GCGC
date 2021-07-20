###  To select which files to parse, list the files in the first cell. Add labels to each cell, describing the passed dataset.
--- 
```
files = [...]
labels = [...]
time_range_seconds = [...]

csv_files_to_import = [...]
csv_file_labels = [...]
```
--- 
After filling in the variables with information, you can choose `cell -> run all` in web-based Jupyter, or `run all` in VSCode from the top . This will run the complete analysis given the provided information.

---

> Default gc_event_dataframe: A gc_event_dataframe has default columns, described in the [README.md](../README.md) in the [folder](../) below this one



# Customize the Notebook output

There are many fields in the notebook that can be easily changed to view certain aspects of the data. For this explanation, we will use code cell 2 for all analysis.


The following examples are written for the **plot_scatter** function. However, these parameters are present in the following functions. Modify and update these fields to generate more specific plots. 
- plot_bar_sum
- plot_trends (Does not allow for selection of: color, plot, column_timing)
- plot_percentiles (Does not allow for selection of: color, plot, column_timing)
- plot_bar_avg
- plot_line
- plot_reclaimed_bytes (column cannot be changed.)
- plot_frequency_intervals (Also includes `interval_duration` parameter)
- plot_percentile_intervals (Also includes `percentiles` parameter)
- plot_frequency_of_gc_intervals (also includes `interval_duration` parameter)
- plot_sum_pause_intervals (Also includes `interval_duration` parameter)

>    __gc_event_dataframes__ : List of pandas dataframes. Should be the variable created in cell 1, called `gc_event_dataframes`.
---
> __group_by__ : (Default = None) Given a column name in the gc_event_dataframes, the output analysis will group all same values in that column into distinct groups. If the column is not present in a dataframe, a warning will be printed again. 
Examples below:


`group_by = "EventType"`  # Distinct groups for EventType, such as Pauses vs. Concurrent 

`group_by = "EventName" ` # Distinct groups from EventName, such as Pause Young or Pause Full.

---
> __filter_by__ : (Default = None) A list of functions to be applied to each row of each dataframe. Should return a boolean. Returning false will remove that line from the dataset.  Examples below:

`group_by = [(lambda row: row["EventType"] == "Pause")]` # Only accepts and uses rows in the table that represent pauses.

`group_by = [(lambda row: row["Duration_miliseconds"] > 100), (lambda row: row["EventType"] == "Pause)]` # Only collect pauses over 100 miliseconds for pauses

---
> __labels__ : (Default = None) A list of labels to explain each gc_event_dataframe passed in. Typically set to `labels` variable which is set in cell 1. Labels are strongly suggested, because default labels just create a numeric list numbering the logs. (1...n)

Example:
`plot_scatter(gc_event_dataframes, labels = ["G1", "ZGC"])`

---
> __colors__ : (Default = None) A list of colors from [matplotlib's colors](https://matplotlib.org/stable/gallery/color/named_colors.html), or (r,g,b) tuples, with 0 <= r,g,b <= 1. This is typically left blank, because by default, deterministic colors based on the log file orders are created and used in every analysis file.

Example: Graphing with two manually set colors. The first being red, and the second being blue (red=0, green=0, blue=1)

`plot_scatter(gc_event_dataframes, colors = ["red", (0,0,1)])`

--- 
> __plot__ : (Default = None) A plot that has been returned from a graphing function. Returning this would add the new plotted data values to an already existing plot. To plot data from two different columns in the same gc_event_dataframe, run a plotting function twice, using the returned plot as a variable. (Say, plotting transaction data from a CSV vs. MB reclaimed would require two runs.)

Example, plotting both a scatter plot and line graph on the same graph:

```
plot = plot_scatter(gc_event_dataframes, labels = labels)

plot = plot_line(gc_event_dataframes, plot = plot)
```

Example: Plotting from gc_event_dataframes, and a csv that is not included.
```
plot = plot_scatter(gc_event_dataframes, labels = labels)

plot = plot_scatter([csv_dataframe], plot = plot, column = "Transactions")
```

---

> __column__ : (Default = "Duration_miliseconds") The name of the column in the dataframe to read Y-axis values from.
Example:

`plot_scatter(gc_event_dataframes, column = "HeapBeforeGC")` # Choose a new column to plot data from. Often paired with a filter to assert that the data is present in each row.

`plot_scatter(gc_event_dataframes, column = "HeapBeforeGC", filter_by = [(lambda row: row["HeapBeforeGC"] != None)])`

---
> __column_timing__ (Default = "TimeFromStart_seconds") The name of the column to read X-axis timing values from. Note: Specifiying DateTime will interpret the column "DateTime" in the dataframe as if it were a Date-Time string using `matplotlib.dates.date2num`. The values here are expected to be floats/ints for all rows. 

`plot_scatter(gc_event_dataframes, column_timing = "DateTime")`

--- 