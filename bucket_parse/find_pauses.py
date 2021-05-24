# Purpose:  Find all GC pause (young) in a given filename as argument 1
import sys

def usage():
    if (len(sys.argv)) < 3:
        print("Sorry, please rerun using " + str(sys.argv[0])
        + " <filename> <output_data filename>")
        quit()

def parse_file(filename_in, filename_out):
    file = open(filename_in, "r")
    output_file = open(filename_out, "w")
    pauses = []
    for line in file:
        if "Pause Young" in line:
            output_file.write(line)

def main():
    usage()
    parse_file(sys.argv[1], sys.argv[2])



main()