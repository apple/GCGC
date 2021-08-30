#       parse_log_line_regex.py
#
#   Defines the parsing function for reading a GC log line in JDK11 & JDK16
#   Returns a regex searchable string, the column names associated, and the datatypes of the columns
#

'''https://regex101.com : the best website for checking regex!'''

# Note: the documentation of this regex string is confusing. It is STRONGLY recommended you follow along here!!!!
# https://regexper.com/#%5E%28%3F%3A%28%3F%3A%5C%5B%28%5Cd%7B4%7D-%5Cd%5Cd-%5Cd%5CdT%5Cd%5Cd%3A%5Cd%5Cd%3A%5Cd%5Cd%5C.%5Cd%7B3%7D%5B%2B-%5D%5Cd%7B4%7D%29%5C%5D%29%7C%28%3F%3A%5C%5B%28%5B%5Cd%5C.%5D%2B%29%28%28%3F%3As%29%7C%28%3F%3Ams%29%7C%28%3F%3Ans%29%29%5C%5D%29%29%28%28%3F%3A%5C%5B.*%3F%5C%5D%29*%29%28%3F%3A%28%3F%3A%20GC%5C%28%28%5Cd%2B%29%5C%29%20%28%28%3F%3APause%28%3F%3D.*ms%29%29%7C%28%3F%3AConcurrent%28%3F%3D.*ms%29%29%7C%28%3F%3AGarbage%20Collection%29%29%20%28%3F%3A%28%28%3F%3A%5Cw%2B%20%3F%29%7B1%2C4%7D%29%20%29%3F%28%28%3F%3A%5C%28%28%3F%3A%5Cw%2B%20%3F%29%7B1%2C3%7D%5C%29%20%29%7B0%2C3%7D%29%28%3F%3A%28%3F%3A%28%3F%3A%28%5Cd%2B%29M-%3E%28%5Cd%2B%29M%28%3F%3A%5C%28%28%5Cd%2B%29M%5C%29%3F%29%3F%29%3F%28%3F%3D%20%3F%28%5Cd%2B%5C.%5Cd%2B%29ms%29%29%7C%28%3F%3A%28%5Cd%2B%29M%5C%28%5Cd%2B%25%5C%29-%3E%28%5Cd%2B%29M%5C%28%28%5Cd%2B%29%25%5C%29%29%29%29%7C%28%3F%3A%20Safepoint%20%22%28%5Cw%2B%29%22%2C%20Time%20since%20last%3A%20%28%5Cd%2B%29%20ns%2C%20Reaching%20safepoint%3A%20%28%5Cd%2B%29%20ns%2C%20At%20safepoint%3A%20%28%5Cd%2B%29%20ns%2C%20Total%3A%20%28%5Cd%2B%29%20ns%24%29%7C%28%3F%3A%20Total%20time%20for%20which%20application%20threads%20were%20stopped%3A%20%28%5B%5Cd%5C.%5D%2B%29%20seconds%2C%20Stopping%20threads%20took%3A%20%28%5B%5Cd%5C.%5D%2B%29%20seconds%24%29%29


