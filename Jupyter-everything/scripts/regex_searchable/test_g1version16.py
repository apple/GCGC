import g1version16 as tre
def find_log_lines():
    with open("/Users/ellisbrown/Desktop/Project/datasets/amzn_workload_4.log") as file:
        data = file.readlines()
    print("Hello world!")
    table = tre.manyMatch_LineSearch([tre.fullLineInfo()], 5, data)
    simple = []
    for line in table[-1]:
        simple.append(line.strip())

    search_terms = [tre.HeapMinCapacity(), tre.HeapMaxCapacity(), tre.HeapRegionSize()]
    search_titles = ["Min Cap", "Max Cap", "Region"]
    searched = tre.singleMatch_LineSearch(search_terms, simple, search_titles)
    print(searched)
    #print(simple)

find_log_lines()