#### Purpose: Taken in the actions specified by the logs, and do something
#### to find the similarity between all. Use using a threshold hash table.
# Ellis Brown, 5/20/2021

import sys
from collections import defaultdict
from difflib import SequenceMatcher

'''
Parameters: 
argv[1]:    Filename containing lines with 
            interesting data, to find similarities between
others:     none
'''

def main():
    usage() # establish correct arguments called
    
    table = find_matches(open(sys.argv[1], "r"))
    # hash table with lists for values. In time order per list grouping.
    
    print_table(table)


# Takes in a, and hashes each line in the file using 
# the first 10 characters. Then, it finds similar entry characters.
# Returns a hash table with first 10 characters as keys, and lists of lines from
# the file that had the similar first 10 as the values.
def find_matches(f):

    hash_table = defaultdict(list)
    file = f.readlines()
    f.close()
    # For each line in the file, we use case analysis:
    #
    #   Case 1: the current_key is IN the table
    #               -> append to that list.
    #   Case 3: the current_key is NOT in the table
    #               -> Create a new entry to the table. 
    for line in file:
        current_key = line[:3]
        
        if current_key in hash_table:
            hash_table[current_key].append(line)
   
        else:
            # found = False
            hash_table[current_key].append(line)
            # for key in hash_table:
            #     if similar(key, current_key) >= 0.85:
            #         hash_table[key].append(line)
            #         found = True
            #         break

            #  if not found:
            

    return hash_table


# Prints off the different entries of the has table, row by row.
def print_table(hash_table):
    for key in hash_table:
        print(str(hash_table[key]) + "\n")


# Defines the similarity between two strings. Returns a float
# from 0-1, where 0 is no match, 1 is the same string.
def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()


# Defines arguments to call this program from command line. 
# Program quits if called incorrectly.
def usage():
    if len(sys.argv) < 2:
        print("Usage: " + str(sys.argv[1] + " <filename>"))
        quit()


main()