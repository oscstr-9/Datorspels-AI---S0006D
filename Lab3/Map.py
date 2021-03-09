import random
map = 0

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

def generateMinerals(map):
    pos = [random.randrange(1, 99), random.randrange(1, 99)]
    for i in range(60):
        while True:
            if map[pos[0]][pos[1]] in ("B", "V", "T"):
                pos = [random.randrange(1, 99), random.randrange(1, 99)]
            else:
                map[pos[0]][pos[1]] = "I"
                pos = [random.randrange(1, 99), random.randrange(1, 99)]
                break

def changeMap(change, pos):
    global map
    map[pos[0]][pos[1]] = change
