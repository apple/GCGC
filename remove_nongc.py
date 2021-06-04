with open("/Users/ellisbrown/Desktop/JFR_folder/temp_out", "r") as file:
    with open("./datasets/linux_ubuntu.log", "w") as out:
        data = file.readlines()
        for line in data:
            if line[0] == "[":
                out.write(line)
                