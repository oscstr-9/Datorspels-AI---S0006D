import Agents
import Pygame
import Map
import copy

fogOfWar = 0
fogOfWarList = []

def createFogOfWar(startPos):
    global fogOfWar
    global fogOfWarList
    fogOfWar = copy.deepcopy(Map.map)
    for x in range(len(fogOfWar)):
        for y in range(len(fogOfWar[0])):
            fogOfWar[x][y] = False
            if Map.map[x][y] not in ("B", "V"):
                fogOfWarList.append((x, y))

    for next in Map.r:
        fogOfWar[startPos[0]+next[0]][startPos[1]+next[1]] = True

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

