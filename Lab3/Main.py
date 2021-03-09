import Pygame
import FogOfWar
import Agents
import StateManager
import Map
import TimeMultiplier
import BaseManager
import Resources
import random
import copy

agents = []
base = 0

def main():
    global base
    r = ([0, 0, 0], [1, 1, 0], [1, 0, 0], [0, 1, 0], [-1, 1, 0], [1, -1, 0], [-1, 0, 0], [0, -1, 0], [-1, -1, 0])
    Map.makeMap()
    startPos = setupStartPos(r)
    FogOfWar.createFogOfWar(startPos, r)
    FogOfWar.updateFogOfWar(agents, r)
    Resources.findMaterials()
    Pygame.init()

    # TimeMultiplier.setTimeMultiplier(int(input("Set a time multiplier: ")))
    TimeMultiplier.setTimeMultiplier(50)

    for i in range(25):
        if i < 5:
            agents[i].setState(StateManager.upgrading())
            agents[i].setRole("explorer")
        elif i >= 5 and i < 15:
            agents[i].setState(StateManager.locateMaterials())
            agents[i].setJob("woodcutter")
        else:
            agents[i].setState(StateManager.locateMaterials())
            agents[i].setJob("miner")


    updateGame(r)


def setupStartPos(r):
    global base
    map = Map.map
    R = copy.deepcopy(r)
    redo = True
    while redo:
        startPos = (random.randrange(1, 99), random.randrange(1, 99))
        for neighbour in R:
            if map[startPos[0] + neighbour[0]][startPos[1] + neighbour[1]] in ("B", "V", "T", "I"):
                redo = True
                break
            else:
                redo = False

    map[startPos[0]][startPos[1]] = "S"
    base = BaseManager.base(startPos)

    for i in range(50):
        for next in R:
            if next[2] == 7:
                continue
            agents.append(Agents.agent((startPos[0]+next[0], startPos[1]+next[1]), base))
            next[2] += 1
            break

    return startPos

def updateGame(r):
    while True:
        for agent in agents:
            agent.state.execute(agent)

        FogOfWar.updateFogOfWar(agents, r)
        Pygame.drawAgents(agents)
        Pygame.update()

main()