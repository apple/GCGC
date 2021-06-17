# Functions to assist with plotting data for garbage collection
Ellis Brown. 6/16/2021

> ### plot_pauses_bar
> Constructs a bar graph from the provided data. Typically time vs. pause durations
- `xdata` a list of float data for the x axis. Typically integer time stamps in seconds.
- `ydata` a list of data for the y axis. Typically STW pause durations in miliseconds. list type = float
- `axs` a [matplotlib.axes](https://matplotlib.org/stable/api/axes_api.html#subplots) object that represents a plot.
- `color` a color from [matplotlib.colors](https://matplotlib.org/stable/gallery/color/named_colors.html). If no color is provided, a random color is created. type = string
- `label` a label to describe the data being plotted. If none provided, label is displayed as "No label provided". type = string


> ### compare_pauses_bar
> Compares multiple sets of data against each other on the same graph
- `timedata_lists` a list of lists of float data for the x axis. Typically the timestamps during runtime.
- `heightdata_lists` a list of lists of float data for the y axis. Typically the latency durations during runtime.
- `axs` a [matplotlib.axes](https://matplotlib.org/stable/api/axes_api.html#subplots) object that represents a plot. If none provided, one will be created
- `color` a list of colors from [matplotlib.colors](https://matplotlib.org/stable/gallery/color/named_colors.html). If no color is provided, a random color is created. type = string
- `labels` a list of labels to describe the data being plotted. If none provided, each label is displayed as "No label provided". type = string


> ### plot_pauses_scatter
> Constructs a scatter plot from the provided data
- `xdata` a list of float data for the x axis. Typically integer time stamps in seconds.
- `ydata` a list of data for the y axis. Typically STW pause durations in miliseconds. list type = float
- `axs` a [matplotlib.axes](https://matplotlib.org/stable/api/axes_api.html#subplots) object that represents a plot.
- `color` a color from [matplotlib.colors](https://matplotlib.org/stable/gallery/color/named_colors.html). If no color is provided, a random color is created. type = string
- `label` a label to describe the data being plotted. If none provided, label is displayed as "No label provided". type = string




> ### comparrison_scatter
> Compare multiple sets of data on the same scatter plot
- `xdata_list` a list of lists of float data for the x axis. Typically the timestamps during runtime.
- `ydata_list`a list of lists of float data for the y axis. Typically the latency durations during runtime. 
- `axs` a [matplotlib.axes](https://matplotlib.org/stable/api/axes_api.html#subplots) object that represents a plot. If none provided, one will be created.
- `colors` a list of colors from [matplotlib.colors](https://matplotlib.org/stable/gallery/color/named_colors.html). If no color is provided, a random color is created. type = string
- `labels` a list of labels to describe the data being plotted. If none provided, each label is displayed as "No label provided". type = string

> ### print_percentiles
> Print a set of percentiles for latency during runtime
- `pauses_miliseconds`  List of pauses during runtime (any order)
- `print_title=True`    If true, print a title for the ascii table being created 
- `percentiles` A list of floats, for each percentile to inspect. If none provided, default are used [50, 75, 90, 95, 99, 99.9, 99.99]
- `label` a label to describe the data being plotted. If none provided, label is displayed as "label". type = string

> ### compare_pauses_percentiles
> Create a table to compare latency percentiles for multiple latency lists
- `list_of_list_pauses_ms` List of list of pauses during runtime
- `percentiles` A list of floats, for each percentile to inspect. If none provided, default are used [50, 75, 90, 95, 99, 99.9, 99.99]
- `labels` a list of string labels to describe each entry in the pauses_miliseconds list. If none are provided, each label is displayed as "label". 

> ### print_trends
> Desribes trends within the data. Shows max, number of pauses, mean, sum, and maybe throughput. Outputs an ASCII table.
- `pauses_miliseconds` List of pauses to analyze
- `label` Label for this row in the table, to explain what data has been passed in
- `print_title=True` True to print title for ASCII table output by function
- `total_runtime_seconds` The total runtime in seconds (optional). Used to calculate throughput
- `timestamps` list of float time stamps for pause times (optional). Used to calculate throughput.

> ### compare_trends
> Compares trends of latency lists. Outputs an ASCII table.
- `pauses_ms_lists` List of lists of pauses to analyze. Pauses in miliseconds
- `labels` List of string labels to describe each pause list.
- `lists_of_total_program_runtime` list of floats showing the total runtime for each of the pause lists to analyze (optional) Used to calculate throughput.
- `lists_of_timestamps` lists of timestamps associated with each pause. (optional). Used to calculate throughput.

> ### plot_pauses_line
> Plots data on a line graph to compare latency over runtime.
- `time_seconds` a list of float timestamp data 
- `pauses_miliseconds` a list of float pauses of pause latency
- `axs` a [matplotlib.axes](https://matplotlib.org/stable/api/axes_api.html#subplots) object that represents a plot.
- `color` a color from [matplotlib.colors](https://matplotlib.org/stable/gallery/color/named_colors.html). If no color is provided, a random color is created. type = string
- `label` a label to describe the data being plotted. If none provided, labels are displayed as increasing integers


> ### compare_pauses_line
> Compares multiple sets of data using a line graph
- `timedata_lists` a list of lists of float data for timestamps per run
- `ydata_lists` a list of lists of float latency information per run
- `axs` a [matplotlib.axes](https://matplotlib.org/stable/api/axes_api.html#subplots) object that represents a plot. If none provided, one will be created
- `colors` a list of colors from [matplotlib.colors](https://matplotlib.org/stable/gallery/color/named_colors.html). If no color is provided, a random color is created. type = string
- `labels` a list of labels to describe the data being plotted. If none provided, each label is displayed as "No label provided". type = string

> ### plot_paused_and_running_line
> Plots data in a fasion to show pauses over runtime. Taller bars are for longer pauses, and a value of zero means the program was running without gc STW interruption.
- `time_seconds` list of float times 
- `pauses_miliseconds` list of float pauses
- `axs` a [matplotlib.axes](https://matplotlib.org/stable/api/axes_api.html#subplots) object that represents a plot.
- `color` a color from [matplotlib.colors](https://matplotlib.org/stable/gallery/color/named_colors.html). If no color is provided, a random color is created. type = string
- `label` a label to describe the data being plotted. If none provided, labels are displayed as increasing integers
- `const_bar_width=False` if True, ignores the trend that a value of zero means no stw interruption. Instead, makes bars equally spaced. Used for max/sum pauses over buckets plotting

> ### compare_paused_running_line
> Compares multiple sets of data using the pauses_lines approach, which has taller bars for longer pauses, and a value of zero means the program was running without gc STW interruptions
- `xdata_list` list of lists of float pause data
- `ydata_list` list of lists of float latency data
- `axs` a [matplotlib.axes](https://matplotlib.org/stable/api/axes_api.html#subplots) object that represents a plot. If none provided, one will be created
- `colors` a list of colors from [matplotlib.colors](https://matplotlib.org/stable/gallery/color/named_colors.html). If no color is provided, a random color is created. type = string
- `labels` a list of labels to describe the data being plotted. If none provided, each label is displayed as "No label provided". type = string
- `const_bar_width=False` if True, ignores the trend that a value of zero means no stw interruption. Instead, makes bars equally spaced. Used for max/sum pauses over buckets plotting


> ### plot_heatmap
- `heatmap` 2d information representing the buckets of the heatmap. It is recommended you gather this data using `scripts/transform_data/`
- `dimensions` list with dimensions as integers. Times in seconds, pauses in miliseconds.
    - heatmap width = dimensions[0]  
    - heamap height = dimensions[1] 
    - time bucket size = dimensions[3]
    - pause bucket size = dimensions[2]
- `labels=True` if True, frequency information will show up on the heatmap as integers. If false, only the colors will appear.

> ### print_metadata
- `metadata_table` a list of metadata lists. For more information, see parse/log
- `labels` a description for each metadata in the table
- `column_width=14` the length of the columns in the table. Can be decreased if many logs need to be compared, although characters are lost as the size decreases.
