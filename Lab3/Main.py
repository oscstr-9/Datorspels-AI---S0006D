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

# The main function. Initialises useful functions and adds important data to some arrays so the AI knows what to do.
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

    # Adds jobs to the job list for workers to be assigned to.
    for j in range(StatParser.statDict["workers"]):
        if j < 30:
            Agents.addToJobList("woodCutter")
        elif j >= 30 and j < 40:
            Agents.addToJobList("miner")
        elif j >= 40 and j < 46:
            Agents.addToJobList("explorer")
        else:
            Agents.addToJobList("builder")

    # Adds some buildings to the build list so the builders know what to build.
    for k in range(8):
        if k < 6:
            base.addToBuildList(["coalFurnace", 0])
        else:
            base.addToBuildList(["smeltery", 0])


    # Allows user to speed up the application (can be laggy).
    TimeMultiplier.setTimeMultiplier(int(input("Set a time multiplier: ")))
    # Allows the user to choose if they want debug info to be displayed or not
    debug = input("Debug info y/n?: ")
    if debug == "y":
        debug = True
    else:
        debug = False

    # Runs and times update to see how long it took for the AI to complete the wanted task
    gameStart = time.time()
    if updateGame(debug):
        print("Time to finish: " + str((time.time() - gameStart) * TimeMultiplier.timeMultiplier))
        return True

# Gets a random position on the map and checks if it's possible to spawn there.
# Spawns workers around spawning area and sets base position to spawn position.
def setupStartPos(r):
    global base
    map = Map.map
    R = copy.deepcopy(r)
    redo = True

    # Finds suitable spawning area
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

    # Spawn workers around spawning area
    for i in range(StatParser.statDict["workers"]):
        for next in R:
            if next[2] == 7:
                continue
            agents.append(Agents.agent((startPos[0]+next[0], startPos[1]+next[1]), base, i+1))
            next[2] += 1
            break

    return startPos

# Keeps the application updated by running pygame and checking triggers like
# jobs being available and if victory requirements have been met.
def updateGame(debug):
    global base
    while True:
        Pygame.update()

        # Checks job list for available jobs and assigns them to workers.
        if Agents.jobList:
            for agent in agents:
                if agent.getRole() == "worker" and agent.getState() != "upgrading":
                    agent.setJob(Agents.jobList[0])
                    Agents.removeFromJobList()
                    agent.setState(StateManager.upgrading())
                    if not Agents.jobList:
                        break

        # Executes the agents current state
        for agent in agents:
            agent.state.execute(agent)

        FogOfWar.updateFogOfWar(agents)
        Pygame.drawAgents(agents)

        # Checks if victory requirements have been met.
        if agents[0].base.getCoal() >= 200 and agents[0].base.getIron() >= 20:
            print("Victory!")
            return True
        if debug:
            infoPrints()



on = True
worldTimer = 3

# Prints useful information for debugging on a 3 second timer.
def infoPrints():
    global on
    global worldTimer

    if not on:
        worldTimer = time.time()
        on = True
    if time.time() - worldTimer >= 3:
        on = False
        worldTimer = time.time()
        print("Wood: " + str(agents[0].base.getWood()))
        print("---------------------------------------------")
        print("Ore: " + str(agents[0].base.getMinerals()))
        print("---------------------------------------------")
        print("Coal: " + str(agents[0].base.getCoal()))
        print("---------------------------------------------")
        print("Iron: " + str(agents[0].base.getIron()))
        print("---------------------------------------------")

        i = 0
        j = 0
        k = 0
        l = 0
        m = 0
        n = 0
        o = 0
        for agent in agents:
            if agent.getJob() == "woodCutter":
                i += 1
            elif agent.getJob() == "miner":
                j += 1
            elif agent.getRole() == "builder":
                k += 1
            elif agent.getRole() == "explorer":
                l += 1
            elif agent.getRole() == "smelteryWorker":
                m += 1
            elif agent.getRole() == "coalWorker":
                n += 1
            o += 1

        print("woodCutter: " + str(i))
        print("miner: " + str(j))
        print("builders: " + str(k))
        print("explorers: " + str(l))
        print("smelteryWorkers: " + str(m))
        print("coalWorkers: " + str(n))
        print("Total amount of agents: " + str(o))
        print("---------------------------------------------")
        print(base.getBuildList())
        print("---------------------------------------------")
        print("\n")


main()