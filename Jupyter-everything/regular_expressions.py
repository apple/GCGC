
###  Getting the groups out of any line. 
        # group 1 : (DATE-TIME)
        # group 2 : (TIME FROM START)
        # group 3 : (info/debug/...) 
        # group 4 : (gc, phases, ...)
        # group 5: (everything else on that line)
#[0.549s][debug][gc,phases    ] GC(0)     Code Roots Fixup: 0.0ms
#[2020-11-16T14:54:16.417+0000][0.015s][trace][gc,task      ] WorkerManager::add_workers() : created_workers: 1
line_parse = '/\[*(.*)\]*\[\d+\.\d+\w+\]\[(.*)\[(.*)\](.*)/gm'
        #     ^                                           ^^^
        #     things with arrows probably not needed for re expression   


### Getting INITAL information from multiple heap logs.
'''example 1: From this log'''

Using G1
Version: 16.0.1+9 (release)
CPUs: 16 total, 16 available
Memory: 65536M
Heap Region Size: 8M
Heap Min Capacity: 8M
Heap Initial Capacity: 1G
Heap Max Capacity: 16G

'''example 2: From this log'''

MarkStackSize: 4096k  MarkStackSizeMax: 16384k
Heap region size: 4M
Minimum heap 12582912000  Initial heap 12582912000  Maximum heap 12582912000


# Start with top log.
pattern = "Heap\sMin\sCapacity:\s*(.+)\s|Heap\sRegion Size:\s(.+)\s|Heap\sInitial Capacity:\s(.+)\s|Heap\sMax\sCapacity:\s(.+)\s|Initial\sheap\s(\d+\w*)\s|Heap\sregion\ssize:\s(.+)\s|Minimum\sheap\s(\d+)\s|Maximum\sheap\s(\d+)\s"
# Groups: 
# 2 || 6 : Heap Region Size
# 1 || 7  : Heap Min Capacity
# 3 || 5 : Heap Initial Capacity
# 4 || 0 : Heap Max Capacity