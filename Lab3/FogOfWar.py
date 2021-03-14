import Agents
import Pygame
import Map
import copy

fogOfWar = 0
fogOfWarList = []

# Creates an equally big array to the map containing True and False bools.
# If an index is False then it has yet to be discovered on the map, if True, vice versa.
def createFogOfWar(startPos):
    global fogOfWar
    global fogOfWarList
    fogOfWar = copy.deepcopy(Map.map)
    for x in range(len(fogOfWar)):
        for y in range(len(fogOfWar[0])):
            fogOfWar[x][y] = False

            # Adds all fog of war to a single array for explorers to use when exploring
            if Map.map[x][y] not in ("B", "V"):
                fogOfWarList.append((x, y))

    for next in Map.r:
        fogOfWar[startPos[0]+next[0]][startPos[1]+next[1]] = True

# Updates the fog of war to make every square around an explorer visible to the rest of the agents
def updateFogOfWar(agents):
    global fogOfWar
    global fogOfWarList
    for agent in agents:
        pos = agent.getPos()
        if Agents.agent.getRole(agent) == "explorer":
            for neighbour in Map.r:
                fogOfWar[pos[0] + neighbour[0]][pos[1] + neighbour[1]] = True
                if (pos[0] + neighbour[0], pos[1] + neighbour[1]) in fogOfWarList:
                    fogOfWarList.remove((pos[0] + neighbour[0], pos[1] + neighbour[1]))

