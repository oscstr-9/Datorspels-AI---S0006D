import Map
woodList = []
woodLeft = []
mineralList = []
mineralLeft = []

# Puts all trees and ores into lists for later
def findMaterials():
    global woodList
    global mineralList
    for x in range(len(Map.map)):
        for y in range(len(Map.map[x])):
            if Map.map[x][y] == "T":
                woodList.append([x, y])
                woodLeft.append([x, y, 0])
            if Map.map[x][y] == "I":
                mineralList.append((x, y))
                mineralLeft.append((x, y))

# Checks if wood can be collected
def gatherWood(agent):
    for i in range(len(woodList)):
        # If agent is standing on wood
        if agent.getPos() == (woodList[i][0], woodList[i][1]):
            treeGone = True
            # If wood has no charges left, change texture and remove from list
            for j in range(len(woodLeft)):
                if woodList[i] == [woodLeft[j][0], woodLeft[j][1]]:
                    treeGone = False
                    break
            if treeGone:
                Map.changeMap("t", (woodList[i][0], woodList[i][1]))
            return True
    return False

# Tells lists that a tree has been found and will be cut down
def treeFound(pos):
    for i in range(len(woodLeft)):
        if pos == (woodLeft[i][0], woodLeft[i][1]):
            woodLeft[i][2] += 1
            if woodLeft[i][2] >= 5:
                woodLeft.pop(i)
            break

# Checks if ores can be collected
def gatherMinerals(agent):
    # If the world is out of ores, become woodcutter
    if not mineralList:
        agent.setJob("woodcutter")
        return False
    # When agent stands on ore and is planning to pick it up, remove it from list and change texture
    for i in range(len(mineralList)):
        if agent.getPos() == (mineralList[i][0], mineralList[i][1]):
            if not agent.getPath():
                Map.changeMap("M", (mineralList[i][0], mineralList[i][1]))
                agent.setInventory("minerals")
            return True
    return False

# Tells lists that an ore has been found and will be collected
def mineralFound(pos):
    for i in range(len(mineralLeft)):
        if pos == mineralLeft[i]:
            mineralLeft.pop(i)
            break

