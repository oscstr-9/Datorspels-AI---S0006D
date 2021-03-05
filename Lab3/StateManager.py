import Agents
import Pathfinder
import Map
import FogOfWar
import TimeMultiplier
import Resources
import BaseManager
import time
import random

priorityList = []

class explore:

    def execute(self, agent):
        map = Map.map
        fogOfWar = FogOfWar.fogOfWar
        fogOfWarList = FogOfWar.fogOfWarList


        r = ([0, 0, 0], [1, 1, 0], [1, 0, 0], [0, 1, 0], [-1, 1, 0], [1, -1, 0], [-1, 0, 0], [0, -1, 0], [-1, -1, 0])
        path = agent.getPath()
        pos = agent.getPos()
        traverseTime = 10
        woodsFound = False
        WoodsPos = (0, 0)

        # Check if neighbour is tree and close to fog of war
        for next in r:
            if map[pos[0] + next[0]][pos[1] + next[1]] == "T" and not fogOfWar[pos[0] + next[0] * 2][pos[1] + next[1] * 2]:
                woodsFound = True
                woodsPos = (pos[0] + next[0], pos[1] + next[1])

        # If has no path, get random finish in unexplored area
        if not path and not woodsFound:
            while True:
                index = random.randrange(1, len(fogOfWarList)-1)
                goal = fogOfWarList[index]
                # If goal not in unwalkable tile
                if map[goal[0]][goal[1]] not in ("B", "V"):
                    agent.setPath(Pathfinder.findPath(agent.getPos(), goal))
                    break
                else:
                    goal = fogOfWarList[random.randrange(1, len(fogOfWarList)-1)]
        else:
            if len(agent.getPath()):
                pass

            # Delay walking speed
            diff = (time.time() - Agents.agent.getTimer(agent)) * TimeMultiplier.timeMultiplier
            if map[pos[0]][pos[1]] in ("G", "T", "t"):
                traverseTime = 20
            else:
                traverseTime = 10

            if diff >= traverseTime:
                agent.setTimer(time.time())

                if not woodsFound:
                    agent.setPos(agent.getPath()[0])
                    agent.setPath(agent.popPath())

                # If woods found, discard path and walk that way
                else:
                    if agent.getPath() != []:
                        fogOfWarList.append(agent.getPath()[len(agent.getPath())-1])
                    agent.setPos(woodsPos)
                    agent.setPath([])

class idle:
    def execute(self, agent):
        # Empty
        return

class findWood:
    def execute(self, agent):
        global priorityList
        pos = agent.getPos()
        if priorityList == []:
            # Add all trees in the world and sort by closeness to spawn
            for tree in Resources.woodList:
                priorityList.append((tree[0], tree[1], abs(tree[0] - pos[0]) + abs(tree[1] - pos[1])))
            priorityList.sort(key=lambda x: x[2])

        # If agent has no path, go to closest found tree
        if not agent.getPath():
            agent.setPath(Pathfinder.findPath(agent, priorityList[0]))

        if Map.map[pos[0]][pos[1]] in ("G", "T", "t"):
            traverseTime = 20
        else:
            traverseTime = 10

        if diff >= traverseTime:
            agent.setTimer(time.time())

            agent.setPos(agent.getPath()[0])
            agent.setPath(agent.popPath())

            if Resources.gatherWood(agent):
                agent.setTimer(time.time())
                agent.setState(woodCutting())

class woodCutting():
    def execute(self, agent):
        diff = (time.time() - agent.getTimer()) * TimeMultiplier.timeMultiplier
        agent.setLocked(True)
        if diff >= 30:
            agent.setInventory("wood")
            agent.getTimer(time.time())
            agent.setState(returnHome())

class returnHome():
    def execute(self, agent):
        return

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
