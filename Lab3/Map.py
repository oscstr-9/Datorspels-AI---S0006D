import StatParser
import random
map = 0
r = ((1, 1), (1, 0), (0, 1), (-1, 1), (1, -1), (-1, 0), (0, -1), (-1, -1))

# Reads map from map file and make a 2D array where every index is a square on the map.
def makeMap():
    global map
    f = open("Maps/Map.txt", "r")

    # parse map file
    mapLines = f.readlines()
    map = [[] for _ in range(len(mapLines[0]) - 1)]

    for lines in mapLines:
        i = 0
        for c in lines:
            if c == "\r":
                continue
            if c == "\n":
                break
            map[i].append(c)
            i += 1

    generateMinerals(map)

# Generates minerals in random positions on the map
def generateMinerals(map):
    pos = [random.randrange(1, 99), random.randrange(1, 99)]
    for i in range(StatParser.statDict["ores"]):
        while True:
            if map[pos[0]][pos[1]] in ("B", "V", "T"):
                pos = [random.randrange(1, 99), random.randrange(1, 99)]
            else:
                map[pos[0]][pos[1]] = "I"
                pos = [random.randrange(1, 99), random.randrange(1, 99)]
                break

# Changes value of square on the map if something has changed, e.g. mineral was picked up or building was built.
def changeMap(change, pos):
    global map
    map[pos[0]][pos[1]] = change
