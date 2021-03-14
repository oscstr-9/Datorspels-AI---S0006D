statDict = {}

# Reads all set values for agents, buildings, minerals and trees from stats file
def readStats():
    f = open("stats.txt", "r")
    # parse map file
    statLines = f.readlines()
    global statDict
    for line in statLines:
        if line[0] not in ("\n", "#"):
            entry = line.split(":")
            statDict[str(entry[0])] = int(entry[1])