# updated_parse_data .py
## Used to read through a gc log and extract relevant data on the runtime
Ellis Brown 6/16/2021

> ### getPauses
> Searched through a log file, and returns a dataframe showing gc pauses, with recorded changes in heap usage. Defines what type of pause was recorded, if possible. Named columns describe returned data, rows are each gc instance. Return includes time / gc other metadata
- `logfile=None` str filepath to logfile to be analyzed
- `gctype` string description of logtype. If left blank, the gctype will attempt to be automatically be detected & set. Acceptable filetypes : "G1", "Shenandoah". More coming soon.
- `create_csv=False` if true, a csv of the output pandas dataframe will be created.

> ### getConcurrentDurations
> Searches through the file for concurrent phases recorded in the gc. Returns a pandas dataframe with the recorded phases, and additional metadata.
- `logfile=None` str filepath to logfile to be analyzed
- `gctype` string description of logtype. If left blank, the gctype will attempt to be automatically be detected & set. Acceptable filetypes : "G1", "Shenandoah". More coming soon.
- `create_csv=False` if true, a csv of the output pandas dataframe will be created.

> ### getGCdataSections
> Takes all information in the GC log, and turns it into a pandas dataframe. Columns are not named, but are described in the functions inline documentation.  TODO: update inline documentation and documentation here for this function.
- `logfile=None` str filepath to logfile to be analyzed
- `gctype` string description of logtype. If left blank, the gctype will attempt to be automatically be detected & set. Acceptable filetypes : "G1", "Shenandoah". More coming soon.
- `create_csv=False` if true, a csv of the output pandas dataframe will be created.

> ### getTotalProgramRuntime
> Gets the total runtime of the program, by reading backwards from the end of the file to find the last recorded timestamp.
- `logfile=None` str filepath to logfile to be analyzed

> ### getGCMetadata
> Gathers metadata printed into the log for runtime. TODO: Currently only works on G1.
- `logfile=None` str filepath to logfile to be analyzed
- `create_csv=False` if true, a csv of the output pandas dataframe will be created.

> ### getHeapAllocation
> Parses a gc log and gathers heap allocation data both before and after gabage collection runs.
- `logfile=None` str filepath to logfile to be analyzed
- `gctype=None` string description of logtype. If left blank, the gctype will attempt to be automatically be detected & set. Acceptable filetypes : "G1", "Shenandoah". More coming soon.
- `create_csv=False` if true, a csv of the output pandas dataframe will be created.
- `robust=False` a robust file is expected to include full mapping of each chunk of heap memory in the during each gc runtime, as a trace. Turn on this feature to gather heap allocation for such files.

> ### get_gc_type
> Automatically detects and returns the gc type of a specified file (from filepath) as a string. May fail to return the correct type if unable to detect.
- `filepath`

