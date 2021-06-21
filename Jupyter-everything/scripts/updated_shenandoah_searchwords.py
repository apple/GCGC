# Search terms to parse Shenandoah style logs
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


def PauseDegeneratedGC():
    return "Pause Degenerated GC(?: \([\w ]*?\)){0,2} (\d+\w->\d+\w\(?\d+?\w?\)?) (\d+\.\d+\w+)"


def Concurrent():
    return "Concurrent((?: \w+){1,3}) (\d+\w->\d+\w\(?\d+?\w?\)?){0,1}(\((?:\w+ ?){0,2}\))? ?(\d+\.\d+)ms"


def experimentPauses():

    return "((?:Concurrent)|(?:Pause)) ((?:\w+ ?){1,3}) (\d+\w->\d+\w\(?\d+?\w?\)?){0,1}(\((?:\w+ ?){0,2}\))? ?(\d+\.\d+)ms"


import g1version16 as g

# import shenandoah_p as s

data = g.manyMatch_LineSearch(
    match_terms=[g.lineMetadata() + experimentPauses()],  # regex terms to search for
    num_match_groups=8,
    filepath="/Users/ellisbrown/Desktop/Project/datasets/gc-many/shenandoah_log.log",  # filepath of file to read
    in_file=True,
)
for line in data:
    print(line)
    print("\n\n")
