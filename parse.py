# Goal: Better understand the output log,
#       by analyzing the sub categories produced.
#
# Goal: Become more fluent using Apple computer, VSCode IDE.


# Purpose: Simple parsing of gc log file, @info level.
# Ellis Brown, 5/19/2021

# open the specific test file. Update to use any file.
import sys

import time
## Timing test start ###
startTime = time.time()

# Global varaibles : used through runtime #
data_table = []
debug_mode = False
#### Set up debug mode ### 
if len(sys.argv) >= 2:
    if sys.argv[1] in ["True", "true", "t"]:
        debug_mode = True


def read_file():
    log = open("gc.log", mode="r") # Everyone LOVES hard coded in files <3
    log_data = log.readlines()

    #count = 0 # used for small testing

    for idx, line in enumerate(log_data):
        read_header(line, idx)
        # count += 1
        # if count == 45 and debug_mode:
        #     log.close()
        #     return

    log.close()

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
    if debug_mode:
        print(start_tag)
        print(end_tag)
        print("read_header " + str(idx))
    verify_valid_tag(start_tag, end_tag)



def main():
    print(sys.argv)
    print("Entering main!")
    read_file()
    print("Finished running proram")
    #print_info()

main()

### Timing test end ###
executionTime = (time.time() - startTime)
print("\n\nExecution time in seconds: " + str(executionTime) + "\n\n")