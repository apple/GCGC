#       parse_log_line_regex.py
#
#   Defines the parsing function for reading a GC log line in JDK11 & JDK16
#   Returns a regex searchable string 
#


## # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#                       event_parsing_string
#
# Returns a regex-searchable string to handle parsing log lines.
# Defined regex groups are each section of the code
#
# GROUP 1: "DateTime" -> information on time of recording
# GROUP 2: "TimeFromStart_seconds" -> time of beginning of event in seconds
# GROUP 3: "EventType" -> Either concurrent or stop the world pause
# GROUP 4: "EventName" -> Specific action from the event. Example : "(pause) Young"
# GROUP 5: "AdditionalEventInfo" -> Information about the event
# GROUP 6: "MemoryChange_MB" -> Memory changed, following this patten: before->after(max_heapsize)
# 7, 11: before
# Return: string
## # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def event_parsing_string():
# Note: the documentation of this regex string is confusing. It is recommended you follow along
# Using this link to view the regex in a more natural way.
# https://regexper.com/#%5E%28%3F%3A%5C%5B%28%5Cd%7B4%7D-%5Cd%5Cd-%5Cd%5CdT%5Cd%5Cd%3A%5Cd%5Cd%3A%5Cd%5Cd%5C.%5Cd%7B3%7D%5C%2B%5Cd%7B4%7D%29%5C%5D%29%3F%5C%5B%28%5Cd%2B%5C.%5Cd%2B%29s%5C%5D%28%3F%3A%5C%5B.*%3F%5C%5D%29%2B%28%3F%3A%28%3F%3A%20GC%5C%28%5Cd%2B%5C%29%20%28%28%3F%3APause%28%3F%3D.*ms%29%29%7C%28%3F%3AConcurrent%28%3F%3D.*ms%29%29%7C%28%3F%3AGarbage%20Collection%29%29%20%28%3F%3A%28%28%3F%3A%5Cw%2B%20%3F%29%7B1%2C3%7D%29%20%29%3F%28%28%3F%3A%5C%28%28%3F%3A%5Cw%2B%20%3F%29%7B1%2C3%7D%5C%29%20%29%7B0%2C3%7D%29%28%3F%3A%28%3F%3A%28%3F%3A%28%5Cd%2B%29%5Cw-%3E%28%5Cd%2B%29%5Cw%28%3F%3A%5C%28%5Cd%2B%5Cw%5C%29%3F%29%3F%29%3F%28%3F%3D%20%3F%28%5Cd%2B%5C.%5Cd%2B%29ms%29%29%7C%28%3F%3A%28%5Cd%2B%29%5Cw%5C%28%5Cd%2B%25%5C%29-%3E%28%5Cd%2B%29%5Cw%5C%28%5Cd%2B%25%5C%29%29%29%29%7C%28%3F%3A%20Safepoint%20%5C%22%28%5Cw%2B%29%5C%22%2C%20Time%20since%20last%3A%20%28%5Cd%2B%29%20ns%2C%20Reaching%20safepoint%3A%20%28%5Cd%2B%29%20ns%2C%20At%20safepoint%3A%20%28%5Cd%2B%29%20ns%2C%20Total%3A%20%28%5Cd%2B%29%20ns%24%29%7C%28%3F%3A%20Total%20time%20for%20which%20application%20threads%20were%20stopped%3A%20%28%5B%5Cd%5C.%5D%2B%29%20seconds%2C%20Stopping%20threads%20took%3A%20%28%5B%5Cd%5C.%5D%2B%29%20seconds%24%29%29
# Required / Safepoint means that the filed is required in a "Safepoint" line
# Required / Normal    means the filed is required for a general non-safepoint event

    start_of_line = "^"
    #   DateTime : Real time of the program's run in DateTime format
    #   Field : Optional
    #   Group : 1 
    #   Captures : Full date time expression, including formatting digits
    date_time = "(?:\[(\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d\.\d{3}\+\d{4})\])?"  # [2021-07-01T23:23:22.001+0000]    *

    #   TimeFromStart_seconds : 
    #   Field : Required
    #   Group : 2
    #   Captures : Full time in seconds, only including floating numbers and decimal place. Does not include unit.
    time_from_start_seconds = "\[(\d+\.\d+)s\]"  #[243.45s]
    
    #   Other info fields detailing log line info
    #   Field : Required
    #   Group : Non capturing
    other_info_fields = "(?:\[.*?\])+ "
    
    #   Gc event number
    #   Field : Required
    #   Group : Non capturing
    gc_event_number = "(?:(?: GC\(\d+\) "
    
    #   EventType : Type of gc event
    #   Field : Required / Normal
    #   Group : 3
    #   Captures: The exact word from the choices of ("Pause", "Concurrent", "Garbage Collection")
    gc_event_type = "((?:Pause(?=.*ms))|(?:Concurrent(?=.*ms))|(?:Garbage Collection)) " 
    
    #   EventName : The name of the GC event
    #   Field : Required / Normal
    #   Group : 4
    #   Captures : The set of 1-3 words following the EventType that names the event
    gc_event_name = "(?:((?:\w+ ?){1,3}) )?"  # Young    *
    
    #   AdditionalEventInfo
    #   Field : Optional
    #   Group : 5
    #   Captures: The set of 0-3 words in 0-3 parentheses following the EventName
    gc_additional_info = "((?:\((?:\w+ ?){1,3}\) ){0,3})"  # (Evacuation Pause)    *
    
    #   Non capturing group setup for OR expressions
    #   Field: NA
    #   Group : Non capturing
    setup_optional_groups = "(?:(?:(?:"

    #   HeapBeforeGC : Captures the heapsize in MB before the GC run.
    #   Field : Optional
    #   Group: 6
    #   Captures: The float value for the heapsize. No unit captured 
    heap_before_gc = "(\d+)\w->"
    
    #   HeapAfterGC : Captures the heapsize in MB after the GC run.
    #   Field : Optional
    #   Group : 7
    #   Captures :  The float value for the heapsize. No unit captured
    heap_after_gc = "(\d+)\w(?:\(\d+\w\)?)?"

    #   Closing capture group, create positive lookahead
    #   Field : NA
    #   Group : Non capturing
    optional_group_stuff = ")?(?= ?"
    
    #   Duration_miliseconds :  Time used for this event in miliseconds
    #   Field : Required / Normal
    #   Group : 8
    #   Captures: The value of the duration. No unit captures
    time_spent_miliseconds = "(\d+\.\d+)ms))"  # 24.321ms
    
    #   Begin regex for ZGC specific memory capturing 
    #   Field : NA
    #   Group : Non capturing
    zgc_memory_start = "|(?:"

    #   HeapBeforeGC : ZGC style heap before gc metric
    #   Field : Required / ZGCmem
    #   Group : 9 
    #   Captures : The Heap size in MB before GC run. No unit captured.
    zgc_heap_before_gc = "(\d+)\w\(\d+%\)->"

    #   HeapAfterGC : ZGC style heap after gc metric
    #   Field : Required / ZGCmem
    #   Group : 10 
    #   Captures : The Heap size in MB after GC run. No unit captured.
    zgc_heap_after_gc = "(\d+)\w\(\d+%\))))"

    #   SafepointName : The name of the recorded safepoint
    #   Field : Required / Safepoint JDK16
    #   Group : 11
    #   Captures: Name of the safepoint, not including parentheses
    safepoint_name = "|(?: Safepoint \"(\w+)\""

    #   TimeFromLastSafepoint_ns : Time from last safepoint in nanoseconds
    #   Field : Required / Safepoint JDK16
    #   Group : 12 
    #   Captures: The time since the last safepoint in nanoseconds. No unit captured.
    safepoint_time_since_last = ", Time since last: (\d+) ns, "
    
    #   TimeToReachSafepoint_ns
    #   Field : Required / Safepoint JDK16
    #   Group : 13
    #   Captures : Time required to reach the safepoint
    safepoint_time_to_reach = "Reaching safepoint: (\d+) ns, "
    
    #   AtSafepoint_ns
    #   Field :  Required / Safepoint JDK16
    #   Group : 14
    #   Captures: Time while at Safepoint. No unit captured,
    time_at_safepoint = "At safepoint: (\d+) ns, "

    #   TotalTimeAtSafepoint_ns
    #   Field :  Required / Safepoint JDK16
    #   Group : 15
    #   Captures : Total time spent getting to and at the safepoint. No unit captured 
    total_time_safepoint = "Total: (\d+) ns$)"

    #   TotalApplicationThreadPauseTime_seconds
    #   Field : Required / Safepoint JDK11
    #   Group : 16
    #   Captures : Total time the program's application threads were stopped
    program_pause_time = "|(?: Total time for which application threads were stopped: ([\d\.]+) seconds,"

    #   TimeToStopApplication_seconds
    #   Field : Required / Safepoint JDK11
    #   Group : 17
    #   Captures: Time in seconds to stop threads for safepoint
    time_to_stop_application = " Stopping threads took: ([\d\.]+) seconds$))"
    
    
    event_parsing = (start_of_line +                # ALL
                     date_time +                    # ALL
                     time_from_start_seconds +      # ALL
                     other_info_fields +            # ALL
                     gc_event_number +              # normal
                     gc_event_type +                # normal
                     gc_event_name +                # normal
                     gc_additional_info +           # normal
                     setup_optional_groups +        # normal
                     heap_before_gc +               # normal
                     heap_after_gc +                # normal
                     optional_group_stuff +         # normal
                     time_spent_miliseconds +       # normal
                     zgc_memory_start +             # zgc mem
                     zgc_heap_before_gc +           # zgc mem
                     zgc_heap_after_gc +            # zgc mem
                     safepoint_name +               # safepoints jdk16
                     safepoint_time_since_last +    # safepoints jdk16
                     safepoint_time_to_reach +      # safepoints jdk16
                     time_at_safepoint +            # safepoints jdk16
                     program_pause_time +           # safepoints jdk11
                     time_to_stop_application)      # safepoints jdk11
    return event_parsing
    # TODO: Update documentation on capture group after new inclusion of "Safepoint" metrics
    # return "^(?:\[(\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d\.\d{3}\+\d{4})\])?\[(\d+\.\d+)s\](?:\[.*?\])+(?:(?: GC\(\d+\) ((?:Pause(?=.*ms))|(?:Concurrent(?=.*ms))|(?:Garbage Collection)) (?:((?:\w+ ?){1,3}) )?((?:\((?:\w+ ?){1,3}\) ){0,3})(?:(?:(?:(\d+)\w->(\d+)\w(?:\(\d+\w\)?)?)?(?= ?(\d+\.\d+)ms))|(?:(\d+)\w\(\d+%\)->(\d+)\w\(\d+%\))))|(?: Safepoint \"(\w+)\", Time since last: (\d+) ns, Reaching safepoint: (\d+) ns, At safepoint: (\d+) ns, Total: (\d+) ns$)|(?: Total time for which application threads were stopped: ([\d\.]+) seconds, Stopping threads took: ([\d\.]+) seconds$))"

# Examples follow below:

