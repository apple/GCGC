import sys

def usage():
    if (len(sys.argv)) < 2:
        print("Sorry, please rerun using " + str(sys.argv[0])
        + " <filename>")
        quit()
def parse_file(filename):
    file = open(filename, "r")
    output_file = open("pauses_out", "w")
    pauses = []
    for line in file:
        if "Pause Young" in line:
            output_file.write(line)

def main():
    usage()
    parse_file(sys.argv[1])

main()