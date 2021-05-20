#### Purpose: Taken in the actions specified by the logs, and do something
#### to find the similarity between all. Use using a threshold hash table.
# Ellis Brown, 5/20/2021

import sys
from collections import defaultdict
from difflib import SequenceMatcher


def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()


f = open(sys.argv[1], "r")
file = f.readlines()
f.close()

hash_table = defaultdict(list)

for line in file:
    current_key = line[:10]
    
    if current_key in hash_table:
        hash_table[current_key].append(line)
        
    else:
        found = False
        for key in hash_table:
            if similar(key, current_key) >= 0.85:
                hash_table[key].append(line)
                found = True
                break
        if not found:
            hash_table[current_key].append(line)

for key in hash_table:
    print(str(hash_table[key]) + "\n")


