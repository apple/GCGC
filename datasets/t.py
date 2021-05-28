max = 20000
count = 0
with open("./gc.log", "r") as file:
    with open("./medium_gc.log", "w") as file_out:
        d = file.readlines()
        for line in d:
            count += 1
            file_out.write(line)
            if (count >= max):
                break