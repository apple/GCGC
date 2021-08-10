# Notebooks


> If this is your first time using a Jupyter notebook for python3, and you would like to modifiy and understand the source code, use the following [tutorials](../../tutorials)


The notebook compare_any.ipynb is a complete analysis notebook, and only requires a user to edit the first cell. Locally create a copy of this file to do any work, and use the original as a reference.


## Important: 
If you do not know how to start a jupyter notebooks server/kernel required for all notebooks, follow the setup instructions in [setup.md](../../setup.md)

# GC Analysis provided
The following are a list of automatically generated graphs/tables that are created after filling in the first cell with GC information. Afterwards, a detailed tuning section for each graph can be found.

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

> #### 7. Average STW pause duration

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