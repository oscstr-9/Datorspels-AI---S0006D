import Agents
import Pathfinder
import Map
import FogOfWar
import time
import random

# These classes all can be used to change the stats of an agent and to get the state name
class explore:
    def execute(self, agent):
        map = Map.map
        fogOfWar = FogOfWar.fogOfWar
        r = ([0, 0, 0], [1, 1, 0], [1, 0, 0], [0, 1, 0], [-1, 1, 0], [1, -1, 0], [-1, 0, 0], [0, -1, 0], [-1, -1, 0])
        path = agent.getPath()
        pos = agent.getPos()
        traverseTime = 10
        woodsFound = False
        WoodsPos = (0, 0)

        for next in r:
            if map[pos[0] + next[0]][pos[1] + next[1]] == "T" and not fogOfWar[pos[0] + next[0] * 2][pos[1] + next[1] * 2]:
                woodsFound = True
                woodsPos = (pos[0] + next[0], pos[1] + next[1])
        if not path and not woodsFound:
            while True:
                goal = [random.randrange(1, 99), random.randrange(1, 99)]
                if not fogOfWar[goal[0]][goal[1]] and map[goal[0]][goal[1]] not in ("B", "V"):
                    agent.setPath(Pathfinder.findPath(agent.getPos(), goal, map))
                    break
                else:
                    goal = [random.randrange(1, 99), random.randrange(1, 99)]
        else:
            if len(agent.getPath()):
                pass

            diff = time.time() - Agents.agent.getTimer(agent)
            if map[pos[0]][pos[1]] == "G":
                traverseTime = 0.5
            else:
                traverseTime = 0.02

            if diff >= traverseTime:
                agent.setTimer(time.time())

                if not woodsFound:
                    agent.setPos(agent.getPath()[0])
                    agent.setPath(agent.popPath())

                else:
                    agent.setPos(woodsPos)
                    agent.setPath([])

class idle:
    def execute(self, agent):
        # Empty
        return

class upgrading:
    def execute(self, agent):
        if agent.getRole() == "worker":
            agent.setTimer(time.time())
            agent.setRole("upgrading")

        diff = time.time() - agent.getTimer()

        if role == "explorer":
            if diff >= 0:
                agent.setRole("explorer")
                agent.setState(explore)

        elif role == "builder":
            if diff >= 60:
                Agents.agent.setRole(agent, "builder")

        elif role == "soldier":
            if diff >= 120:
                Agents.agent.setRole(agent, "soldier")
