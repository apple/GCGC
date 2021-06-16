from os import listdir
from os.path import isfile, join

onlyfiles = [f for f in listdir("./") if isfile(join("./", f))]
print(onlyfiles)
for filename in onlyfiles:
    with open(filename, "r") as file:

        data = file.readlines()
        i = 0
        for i in range(len(data)):
            reading = False
            opened = False
            closed = False
            if "def " in data[i]:
                print(filename + "\t|\t" + data[i], end="")
