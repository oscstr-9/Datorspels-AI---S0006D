import Agents
import Pygame
import Map
import copy

fogOfWar = 0

def createFogOfWar():
    global fogOfWar
    fogOfWar = copy.deepcopy(Map.map)
    for x in range(len(fogOfWar)):
        for y in range(len(fogOfWar[0])):
            fogOfWar[x][y] = False

def updateFogOfWar(agents, r):
    global fogOfWar
    for agent in agents:
        pos = Agents.agent.getPos(agent)
        if Agents.agent.getRole(agent) == "explorer":
            for neighbour in r:
                fogOfWar[pos[0] + neighbour[0]][pos[1] + neighbour[1]] = True
        else:
            fogOfWar[pos[0]][pos[1]] = True
