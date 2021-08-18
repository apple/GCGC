# GCGC :  Garbage Collection Graph Collector 

<img src="images/stw_pauses_log.jpg" alt="Example scatter plot" />
<img src="images/heatmap.jpg" alt="Example heat map plot" />



GCGC uses a Jupyter notebook interface to analyze GC log files.

The analysis is built into a provided notebook, and generates plots and tables from collected GC information. The collected data for each log is parsed into a python pandas 'event log'. Then, using the event logs as a persistent database, the event information can be sorted, filtered, and grouped in both pre-set and customizable ways to display relevant trends and outliers.
 
There are 17 generated plots, which analyze latency, concurrent and STW events, heap information, allocation rates, frequencies of events, and trends, comparing any number of log files and external data sources. 

Furthermore, using Jupyter notebook data visualization allows for easy customization of provided plots.

Currently supports collectors in JDK11 & JDK 16.
 # Requirements

- Python3 
- The following Python3 packages
    - numpy
    - pandas
    - matplotlib
    - Jupyter notebook 

Installation explained here: [docs/setup.md](./docs/setup.md)



# How to run analysis

Follow the instructions in [docs/how-to-run.md](./docs/how-to-run.md)

--- 

## Known edge cases:

Note: The following edge cases are known and not handled automatically:

1) Shenandoah has two phases per garbage collection cycle reporting Heap allocation, will lead to two plotted heap occupancy metrics for each GC phase.
2) ZGC in JDK16 Puts information in safepoints, does not automatically print these in log analysis as it currently stands. These safepoints have comparable metrics to pause times, but ZGC does not report them in the same fashion, so these must be manually enabled on plots.
3) ZGC bytes reclaimed calculation (This may extend to Shenandoah) may be negative, if the rate of allocation exceeds the rate of gc collection. Information is correctly provided in logs, not properly analyzed here. Feature is being fixed in a later version
4) Trying to plot a graph or plot with a returned matlpotlib.axes variable declared in another cell does not show up inline in Jupyter notebooks.
5) Using column_timing = "DateTime" in any function that requires an "interval_duration" breaks the tool's analysis features, since DateTime represents each day with about 0.25 float value precision, not the expected unit of seconds. Feature is being fixed in a later version.

--- 
### Note:
The following file will have documentation improvements to make improvements easier:
- src/parse_log_file.py 

