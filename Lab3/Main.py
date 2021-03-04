import Pygame
import FogOfWar
import Agents
import StateManager
import Map
import random

agents = []

def main():
    r = ([0, 0, 0], [1, 1, 0], [1, 0, 0], [0, 1, 0], [-1, 1, 0], [1, -1, 0], [-1, 0, 0], [0, -1, 0], [-1, -1, 0])
    Map.makeMap()
    FogOfWar.createFogOfWar()
    setupStartPos(r)
    FogOfWar.updateFogOfWar(agents, r)
    Pygame.init()

    for i in range(10):
        agents[i].setState(StateManager.upgrading())
        agents[i].state.execute(agents[i], "explorer")

    while True:
        Pygame.drawAgents(agents)
        Pygame.update()
        for agent in agents:
            if agent.role == "explorer":
                agent.state.execute(agent)
        FogOfWar.updateFogOfWar(agents, r)
        Pygame.drawMap()

def setupStartPos(r):
    map = Map.map
    redo = True
    while redo:
        startPos = [random.randrange(1, 99), random.randrange(1, 99)]
        for neighbour in r:
            if map[startPos[0] + neighbour[0]][startPos[1] + neighbour[1]] in ("B", "V", "T", "I"):
                redo = True
                break
            else:
                redo = False

    map[startPos[0]][startPos[1]] = "S"

    for i in range(50):
        for next in r:
            if next[2] == 7:
                continue
            agents.append(Agents.agent((startPos[0]+next[0], startPos[1]+next[1]), "state"))
            next[2] += 1
            break

main()