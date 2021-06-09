## /Jupyter-everything/scripts/

- `compare_logs.py`
    - handles graphical comparison and data collection for multiple logs

- `g1version16.py`
    - handles exact formatting of log outputs using regex strings for g1 logs, includes mapping functions for searching for one / many regex strings within a set of data or file

- `plot_data.py`
    - Handles plotting data for a single log file

- `parse_log.py`

    - Creates public functions to set a file to parse, and parse through that file for information

### The following is temporary
- `zulu_output_process.py`
    - extract information from a JFR output with strange csv formatting

> Functions for parsing log files. Exported in scripts/parse_log.py
>- `setLogPath( filename  = '' )`
>- `getLogPath()`
>- `getLogSchema( logtype = 0)`
>- `getPauses( create_csv = False )` 
>- `getHeapAllocation( create_csv = False )`
>- `GetGCMetadata( create_csv = False)`
>- `getHeapInitialState( create_csv = False )`
>- `getGCdataSections( create_csv = False )` - large output
>- `getTotalProgramRuntime( create_csv = False)`
>- `getGCMetadata(create_csv = False )`

> Functions for displaying log data. Exported in scripts/plot_data.py
>- `plot_pauses( table )`
>- `plot_heap_allocation_breakdown( table )`
>- `displayMetadata( table )`
>- `heap_allocation_before_gc( data_arr, max_heap_size)`
>- `plot_heatmap( table, width = 20, height = 20, labels = True )`
>- coming soon (currently in scripts/compare_logs.py):
>   - Old memory during runtime
>   - Total allocated before gc run
>   - Total allocated after gc run

