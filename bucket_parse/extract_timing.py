import sys

def usage():
    if (len(sys.argv)) < 3:
        print("Sorry, please rerun using " + str(sys.argv[0])
        + " <filename> <output_csv filename>")
        quit()

def extract_data(filename, target_string):
    
    file = open(filename, "r")
    timing = []
    str_len = len(target_string)
    for line in file:
        if target_string in line:         
            idx = line.index(target_string)
            left = find_index_left(idx, line, ")")            
            right = idx +  line[idx:].index("\n")
            timing.append(line[left + 1 : right - 1])
    return timing

def arrange_tup(timing):
    arr = []
    for row in timing:
        idx = row.index(")")
        tup = (row[idx+2:-1],row[1:idx+1])
        arr.append(tup)
    return arr


def find_trends(s):
    max_wait = max(s, key = lambda i : float(i[0][:-2]))
    #print("Max wait" + str(max_wait))
    total_wait =  round(sum(float(i[0][:-2]) for i in s), 4)
    average_wait = round(total_wait / len(s), 4)
    #print("Total wait: " + str(total_wait))
    #print("Average wait: " + str(average_wait))


def find_index_left(idx, line, char):
    for i in range(idx, 0, -1):
        if line[i] == char:
            return i
    return -1

def main():
    usage()
    timing = extract_data(sys.argv[1], "->")
    unsorted = arrange_tup(timing)
    if (len(unsorted)) == 0:
        print("Length of unsorted is zero...\n")
        quit()
    
    
    s = sorted(unsorted, key=lambda tup: float(tup[0])) # sorts by using tuple[0] as key
    for line in s:
        print(line)
    
    find_trends(s)
    write_to_csv(s, sys.argv[2])

def write_to_csv(data, filename):
    file = open(filename, "w") 
    for line in data:
        file.write(line[0] + str(", ") + line[1] + "\n")
    file.close()

main()