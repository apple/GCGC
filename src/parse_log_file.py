#       parse_log_line_regex.py
#
#   Defines the parsing function for reading a GC log line in JDK11 & JDK16
#   Returns a regex searchable string 
#


## # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#                       event_parsing_string
#
#   Returns a regex-searchable string to handle parsing log lines.
#   Defined regex groups are each section of the code
#
## # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
'''
The regex capture groups follow the following format:
1 : DateTime                    | string
2 : TimeFromStart_seconds       | float
3 : GGIndex                     | float
4 : EventType                   | string
5 : EventName                   | string
6 : AdditionalEventInfo         | string
7 : HeapBeforeGC  *             | float
8 : HeapAfterGC   *             | float
9 : MaxHeapsize   *             | float
10: Duration_milliseconds        | float
11: HeapBeforeGC * (zgc)        | float
12: HeapAfterGC  * (zgc)        | float
13: MaxHeapsize  * (zgc)        | float
14: SafepointName               | string
15: TimeFromLastSafepoint_ns    | float
16: TimeToReachSafepoint_ns     | float
17: AtSafepoint_ns              | float
18: TotalTimeAtSafepoint_ns     | float
19: TotalApplicationThreadPauseTime_seconds | float
20: TimeStopApplication_seconds | float
'''
def event_parsing_string():
# Note: the documentation of this regex string is confusing. It is recommended you follow along
    # Using this link to view the regex in a more natural way.
    # https://regexper.com/#%5E%28%3F%3A%5C%5B%28%5Cd%7B4%7D-%5Cd%5Cd-%5Cd%5CdT%5Cd%5Cd%3A%5Cd%5Cd%3A%5Cd%5Cd%5C.%5Cd%7B3%7D%5C%2B%5Cd%7B4%7D%29%5C%5D%29%3F%5C%5B%28%5Cd%2B%5C.%5Cd%2B%29s%5C%5D%28%3F%3A%5C%5B.*%3F%5C%5D%29%2B%28%3F%3A%28%3F%3A%20GC%5C%28%5Cd%2B%5C%29%20%28%28%3F%3APause%28%3F%3D.*ms%29%29%7C%28%3F%3AConcurrent%28%3F%3D.*ms%29%29%7C%28%3F%3AGarbage%20Collection%29%29%20%28%3F%3A%28%28%3F%3A%5Cw%2B%20%3F%29%7B1%2C3%7D%29%20%29%3F%28%28%3F%3A%5C%28%28%3F%3A%5Cw%2B%20%3F%29%7B1%2C3%7D%5C%29%20%29%7B0%2C3%7D%29%28%3F%3A%28%3F%3A%28%3F%3A%28%5Cd%2B%29%5Cw-%3E%28%5Cd%2B%29%5Cw%28%3F%3A%5C%28%5Cd%2B%5Cw%5C%29%3F%29%3F%29%3F%28%3F%3D%20%3F%28%5Cd%2B%5C.%5Cd%2B%29ms%29%29%7C%28%3F%3A%28%5Cd%2B%29%5Cw%5C%28%5Cd%2B%25%5C%29-%3E%28%5Cd%2B%29%5Cw%5C%28%5Cd%2B%25%5C%29%29%29%29%7C%28%3F%3A%20Safepoint%20%5C%22%28%5Cw%2B%29%5C%22%2C%20Time%20since%20last%3A%20%28%5Cd%2B%29%20ns%2C%20Reaching%20safepoint%3A%20%28%5Cd%2B%29%20ns%2C%20At%20safepoint%3A%20%28%5Cd%2B%29%20ns%2C%20Total%3A%20%28%5Cd%2B%29%20ns%24%29%7C%28%3F%3A%20Total%20time%20for%20which%20application%20threads%20were%20stopped%3A%20%28%5B%5Cd%5C.%5D%2B%29%20seconds%2C%20Stopping%20threads%20took%3A%20%28%5B%5Cd%5C.%5D%2B%29%20seconds%24%29%29