#       get_parsing_groups
#
#   Returns 3 seperate variables:
#   -> regex string to parse the file.
#   -> list of column names for that regex string, associated 1 to 1 with each group.
#   -> list of datatypes for each column associated with regex groups
#
def get_parsing_groups():
    start = "^", None, None
    
    date_time = "\[(\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d\.\d{3}[+-]\d{4})\]", "DateTime", str # [9999-08-26T14:42:00.565-0400]
                                                                                        # [2021-08-26T14:42:59.565-0400]
    time = "\[([\d\.]+)", "Time", float # 999999
                                        # 123541.21425
    time_unit = "((?:s)|(?:ms)|(?:ns))\]", "TimeUnit", str  # s
                                                            # ms
    other_fields = "((?:\[.*?\])*)", "Other fields", str    # [51805y92148y45y951 it doesnt matter whats in here]
                                                            # [gc][info][2048]
    gc_phase = " GC\((\d+)\)", "GCIndex", int   # GC (0)
                                                # GC (99999)
    # contains lookahead for time spent in event
    event_type = " ((?:Pause(?=.*ms))|(?:Concurrent(?=.*ms))|(?:Garbage Collection)) ", "EventType", str  # Concurrent
                                                                                                          # Pause 
    event_name = "(?:(" + words(1, 4) + ") )?", "EventName", str    # Young
                                                                    # Any Four Words Here
    additional_event_info = "((?:\("+ words(1, 3) +"\) ){0,3})", "AdditionalEventInfo", str # (Mixed)
                                                                                            # (Young) (Mixed Collection)
    # Confusing : Follow the capture groups in this section closely.
    # It is recommended you use the following resource : https://regexper.com
    heap_before_gc = "(?:(\d+)M->", "HeapBeforeGC", float   # 100M->
                                                            # 99999M->
    heap_after_gc = "(\d+)M", "HeapAfterGC", float  # 500M
                                                    # 99999M
    max_heapsize = "(?:\((\d+)M\)?)?)?(?=", "MaxHeapsize", float    # (200M)
                                                                    # (99999M)
    duration_ms = " ?(\d+\.\d+)ms)", "Duration_milliseconds", float # 99999.9999ms
                                                                    # 0.0ms

    zgc_heap_before_gc = "(\d+)M\(\d+%\)", "HeapBeforeGC", float    # 123M(200%)
                                                                    # 999M(999999%)
    zgc_heap_after_gc = "->(\d+)M", "HeapAfterGC", float    # ->200M
                                                            # ->99999M
    zgc_max_heapsize = "\((\d+)%\)", "MaxHeapsize", float   # (24%)
                                                            # (00000%)
    safepoint_name = " Safepoint \"(\w+)\"", "SafepointName", str   # Safepoint "Hello"
                                                                    # Safepoint "Example"
    safepoint_time_since_last = ", Time since last: (\d+) ns, ", "TimeFromLastSafepoint_ns", float  # , Time since last: 99999 ns
                                                                                                    # , Time since last: 1 ns
    safepoint_time_to_reach = "Reaching safepoint: (\d+) ns, ", "TimeToReachSafepoint_ns", float    # Reaching safepoint: 0 ns
                                                                                                    # Reaching safepoint: 99999 ns
    time_at_safepoint = "At safepoint: (\d+) ns, ", "AtSafepoint_ns", float     # At safepoint: 1000 ns
                                                                                # At safepoint: 123 ns

    total_time_safepoint = "Total: (\d+) ns$", "TotalTimeAtSafepoint_ns", float # Total: 1 ns$
                                                                                # Total: 000000 ns$
   
    program_pause_time = (" Total time for which application threads were stopped: ([\d\.]+) seconds,", #  Total time for which application threads were stopped: 999 seconds,
                        "TotalApplicationThreadPauseTime_seconds", float)                               #  Total time for which application threads were stopped: 00.000 seconds,
    time_to_stop_application = " Stopping threads took: ([\d\.]+) seconds$", "TimeToStopApplication_seconds", float # Stopping threads took 990 seconds
                                                                                                                    # Stopping threads took 000.000 seconds
  #################################### 
    
    # Creates the full regex group: Use the website on the top of this file to follow the logic visually.
    combined_groups = [
        start,
        *regex_or(  [date_time], 

                    [time, time_unit]),
        other_fields,
        *regex_or( [gc_phase, 
                    event_type, 
                    event_name,
                    additional_event_info, 
                    *regex_or([heap_before_gc, 
                              heap_after_gc, 
                              max_heapsize, 
                              duration_ms],

                              [zgc_heap_before_gc, 
                              zgc_heap_after_gc, 
                              zgc_max_heapsize])], 

                    [safepoint_name,
                     safepoint_time_since_last, 
                     safepoint_time_to_reach, 
                     time_at_safepoint, 
                     total_time_safepoint],

                    [program_pause_time, time_to_stop_application]
                )
    ]
    # Transform from a list of tuples, into 3 distinct lists. They are initally connected for readability
    regex_groups, column_names, data_types = [], [], []
    for capture_group in combined_groups:        
        regex_groups.append(capture_group[0])
        if capture_group[1]:
            column_names.append(capture_group[1])
        if capture_group[2]:
            data_types.append(capture_group[2])
    capture_string = "".join(regex_groups)

    # Return 3 distinct lists. 
    return capture_string, column_names, data_types
    
