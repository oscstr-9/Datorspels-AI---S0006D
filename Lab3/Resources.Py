import Map
woodList = []
mineralList = []

def findMaterial():
    global woodList
    global mineralList
    for x in range(len(Map.map)):
        for y in range(len(Map.map[x])):
            if Map.map[x][y] == "T":
                woodList.append([x, y, 0])
            if Map.map[x][y] == "I":
                mineralList.append((x, y))

def gatherWood(agent):
    for i in woodList:
        if agent.getPos() == (woodList[i][0], woodList[i][1]):
            woodList[i][2] + 1
            if woodList[i][2] == 5:
                woodlist.pop(i)
                Map.changeMap("t", (woodList[0], woodList[1]))
            return True
        return False

def gatherMinerals(agent):
    for i in mineralList:
        if agent.getPos() == (minrealList[i][0], minrealList[i][1]):
            mineralList.pop(i)
            Map.changeMap("M", (minrealList[0], minrealList[1]))
            return True
        return False
