# # # # # # # # # # # # # # # # # # # # #
#   Oragnize.py
#   Ellis Brown   (5/17/2021)
# 
#   Accepts a CSV file that has read 
#   gc log information, and produces the
#   needed chart information about runtime.
#   organizes data in managable way.
# # # # # # # # # # # # # # # # # # # # #

import pandas as pd
import sys


def main():
        
    if (len(sys.argv)) <= 1:
        print("Incorrect usage : Rerun with the filename, and optional flags")
        quit()
    print("Read CSV file " + str(sys.argv[1]))

    #TODO: come up with better names for the columns
    df = pd.read_csv(sys.argv[1], sep="|", names = ["real-time", "time-from-start", "info-type", "gc-info-type", "data"])
    #print(df)
    df.data = remove_leading_spaces(df.data)
    for line in df.data:
        print(line)

def remove_leading_spaces(column):

    new_info_col = []
    for idx in range(len(column)):
        new_info_col.append(column[idx].strip())
        
    return new_info_col

main()