def save_line(name="", text=""):
    with open("outputs/"+name, "a") as file:
        file.write(text+'\n')

def get_array_csv(name="")->[]:
    array = []
    blacklist = open("outputs/"+name, "r")
    while blacklist:
        line  = blacklist.readline()
        array.append(line.strip())
        if line == "":
            break
    return array