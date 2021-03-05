import Agents
import Pygame
import Map
import copy

fogOfWar = 0
fogOfWarList = []

def createFogOfWar():
    global fogOfWar
    global fogOfWarList
    fogOfWar = copy.deepcopy(Map.map)
    for x in range(len(fogOfWar)):
        for y in range(len(fogOfWar[0])):
            fogOfWar[x][y] = False
            fogOfWarList.append((x, y))

def updateFogOfWar(agents, r):
    global fogOfWar
    global fogOfWarList
    for agent in agents:
        pos = Agents.agent.getPos(agent)
        if Agents.agent.getRole(agent) == "explorer":
            for neighbour in r:
                fogOfWar[pos[0] + neighbour[0]][pos[1] + neighbour[1]] = True
                for fog in range(len(fogOfWarList)):
                    if fog == (pos[0] + neighbour[0], pos[1] + neighbour[1]):
                        fogOfWarList.remove(fog)
        else:
            fogOfWar[pos[0]][pos[1]] = True
            for fog in range(len(fogOfWarList)):
                if fog == (pos[0], pos[1]):
                    fogOfWarList.remove(fog)
