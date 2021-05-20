# Goal: Better understand the output log,
#       by analyzing the sub categories produced.
#
# Goal: Become more fluent using Apple computer, VSCode IDE.


# Purpose: Simple parsing of gc log file, @info level.
# Ellis Brown, 5/19/2021
import sys

# TODO: 
#       Update documentation
#       Verify correctness on edge cases
#       Update handling of command line arguments




def usage():
    if (len(sys.argv)) < 4:
        print("Sorry, please rerun using " + str(sys.argv[0]
        + " <filename> <debug mode> <output csv filename>"))
        quit()


def read_file():
    log = open(sys.argv[1], mode="r") # Everyone LOVES hard coded in files <3
    log_data = log.readlines()

    #count = 0 # used for small testing

    for idx, line in enumerate(log_data):
        start, end = read_header(line, idx)
        add_row_to_table(line, start, end)
        # count += 1
        # if count == 45 and debug_mode:
        #     log.close()
        #     return

    log.close()

# Takes a line, and a specified char. Returns all indicies of that char
# in the specified lines. Max indicies count = 4.
def get_indicies_of_chars(line, char_in):
    data_out = []
    for idx, char in enumerate(line):
        if char_in == char:
            data_out.append(idx)
        if len(data_out) == 4:
            break
    return data_out


# Purpose: Verifies that a set of tags from reading a line is CORRECT, 
# and ready to be parsed.
# Note: This should only be run once, on the entire log file, just to verify 
#       that the file is a valid log.
# TODO : failure mode should be handeled appropriately : probably just ignore this line
# and print to the error screen, and generate "log" of output errors.

def verify_valid_tag(start_tag, end_tag):
    if (len(start_tag) != len(end_tag)):
        if (debug_mode):
            print("Error! Invalid tag set")
        quit()                                  # exit failure mode. Revisit
    for i in range(len(start_tag)):
        if (start_tag[i] >= end_tag[i]):
            if debug_mode:
                print("Error! Invalid tag set")
            quit()  

# Purpose: Given a line, find the time stamp, type of error, task, and info.
#          sort that information into the approriate cateogory.
#
# TODO: Use index information for generation of output log for incorrect lines

def read_header(line, idx):
    start_tag = get_indicies_of_chars(line, "[")
    end_tag = get_indicies_of_chars(line, "]")
    #verify_valid_tag(start_tag, end_tag)
    return start_tag, end_tag
    # now that we have the headers, we can progress to adding them to a hash table.

def add_row_to_table(line, start, end):
    if len(start) == 4:
        for i in range(len(start)):
            data_table[i].append(line[int(start[i] + 1):int(end[i])])
        
        data_table[4].append(line[end[i]+ 1:])
    else:
        data_table[4][-1] += (line)

def main():
    if (debug_mode):
        print("Run " + str(sys.argv[0]) + " with:")
        for i in range(len(sys.argv) - 1 ):
            print(sys.argv[i + 1])
    read_file()
    create_csv()


def create_csv():
    
    filename = sys.argv[3] 
    with open(filename, "w") as ofile:
        for row in range(len(data_table[0])):
            for col in range(len(data_table) - 1):
                ofile.write(data_table[col][row] + "|")
            # special case, don't add on the vertical line for last column.
            ofile.write(data_table[4][row] + "\n")

def print_info():
    for row in range(len(data_table[0])):
        for col in range(len(data_table)):
            print(data_table[col][row], end = " ")
        print("")

usage()
# data_table & debug_mode are global variables used throughout runtime.
data_table = [[],[],[],[],[]]
debug_mode = False
if (sys.argv[2]) in ["True", "true", "t"]:
    debug_mode = True
main()

