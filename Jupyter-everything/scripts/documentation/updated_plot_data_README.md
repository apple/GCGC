# Functions to assist with plotting data for garbage collection


> ### plot_pauses_bar
> Constructs a bar graph from the provided data. Typically time vs. pause durations
- `xdata` a list of float data for the x axis. Typically integer time stamps in seconds.
- `ydata` a list of data for the y axis. Typically STW pause durations in miliseconds. list type = float
- `axs` a [matplotlib.axes](https://matplotlib.org/stable/api/axes_api.html#subplots) object that represents a plot.
- `color` a color from [matplotlib.colors](https://matplotlib.org/stable/gallery/color/named_colors.html). If no color is provided, a random color is created. type = string
- `label` a label to describe the set of bars being plotted. If none provided, label is displayed as "No label provided". type = string


> ### compare_pauses_bar
> Compares multiple sets of data against each other on the same graph
- `timedata_lists` a list of lists of float data for the x axis. Typically the timestamps during runtime.
- `heightdata_lists` a list of lists of float data for the y axis. Typically the latency durations during runtime.
- `axs` a [matplotlib.axes](https://matplotlib.org/stable/api/axes_api.html#subplots) object that represents a plot.
- `color` a list of colors from [matplotlib.colors](https://matplotlib.org/stable/gallery/color/named_colors.html). If no color is provided, a random color is created. type = string
- `labels` a list of labels to describe the set of bars being plotted. If none provided, each label is displayed as "No label provided". type = string


> ### plot_pauses_scatter
> Constructs a scatter plot from the provided data
- `xdata` a list of float data for the x axis. Typically integer time stamps in seconds.
- `ydata` a list of data for the y axis. Typically STW pause durations in miliseconds. list type = float
- `axs` a [matplotlib.axes](https://matplotlib.org/stable/api/axes_api.html#subplots) object that represents a plot.
- `color` a color from [matplotlib.colors](https://matplotlib.org/stable/gallery/color/named_colors.html). If no color is provided, a random color is created. type = string
- `label` a label to describe the set of bars being plotted. If none provided, label is displayed as "No label provided". type = string




> ### comparrison_scatter
> Compare multiple sets of data on the same scatter plot
- `xdata_list` a list of lists of float data for the x axis. Typically the timestamps during runtime.
- `ydata_list`a list of lists of float data for the y axis. Typically the latency durations during runtime. 
- `axs` a [matplotlib.axes](https://matplotlib.org/stable/api/axes_api.html#subplots) object that represents a plot.
- `color` a list of colors from [matplotlib.colors](https://matplotlib.org/stable/gallery/color/named_colors.html). If no color is provided, a random color is created. type = string
- `labels` a list of labels to describe the set of bars being plotted. If none provided, each label is displayed as "No label provided". type = string

> ### print_percentiles
> Print a set of percentiles for latency during runtime
- `pauses_miliseconds`  List of pauses during runtime (any order)
- `print_title=True`    If true, print a title for the ascii table being created 
- `percentiles` A list of floats, for each percentile to inspect. If none provided, default are used [50, 75, 90, 95, 99, 99.9, 99.99]
- `label` a label to describe the set of bars being plotted. If none provided, label is displayed as "label". type = string

> ### compare_pauses_percentiles
> Create a table to compare latency percentiles for multiple latency lists
- `list_of_list_pauses_ms` List of list of pauses during runtime
- `percentiles` A list of floats, for each percentile to inspect. If none provided, default are used [50, 75, 90, 95, 99, 99.9, 99.99]
- `labels` a list of string labels to describe each entry in the pauses_miliseconds list. If none are provided, each label is displayed as "label". 

> ### print_trends
> Desribes trends within the data. Shows max, number of pauses, mean, and sum. Outputs an ASCII table.
- `pauses_miliseconds` List of pauses to analyze
- `label` Label for this row in the table, to explain what data has been passed in
- `print_title=True` True to print title for ASCII table output by function

> ### compare_trends
> Compares trends of latency lists. Outputs an ASCII table.
- `pauses_ms_lists` List of lists of pauses to analyze. Pauses in miliseconds
- `labels` List of string labels to describe each pause list.

> ### plot_pauses_line
- `time_seconds`
- `pauses_miliseconds`
- `axs`
- `color`
- `label`
- `optional`

> ### compare_pauses_line
- `timedata_lists`
- `ydata_lists`
- `axs`
- `colors`
- `labels`

> ### plot_paused_and_running_line

> ### compare_paused_running_line
- `xdata_list`
- `ydata_list`
- `axs`
- `colors`
- `labels`
- `const_bar_width=False`

> ### generic_plotting
- `xdata_list`
- `ydata_list`
- `axs`
- `colors`
- `labels`
- `plotting_function`
- `optional`

> ### plot_heatmap
- `heatmap`
- `dimensions`
- `labels=True`

> ### print_metadata_short
- `metadata_table`
- `label`
- `print_title=True`

> ### print_metadata
- `metadata_table`
- `labels`
- `column_width=14`
