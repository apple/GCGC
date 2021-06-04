# Purpose: Take a CSV file of garbae collection information created
#          by zulu, process and output the ms time information
#          NOTE: this may be unspecific, due to the number of significiant digits in the inital time 

import re

def extract_zulu_pauses(filep):
    # MUST BE MANUALLY SET
    inital_value_ms = 27.384

    zulu_pauses = []
    with open(filep, "r") as file:
        data = file.readlines()
        pattern = '"(\d+) ticks"\s*'
        match = re.search(pattern, data[0])
        if match:
            ticks_per_ms = float(match.group(1)) / inital_value_ms
        else:
            print("No match found")
            return
        for line in data:
            match = re.search(pattern, line)
            if match:
                #print(float(match.group(1)))
                zulu_pauses.append(round(float(match.group(1)) / ticks_per_ms, 3))

    return zulu_pauses

o = extract_zulu_pauses("../datasets/t")
for line in o:
    print(line)