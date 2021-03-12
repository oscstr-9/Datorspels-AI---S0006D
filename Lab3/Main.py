import Pygame
import FogOfWar
import Agents
import StateManager
import Map
import TimeMultiplier
import BaseManager
import Resources
import StatParser
import random
import copy
import time

agents = []
base = 0

def main():
    global base
    r = ([0, 0, 0], [1, 1, 0], [1, 0, 0], [0, 1, 0], [-1, 1, 0], [1, -1, 0], [-1, 0, 0], [0, -1, 0], [-1, -1, 0])
    StatParser.readStats()
    Map.makeMap()
    startPos = setupStartPos(r)
    FogOfWar.createFogOfWar(startPos)
    FogOfWar.updateFogOfWar(agents)
    Resources.findMaterials()
    Pygame.init()

    for j in range(50):
        if j < 20:
            Agents.addToJobList("woodCutter")
        elif j >= 30 and j < 40:
            Agents.addToJobList("miner")
        elif j >= 40 and j < 46:
            Agents.addToJobList("explorer")
        else:
            Agents.addToJobList("builder")

    for k in range(8):
        if k <= 4:
            base.addToBuildList(["coalFurnace", 0])
        else:
            base.addToBuildList(["smeltery", 0])


    # TimeMultiplier.setTimeMultiplier(int(input("Set a time multiplier: ")))
    TimeMultiplier.setTimeMultiplier(100)

    updateGame()


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

    for i in range(StatParser.statDict["workers"]):
        for next in R:
            if next[2] == 7:
                continue
            agents.append(Agents.agent((startPos[0]+next[0], startPos[1]+next[1]), base, i+1))
            next[2] += 1
            break

    return startPos


def updateGame():
    global base
    worldTimer = time.time()
    while True:
        if Agents.jobList:
            for agent in agents:
                if agent.getRole() == "worker" and Agents.jobList:
                    agent.setJob(Agents.jobList[0])
                    Agents.removeFromJobList()
                    agent.setState(StateManager.upgrading())
                    if not Agents.jobList:
                        break

        for agent in agents:
            agent.state.execute(agent)
        FogOfWar.updateFogOfWar(agents)
        Pygame.drawAgents(agents)
        Pygame.update()
        # whenToDoWhat(worldTimer)



def whenToDoWhat(worldTimer):
    if time.time() - worldTimer >= 10:
        worldTimer = time.time()
        print("Coal: " + str(agents[0].base.getCoal()))
        print("---------------------------------------------")
        print("Iron: " + str(agents[0].base.getIron()))

    if agents[0].base.getCoal() >= 200 and agents[0].base.getIron() >= 20:
        print("Victory!")
        return True

main()