# Any number of words between min_num and max_num can be captured.
# Helps clarify what is being captured.
def words(min_num, max_num):
    return "(?:\w+ ?){" + str(min_num) + "," + str(max_num) + "}"


#   regex_or 
#
#   Takes some number of lists, representing tuples of (regex, column name, datatype),
#   and modified the regex to include or statements between each list.
#
#   each passed in list will be put in a non capture group. The entire expression returned
#   will be put in a non-capture group.
def regex_or(*groups):
    # each group is a list of tuples
    
    groups = list(groups)
    groups[0] = set_noncapture(groups[0])
    for idx in range(1, len(groups)):
        groups[idx] = set_noncapture(groups[idx])
        groups[idx] = add_front("|", groups[idx])

    first_term = groups[0][0]
    last_term  = groups[-1][-1]
    first_term_regex = "(?:" + first_term[0]
    last_term_regex  = last_term[0]  + ")"
    groups[0][0] = (first_term_regex, groups[0][0][1], groups[0][0][2])
    groups[-1][-1] = (last_term_regex, groups[-1][-1][1], groups[-1][-1][2])
    combined_groups = []
    for group in groups:
        for regex_tuple in group:
            combined_groups.append(regex_tuple)
    return combined_groups

#       set_noncapture
#   
#   Takes a list of terms, and combines them into one large non-capture group
#
def set_noncapture(terms):
    # Terms is a list containing multiple tuples of (regex, col, datatype.)
    # Change the first item in the list and the last item to turn
    # the entire list into a single non=capture group
    terms[0] = ("(?:" + terms[0][0], terms[0][1], terms[0][2])
    terms[-1] = (terms[-1][0] + ")", terms[-1][1], terms[-1][2])
    return terms

#       add_front
#
#       adds chars to the first term in the list.
#
def add_front(chars, terms):
    new_term = (chars + terms[0][0], terms[0][1], terms[0][2])
    terms[0] = new_term
    return terms


####### this function returns the same as 'get_parsing_groups()'. Also useful for reference. CURRENTLY NOT CALLED.
def better_parsing():
    STRING ='''^(?:(?:\[(\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d\.\d{3}[+-]\d{4})\])|(?:\[([\d\.]+)((?:s)|(?:ms)|(?:ns))\]))((?:\[.*?\])*)(?:(?: GC\((\d+)\) ((?:Pause(?=.*ms))|(?:Concurrent(?=.*ms))|(?:Garbage Collection)) (?:((?:\w+ ?){1,4}) )?((?:\((?:\w+ ?){1,3}\) ){0,3})(?:(?:(?:(\d+)\w->(\d+)\w(?:\((\d+)\w\)?)?)?(?= ?(\d+\.\d+)ms))|(?:(\d+)\w\(\d+%\)->(\d+)\w\((\d+)%\))))|(?: Safepoint "(\w+)", Time since last: (\d+) ns, Reaching safepoint: (\d+) ns, At safepoint: (\d+) ns, Total: (\d+) ns$)|(?: Total time for which application threads were stopped: ([\d\.]+) seconds, Stopping threads took: ([\d\.]+) seconds$))'''
    COLUMN_NAMES = [ 'DateTime', 'Time', "TimeUnit", "Other fields", 'GCIndex', 'EventType', 'EventName', 'AdditionalEventInfo',  'HeapBeforeGC', 'HeapAfterGC', 'MaxHeapsize',  'Duration_milliseconds',  'HeapBeforeGC', 'HeapAfterGC', 'MaxHeapsize', 'SafepointName', 'TimeFromLastSafepoint_ns', 'TimeToReachSafepoint_ns', 'AtSafepoint_ns', 'TotalTimeAtSafepoint_ns', 'TotalApplicationThreadPauseTime_seconds', 'TimeToStopApplication_seconds']
    DATA_TYPES = [str,float,str,str, int, str, str, str,  float, float, float,  float,  float, float, float, str, float, float, float, float, float, float]
    return STRING, COLUMN_NAMES, DATA_TYPES