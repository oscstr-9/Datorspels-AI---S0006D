import Agents
import Pathfinder
import Map
import FogOfWar
import TimeMultiplier
import Resources
import BaseManager
import time
import random

class explore:
    def execute(self, agent):
        map = Map.map
        pos = agent.getPos()
        traverseTime = 10

        # Delay walking speed
        diff = (time.time() - Agents.agent.getTimer(agent)) * TimeMultiplier.timeMultiplier
        if map[pos[0]][pos[1]] in ("G", "T", "t"):
            traverseTime = 20
        else:
            traverseTime = 10

        if diff >= traverseTime:
            agent.setTimer(time.time())

            # Set/declare variables
            fogOfWar = FogOfWar.fogOfWar
            fogOfWarList = FogOfWar.fogOfWarList
            r = ([0, 0, 0], [1, 1, 0], [1, 0, 0], [0, 1, 0], [-1, 1, 0], [1, -1, 0], [-1, 0, 0], [0, -1, 0], [-1, -1, 0])
            path = agent.getPath()
            woodsFound = False
            WoodsPos = (0, 0)

            # Check if neighbour is tree and close to fog of war
            for next in r:
                if map[pos[0] + next[0]][pos[1] + next[1]] == "T" and not fogOfWar[pos[0] + (next[0] * 2)][pos[1] + (next[1] * 2)]:
                    woodsFound = True
                    woodsPos = (pos[0] + next[0], pos[1] + next[1])
                    break

            # If has no path, get random finish in unexplored area
            if not woodsFound:
                if not fogOfWarList:
                    agent.setState(idle())
                if not path:
                    index = random.randrange(0, len(fogOfWarList)-1)
                    goal = fogOfWarList[index]
                    agent.setPath(Pathfinder.findPath(agent, goal))
                else:
                    agent.setPos(agent.getPath()[0])
                    agent.setPath(agent.popPath())

                # If woods found, discard path and walk that way
            else:
                if agent.getPath() != []:
                    agent.setPath([])
                agent.setPos(woodsPos)

class idle:
    def execute(self, agent):
        # Empty
        return

class locateMaterials:
    def execute(self, agent):
        if agent.getJob() == "woodcutter":
            self.findWood(agent)

        elif agent.getJob() == "miner":
            self.findMinerals(agent)

    def findWood(self, agent):
        woodPrioList = []
        pos = agent.getPos()
        # Add all trees in the world and sort by closeness to spawn
        for tree in Resources.woodLeft:
            if FogOfWar.fogOfWar[tree[0]][tree[1]]:
                woodPrioList.append((tree[0], tree[1], abs(tree[0] - pos[0]) + abs(tree[1] - pos[1])))
        woodPrioList.sort(key=lambda x: x[2])


        # If agent has no path, go to closest found tree
        if not agent.getPath() and woodPrioList:
            agent.setPath(Pathfinder.findPath(agent, (woodPrioList[0][0], woodPrioList[0][1])))
            Resources.treeFound((woodPrioList[0][0], woodPrioList[0][1]))

        elif agent.getPath():
            self.move(agent, pos)

            if Resources.gatherWood(agent):
                agent.setTimer(time.time())
                agent.setState(woodCutting())

    def findMinerals(self, agent):
        mineralPrioList = []
        pos = agent.getPos()
        # Add all ores in the world and sort by closeness to spawn
        for ore in Resources.mineralLeft:
            if FogOfWar.fogOfWar[ore[0]][ore[1]]:
                mineralPrioList.append((ore[0], ore[1], abs(ore[0] - pos[0]) + abs(ore[1] - pos[1])))
        mineralPrioList.sort(key=lambda x: x[2])


        # If agent has no path, go to closest found ore
        if not agent.getPath() and mineralPrioList:
            agent.setPath(Pathfinder.findPath(agent, (mineralPrioList[0][0], mineralPrioList[0][1])))
            Resources.mineralFound((mineralPrioList[0][0], mineralPrioList[0][1]))

        elif agent.getPath():
            self.move(agent, pos)

            if Resources.gatherMinerals(agent):
                agent.setTimer(time.time())
                agent.setState(returnHome())

    def move(self, agent, pos):
        diff = (time.time() - agent.getTimer()) * TimeMultiplier.timeMultiplier
        if Map.map[pos[0]][pos[1]] in ("G", "T", "t"):
            traverseTime = 20
        else:
            traverseTime = 10

        if diff >= traverseTime:
            agent.setTimer(time.time())
            agent.setPos(agent.getPath()[0])
            agent.setPath(agent.popPath())


class woodCutting():
    def execute(self, agent):
        diff = (time.time() - agent.getTimer()) * TimeMultiplier.timeMultiplier
        agent.setLocked(True)
        if diff >= 30:
            agent.setInventory("wood")
            agent.setTimer(time.time())
            agent.setLocked(False)
            agent.setState(returnHome())


class returnHome():
    def execute(self, agent):
        pos = agent.getPos()
        if agent.getPath() == []:
            agent.setPath(Pathfinder.findPath(agent, agent.base.getPos()))
        else:
            diff = (time.time() - Agents.agent.getTimer(agent)) * TimeMultiplier.timeMultiplier
            if Map.map[pos[0]][pos[1]] in ("G", "T", "t"):
                traverseTime = 20
            else:
                traverseTime = 10

            if diff >= traverseTime:
                agent.setTimer(time.time())
                agent.setPos(agent.getPath()[0])
                agent.setPath(agent.popPath())

                if agent.getPos() == agent.base.getPos():
                    agent.setPath([])
                    if agent.getInventory() == "wood":
                        agent.base.addWood()
                    elif agent.getInventory() == "minerals":
                        agent.base.addMinerals()

                    agent.setInventory("empty")
                    agent.setState(locateMaterials())

class building:
    def execute(self, agent):
        # Where to build
        # for tiles around spawn:
            # find unused buildable tile

        # What to build
        # get build list from somewhere?

        # When to hire
        # if diff = time left to build  - time to train guy
            # train guy

        # When to tell guy to work
        # building finished, add hired guy to building

        #   When finished go idle until build list has content

        pass

class upgrading:
    def execute(self, agent):
        if agent.getState() == idle():
            agent.setTimer(time.time())
            agent.setLocked(True)

        diff = (time.time() - agent.getTimer()) * TimeMultiplier.timeMultiplier

        if agent.getRole() == "explorer":
            if diff >= 60:
                agent.setState(explore())
                agent.setLocked(False)

        elif agent.getRole() == "builder":
            if diff >= 60:
                agent.setState(build())
                agent.setLocked(False)

        elif agent.getRole() == "soldier":
            if diff >= 120:
                agent.setState(idle())
                agent.setLocked(False)
