# Functions to assist with easily using collected gc data
Ellis Brown. 6/16/2021

> ### get_combined_xy_pauses
> Takes a [pandas dataframe](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html) and extracts the x timestamp information, and y pause latency information.  Timestamps are in seconds, latency pauses are in miliseconds.
- `dataframe` data to be parsed through. Should have labeled columns `TimeFromStart_seconds` and `PauseDuration_miliseconds`
- `to_list=True` if true, the data is returned as a list, rather than a pandas series. (Recommended)


> ### remove_last_character
> Removes the last character from a line. Inteded for use on strings. Returns string
- `line` string line


> ### get_time_in_seconds
> Gets the time from a [pandas dataframe](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html) with the field TimeFromStart_seconds and returns it.
- `dataframe` data to be parsed. Should have column labeled `TimeFromStart_seconds`
- `to_list=True` if true, the data is returned as a list, rather than a pandas series. (Recommended)
>

> ### get_pauses_in_miliseconds
> Gets the latency STW pauses from a [pandas dataframe](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html) with the field PauseDuration_miliseconds and returns it.
- `dataframe` data to be parsed.  Should have column labeled `PauseDuration_miliseconds`
- `to_list=True` if true, the data is returned as a list, rather than a pandas series. (Recommended)

> ### get_sum_pauses_n_buckets
> Takes a group of pauses and timestamps, and groups them by time into n buckets, summing all pauses during that time period.
- `timestamps` list of float data for each pause occurance
- `pausedata` list of float data for each latency pause period
- `num_buckets` the number of buckets to sort the data into, based on timestamps.


> ### get_sum_pauses_n_duration
> Takes a group of pauses and timestamps, and groups them by time into buckets of size 'duration'. Returns lists `time, pauses` after modifiyng them
- `timestamps` list of float data for each pause occurance
- `pausedata` list of float data for each latency pause period
- `duration` time period for each bucket, in miliseconds. 


> ### get_max_pauses_n_buckets
> Takes a group of pauses and timestamps, and groups them by time into n buckets, taking the maximum pause within that time period. Returns lists `time, pauses` 
- `timestamps` list of float data for each pause occurance
- `pausedata` list of float data for each latency pause period
- `num_buckets` the number of buckets to sort the data into, based on timestamps.


> ### get_max_pauses_n_duration
> Takes a group of pauses and timestamps, and groups them by time into buckets of size 'duration' based on the maximum in each bucket (if any). Returns lists `time, pauses` 
- `timestamps` list of float data for each pause occurance
- `pausedata` list of float data for each latency pause period
- `duration`


> ### compare_max_pauses_n_duration
> Compares multiple lists using a constant bucket size for grouping, groups based on max per latency list.
- `xdata_lists` list of float lists, showing timestamps for gc runs
- `ydata_lists` list of float lists, showing pause durations
- `duration` size of one pause bucket, to group max intos
>

> ### compare_max_pauses_n_buckets
- `xdata_lists` list of float lists, showing timestamps for gc runs
- `ydata_lists` list of float lists, showing pause durations
- `duration` size of one pause bucket, to group max intos

> ### compare_sum_pauses_n_duration
- `xdata_lists` list of float lists, showing timestamps for gc runs
- `ydata_lists` list of float lists, showing pause durations
- `duration` size of one pause bucket, to group sums intos

> ### compare_sum_pauses_n_buckets
- `xdata_lists` list of float lists, showing timestamps for gc runs
- `ydata_lists` list of float lists, showing pause durations
- `duration` size of one pause bucket, to group sums intos

> ### get_heatmap_data

> ### get_heap_occupancy
- `dataframe`

