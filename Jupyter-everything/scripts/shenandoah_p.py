## # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#                               PauseInitMark
#   Purpose:
#       Finds the timing associated with Initial pause at the beginning of GC
#   
#   Return:
#       A regex searchable string for this particular field
# 
#   Regex Group Info
#       1) Time spent
#
##  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
def PauseInitMark():
    return "Pause Init Mark(?: \([\w ]*?\)){0,2}() (\d+\.\w+)"

#   Regex Group Info
#       1) Time spent
def PauseFinalMark():
    return "Pause Final Mark(?: \([\w ]*?\)){0,2}() (\d+\.\w+)"

#   Regex Group Info
#       1) Time spent
def PauseInitUpdateRefs():
    return "Pause Init Update Refs() (\d+\.\d+\w+)"

#   Regex Group Info
#       1) Time spent
#       2) Nothing 
def PauseFinalUpdateRefs():
    return "Pause Final Update Refs() (\d+\.\d+\w+)"

#   Regex Group Info
#       1) Change in memory allocation
#       2) Time spent
def PauseDegeneratedGC():
    return "Pause Degenerated GC(?: \([\w ]*?\)){0,2} (\d+\w->\d+\w\(?\d+?\w?\)?) (\d+\.\d+\w+)"


#   Regex Group Info
#       1) Change in memory allocation
#       2) Time spent
def PauseFull():
    return "Pause Full(?: \([\w ]*?\)){0,2} (\d+\w->\d+\w\(?\d+?\w?\)?) (\d+\.\d+\w+)"


## # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#                               lineMetadata
#   Purpose:
#       Parse an entire log line, and extract each and only the metadata 
#   
#   Return:
#       A regex searchable string for this particular field
# 
#   Regex Group Info
#       1) DateTime information (if present)
#       2) Time since program began (integer with a metric unit)
#       3) Reason for log entry [info/debug/...]
#       4) gc phase
#
##  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
def lineMetadata():
    #return  '^\[*(.*)\]*\[(\d+\.\d+\w+)\]\[(.*)\]\[(.*)\].*\s*'
    return '^(\[\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d\.\d{3}\+\d{4}\])?\[(\d+\.\d+\w+)\]\[(\w+ ?)\]\[gc(\w+,?){0,2}\s*\] GC\(\d+\) '

def pauses():
    return [lineMetadata() + PauseInitMark(),
            lineMetadata() + PauseFinalMark(),
            lineMetadata() + PauseInitUpdateRefs(),
            lineMetadata() + PauseFinalUpdateRefs(),
            lineMetadata() + PauseDegeneratedGC(),
            lineMetadata() + PauseFull()]
def Concurrent():
    return "Concurrent((?: \w+){1,3}) (\d+\w->\d+\w\(?\d+?\w?\)?){0,1}(\((?:\w+ ?){0,2}\))? ?(\d+\.\d+)ms"

def ConcurrentLine():
    return lineMetadata() + Concurrent()
