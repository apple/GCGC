# process_log.py

# # # # # # # # # # # # # # # # # # # # # # # # # # # 
# Purpose: Creates functions to process a           #
#          gc log file, extracting information      #
#          of specified types, and returning them.  #
#                                                   #
# Ellis Brown, 5/21/2020                            #
# # # # # # # # # # # # # # # # # # # # # # # # # # #

'''TODO: The following are catogries of information to parse from the log '''
# I would like to be able to produce
# Currently, this assumes usage on "gc1"
    # JVM Memory size
    # (allocated vs peak)
    # Throughput
    # Latency (average pause time, Max pause time)
    # Heap usage after GC
    # Heap usage before GC
    # GC Duration time (over runtime of program, when run? how long run?)
    # Pause GC Duration
    # Reclaimed bytes
    # Young generation allocated space before/after GC
    # Old   generation allocated space before/after GC
    # Allocation and promotion (from young->old)
    # Average time per task compared to all gc tasks
    # Total time (seconds)
    # Memory leaks? 

path= ""

# Set the path to the log file, which will then be parsed for specific 
# attributes.
def setLogPath(p):
    path = p

def getPauses():
    pause_data = []
    with open(path, "r") as file:
        for line in file:
            if "Pause Young" in line:
                pause_data.append(line)
    return extract_pause_metadata(pause_data)

def extract_pause_metadata(pause_data):
    data = []
    timestamps = []
    target_string = "->"
    str_len = len(target_string)
    for line in pause_data:
        if target_string in line:         
            idx = line.index(target_string)
            left = find_index_left(idx, line, ")")            
            right = idx +  line[idx:].index("\n")
            data.append(line[left + 1 : right - 1])
            timestamps.append(get_timestamps(line))
    data = arrange_cols_pauses(data)

#       -> find_index_left
# Purpose: Find the index of a particular character to the left passed idx
# Parameters:
        # (idx)  The starting index to begin searching left from
        # (line) The string of text to search
        # (char) The character you are searching for the index of
# Return: 
        # The first index of the (char) in (line), if found.
        # Else, -1
def find_index_left(idx, line, char):
    for i in range(idx, 0, -1):
        if line[i] == char:
            return i
    return -1

#       -> arrange_cols_pauses
# Purpose: 

def arrange_cols_pauses(data):
    arr = []
    for row in data:
        idx = row.index(")")
        tup = (row[idx+2:-1],row[1:idx+1])
        arr.append(tup)
    return arr