# Goal: Better understand the output log,
#       by analyzing the sub categories produced.
#
# Goal: Become more fluent using Apple computer, VSCode IDE.


# Purpose: Simple parsing of gc log file, @info level.

# open the specific test file. Update to use any file.
data_table = []

def read_file():
    log = open("gc.log", mode="r")
    log_data = log.readlines()

    count = 0 

    for idx, line in enumerate(log_data):
        read_header(line, idx)
        count += 1
        if count == 3:
            log.close()
            return

    log.close()

def get_indicies_of_chars(line, char_in):
    data_out = []
    for idx, char in enumerate(line):
        if char_in == char:
            data_out.append(idx)
    return data_out


def read_header(line, idx):
    start_tag = get_indicies_of_chars(line, "[")
    end_tag = get_indicies_of_chars(line, "]")

    
    print(i)
    print("read_header " + str(idx))


def main():
    print("Entering main!")
    read_file()
    #print_info()

main()