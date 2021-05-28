import g1version16 as tre
def find_log_lines():
    with open("/Users/ellisbrown/Desktop/Project/datasets/medium_gc.log") as file:
        data = file.readlines()
    print("Hello world!")
    table = tre.manyMatch_LineSearch([tre.fullLineInfo()], 5, data)
    for column in table:
        print(column)
find_log_lines()