# The regex has 3 main capture patterns

    # Note: each documented part oof a string has an example capture group as the last comment above the regex region
    start_of_line = "^", None, None


    #   DateTime : Real time of the program's run in DateTime format
    #   Field : Optional
    #   Group : 1 
    #   Captures : Full date time expression, including formatting digits
    #   [2021-07-01T23:23:22.001+0000]
    #   ((empty string))
    date_time = "(?:\[(\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d\.\d{3}[+-]\d{4})\])?", "DateTime", str  

    #   TimeFromStart_seconds : 
    #   Field : Required
    #   Group : 2
    #   Captures : Full time in seconds, only including floating numbers and decimal place. Does not include unit.
    #   [243.45s]
    time_from_start_seconds = "\[(\d+\.\d+)s\]", "TimeFromStart_seconds", float   
    
    #   Other info fields detailing log line info
    #   Field : Required
    #   Group : Non capturing
    #   [info][gc          ] 
    #   [info][81200][gc]
    #    ((empty string)0)
    other_info_fields = "(?:\[.*?\])+", None, None
    
    #   GCIndex
    #   Field : Required
    #   Group : 3
    #   Captures: integer number of the GC's count for an event
    #   GC(0) 
    #   GC(21142) 
    gc_event_number = "(?:(?: GC\((\d+)\) ", "GCIndex", int
    
    #   EventType : Type of gc event
    #   Field : Required / Normal
    #   Group : 4
    #   Captures: The exact word from the choices of ("Pause", "Concurrent", "Garbage Collection")
    #   Pause
    #   Concurrent
    #   Garbage Collection
    gc_event_type = "((?:Pause(?=.*ms))|(?:Concurrent(?=.*ms))|(?:Garbage Collection)) ", "EventType", str
    
    #   EventName : The name of the GC event
    #   Field : Required / Normal
    #   Group : 5
    #   Captures : The set of 1-3 words following the EventType that names the event
    #   Young 
    #   Mark
    #   ((empty string))
    gc_event_name = "(?:((?:\w+ ?){1,3}) )?", "EventName", str  # Young    *
    
    #   AdditionalEventInfo
    #   Field : Optional
    #   Group : 6
    #   Captures: The set of 0-3 words in 0-3 parentheses following the EventName
    #   (Normal) (G1 Evacuation Pause)
    #   ((empty string))
    gc_additional_info = "((?:\((?:\w+ ?){1,3}\) ){0,3})", "AdditionalEventInfo", str  # (Evacuation Pause)    *
    
    #   Non capturing group setup for OR expressions
    #   Field: NA
    #   Group : Non capturing
    #   (no example, nothing here to be compared against)
    setup_optional_groups = "(?:(?:(?:", None, None

    #   HeapBeforeGC : Captures the heapsize in MB before the GC run.
    #   Field : Optional
    #   Group: 7
    #   Captures: The float value for the heapsize. No unit captured 
    #   411M->
    #   222M->
    #   8M->
    heap_before_gc = "(\d+)\w->", "HeapBeforeGC", float
    
    #   HeapAfterGC : Captures the heapsize in MB after the GC run.
    #   Field : Optional
    #   Group : 8
    #   Captures :  The float value for the heapsize. No unit captured
    #   98M(
    #   123542M(
    heap_after_gc = "(\d+)\w(?:\(", "HeapAfterGC", float

    #   MaxHeapsize: The current maximum heap size after the GC run
    #   Field : Optional  
    #   Group: 9
    #   Captures : The integer value for the heapsize
    #   (8192M)
    #   (123456M)
    #   (0000M)
    max_heap_size = "(\d+)\w\)?)?", "MaxHeapsize", float

    #   Closing capture group, create positive lookahead
    #   Field : NA
    #   Group : Non capturing
    #   (no example, nothing here to be compared against)
    optional_group_stuff = ")?(?= ?", None, None
    
    #   Duration_milliseconds :  Time used for this event in milliseconds
    #   Field : Required / Normal
    #   Group : 10
    #   Captures: The value of the duration. No unit captures
    #   11.751ms
    #   12314.751ms
    time_spent_milliseconds = "(\d+\.\d+)ms))", "Duration_milliseconds", float  # 24.321ms
    
    #   Begin regex for ZGC specific memory capturing 
    #   Field : NA
    #   Group : Non capturing
    #   (no example, nothing here to be compared against)
    zgc_memory_start = "|(?:", None, None

    #   HeapBeforeGC : ZGC style heap before gc metric
    #   Field : Required / ZGCmem
    #   Group : 11
    #   Captures : The Heap size in MB before GC run. No unit captured.
    #   12345M(00%)->
    #   00000M(12345%)->
    zgc_heap_before_gc = "(\d+)\w\(\d+%\)->", "HeapBeforeGC", float

    #   HeapAfterGC : ZGC style heap after gc metric
    #   Field : Required / ZGCmem
    #   Group : 12 
    #   Captures : The Heap size in MB after GC run. No unit captured.
    #   194M
    #   00000G
    zgc_heap_after_gc = "(\d+)\w\(", "HeapAfterGC", float
        
    
    #   MaxHeapsize : The size of the current heap in MB
    #   Field : 99
    #   Group : 13
    #   Captures : the max heap size percentage full after completed GC
    #   (2%)
    #   (00000%)
    zgc_max_heapsize = "(\d+)%\))))", "MaxHeapsize", float

    #   SafepointName : The name of the recorded safepoint
    #   Field : Required / Safepoint JDK16
    #   Group : 14
    #   Captures: Name of the safepoint, not including parentheses
    #   Safepoint "ZMarkEnd",
    #   Safepoint "Example",
    safepoint_name = "|(?: Safepoint \"(\w+)\"", "SafepointName", str

    #   TimeFromLastSafepoint_ns : Time from last safepoint in nanoseconds
    #   Field : Required / Safepoint JDK16
    #   Group : 15 
    #   Captures: The time since the last safepoint in nanoseconds. No unit captured.
    #   Time since last: 717687090 ns, 
    #   Time since last: 9999 ns, 
    safepoint_time_since_last = ", Time since last: (\d+) ns, ", "TimeFromLastSafepoint_ns", float
    
    #   TimeToReachSafepoint_ns
    #   Field : Required / Safepoint JDK16
    #   Group : 16
    #   Captures : Time required to reach the safepoint
    #   Reaching safepoint: 109049 ns, 
    #   Reaching safepoint: 99999 ns, 
    safepoint_time_to_reach = "Reaching safepoint: (\d+) ns, ", "TimeToReachSafepoint_ns", float
    

    #   AtSafepoint_ns
    #   Field :  Required / Safepoint JDK16
    #   Group : 17
    #   Captures: Time while at Safepoint. No unit captured,
    #   At safepoint: 38222 ns, 
    #   At safepoint: 00000 ns, 
    time_at_safepoint = "At safepoint: (\d+) ns, ", "AtSafepoint_ns", float

    #   TotalTimeAtSafepoint_ns
    #   Field :  Required / Safepoint JDK16
    #   Group : 18
    #   Captures : Total time spent getting to and at the safepoint. No unit captured 
    #   Total: 147271 ns
    #   Total: 00000 ns
    total_time_safepoint = "Total: (\d+) ns$)", "TotalTimeAtSafepoint_ns", float

    #   TotalApplicationThreadPauseTime_seconds
    #   Field : Required / Safepoint JDK11
    #   Group : 19
    #   Captures : Total time the program's application threads were stopped
    #   Total time for which application threads were stopped: 0.0002106 seconds,
    #   Total time for which application threads were stopped: 99999.99999 seconds,
    program_pause_time = ("|(?: Total time for which application threads were stopped: ([\d\.]+) seconds,",
                        "TotalApplicationThreadPauseTime_seconds", float)

    #   TimeToStopApplication_seconds
    #   Field : Required / Safepoint JDK11
    #   Group : 20
    #   Captures: Time in seconds to stop threads for safepoint
    #    Stopping threads took: 0.0000900 seconds
    #    Stopping threads took: 9999.9999 seconds
    time_to_stop_application = " Stopping threads took: ([\d\.]+) seconds$))", "TimeToStopApplication_seconds", float
    
    
    event_parsing = [start_of_line ,                # ALL
                     date_time ,                    # ALL
                     time_from_start_seconds ,      # ALL
                     other_info_fields ,            # ALL
                     gc_event_number ,              # normal
                     gc_event_type ,                # normal
                     gc_event_name ,                # normal
                     gc_additional_info ,           # normal
                     setup_optional_groups ,        # normal
                     heap_before_gc ,               # normal
                     heap_after_gc ,                # normal
                     max_heap_size ,                # normal
                     optional_group_stuff ,         # normal
                     time_spent_milliseconds ,       # normal
                     zgc_memory_start ,             # zgc mem
                     zgc_heap_before_gc ,           # zgc mem
                     zgc_heap_after_gc ,            # zgc mem
                     zgc_max_heapsize ,             # zgc mem
                     safepoint_name ,               # safepoints jdk16
                     safepoint_time_since_last ,    # safepoints jdk16
                     safepoint_time_to_reach ,      # safepoints jdk16
                     time_at_safepoint ,            # safepoints jdk16
                     total_time_safepoint ,         # safepoints jdk16
                     program_pause_time ,           # safepoints jdk 11
                     time_to_stop_application]      # safepoints jdk 11
    
    regex_group, column_name, data_type = [], [], []
    
    for capture_group in event_parsing:
        regex_group.append(capture_group[0])
        column_name.append(capture_group[1])
        data_type.append(capture_group[2])
    
    capture_string = "".join(regex_group)

    return capture_string, column_name, data_type


