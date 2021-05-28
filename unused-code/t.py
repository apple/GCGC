max = 11652
count = 0
with open("./long_amzn_workload.log", "r") as file:
    with open("./long_a.log", "w") as file_out:
        d = file.readlines()
        for line in d:
            count += 1
            file_out.write(line)
            if (count >= max):
                break