import golly as g
import os

directory_path = "./patterns/"
filenames = [f for f in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, f))]

def get_rule(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
        if len(lines) > 1:
            return lines[1].lstrip('#').strip()
    return None

i = 0
for file in filenames:
    i = i + 1
    full = directory_path + file
    g.open(full)
    rule = get_rule(full)
    print(full)
    g.setrule(rule)
    g.save("./rles/pattern"+str(i)+".rle","rle")
    g.update()