# The following lines are matches. Use https://regex101.com to test match groups.
'''
[1.044s][info][gc          ] GC(0) Garbage Collection (Warmup) 916M(11%)->246M(3%)
[14.169s][info][gc          ] GC(6) Pause Young (Allocation Failure) 2597M->133M(7993M) 24.738ms
[0.611s][info][gc          ] GC(0) Pause Young (Normal) (G1 Evacuation Pause) 411M->98M(8192M) 141.751ms
[2021-07-20T12:29:49.655+0000][370.855s][2258357][2258375][info ] GC(78) Pause Young (Normal) (G1 Evacuation Pause) 5850M->985M(8192M) 78.739ms
[2021-07-20T12:39:31.364+0000][26.826s][2267133][2267139][info ] Total time for which application threads were stopped: 0.0001782 seconds, Stopping threads took: 0.0000366 seconds
[2021-07-20T12:39:57.833+0000][53.296s][2267133][2267139][info ] GC(15) Pause Young (Allocation Failure) 3160M->1787M(7592M) 69.406ms
[2021-07-20T13:42:01.205+0000][96.063s][2302588][2302600][info ] GC(28) Concurrent cleanup 4045M->4040M(8192M) 0.031ms
[2021-07-20T13:28:05.551+0000][1.061s][2294560][2294576][info ] Safepoint "ICBufferFull", Time since last: 352774642 ns, Reaching safepoint: 128133 ns, At safepoint: 1429 ns, Total: 129562 ns
'''

