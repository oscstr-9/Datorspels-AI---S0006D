import Agents
import Pathfinder
import Map
import FogOfWar
import TimeMultiplier
import Resources
import BaseManager
import StatParser
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
            traverseTime = StatParser.statDict["tsSlowed"]
        else:
            traverseTime = StatParser.statDict["tsGround"]

        if diff >= traverseTime:
            agent.setTimer(time.time())

            # Set/declare variables
            fogOfWar = FogOfWar.fogOfWar
            fogOfWarList = FogOfWar.fogOfWarList
            r =  Map.r
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
                    agent.setState(returnHome())
                elif not path:
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

    def getStateName(self):
        return "explore"

class locateMaterials:
    def execute(self, agent):
        if agent.getJob() == "woodCutter":
            self.findWood(agent)

        elif agent.getJob() == "miner":
            self.findMinerals(agent)

    def findWood(self, agent):
        woodPrioList = []
        pos = agent.base.getPos()
        # Add all trees in the world and sort by closeness to spawn
        for tree in Resources.woodLeft:
            if FogOfWar.fogOfWar[tree[0]][tree[1]]:
                woodPrioList.append((tree[0], tree[1], abs(tree[0] - pos[0]) + abs(tree[1] - pos[1])))
        woodPrioList.sort(key=lambda x: x[2])
        print (woodPrioList)


        # If agent has no path, go to closest found tree
        if not agent.getPath() and woodPrioList:
            agent.setPath(Pathfinder.findPath(agent, (woodPrioList[0][0], woodPrioList[0][1])))
            Resources.treeFound((woodPrioList[0][0], woodPrioList[0][1]))

        elif agent.getPath():
            self.move(agent, agent.getPos())

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

    def getStateName(self):
        return "locateMaterials"

    def move(self, agent, pos):
        diff = (time.time() - agent.getTimer()) * TimeMultiplier.timeMultiplier
        if Map.map[pos[0]][pos[1]] in ("G", "T", "t"):
            traverseTime = StatParser.statDict["tsSlowed"]
        else:
            traverseTime = StatParser.statDict["tsGround"]

        if diff >= traverseTime:
            agent.setTimer(time.time())
            agent.setPos(agent.getPath()[0])
            agent.setPath(agent.popPath())


class woodCutting():
    def execute(self, agent):
        diff = (time.time() - agent.getTimer()) * TimeMultiplier.timeMultiplier
        agent.setLocked(True)
        if diff >= StatParser.statDict["wcSpeed"]:
            agent.setInventory("wood")
            agent.setTimer(time.time())
            agent.setLocked(False)
            agent.setState(returnHome())

    def getStateName(self):
        return "woodCutting"


class returnHome():
    def execute(self, agent):
        pos = agent.getPos()
        if agent.getPath() == [] or agent.getPath()[len(agent.getPath())-1] != agent.base.getPos():
            agent.setPath(Pathfinder.findPath(agent, agent.base.getPos()))
        elif not agent.getLocked():
            diff = (time.time() - Agents.agent.getTimer(agent)) * TimeMultiplier.timeMultiplier
            if Map.map[pos[0]][pos[1]] in ("G", "T", "t"):
                traverseTime = StatParser.statDict["tsSlowed"]
            else:
                traverseTime = StatParser.statDict["tsGround"]

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
                    if agent.getRole() == "worker":
                        agent.setState(locateMaterials())
                    elif agent.getRole() == "builder":
                        agent.setState(idle())
                    elif agent.getJob() in ("coalWorker", "weaponSmith", "smelteryWorker"):
                        agent.setState(findWorkStation())

    def getStateName(self):
        return "returnHome"

class findWorkStation:
    def execute(self, agent):
        if not agent.getPath():
            workDict = {
                "coalWorker": "coalFurnace",
                "weaponSmith": "blacksmith",
                "smelteryWorker": "smeltery"
            }
            for building in agent.base.getBuildings():
                if building.getName() == workDict[agent.getJob()] and not building.getOccupied():
                    agent.setPath(Pathfinder.findPath(agent, building.getPos()))
                    building.setOccupied(True)
                    agent.setJob(building)
                    break
        else:
            pos = agent.getPos()
            diff = (time.time() - Agents.agent.getTimer(agent)) * TimeMultiplier.timeMultiplier
            if Map.map[pos[0]][pos[1]] in ("G", "T", "t"):
                traverseTime = StatParser.statDict["tsSlowed"]
            else:
                traverseTime = StatParser.statDict["tsGround"]

            if diff >= traverseTime:
                agent.setTimer(time.time())
                agent.setPos(agent.getPath()[0])
                agent.setPath(agent.popPath())

                if not agent.getPath():
                    agent.setState(work())

    def getStateName(self):
        return "findWorkStation"


class work:
    def execute(self, agent):
        if agent.base.getBuildList() == []:
            if agent.getRole() == "smelteryWorker" and agent.base.getIron() >= 20:
                return
            agent.getJob().work(agent)

    def getStateName(self):
        return "work"

class build:
    def execute(self, agent):
        readyToBuild = False
        # Where to build
        if agent.base.getBuildList() and not agent.getLocked():
            pos = agent.getPos()
            # find unused buildable tile
            for next in Map.r:
                if Map.map[pos[0] + next[0]][pos[1] + next[1]] in ("M", "G") and FogOfWar.fogOfWar[pos[0] + next[0]][pos[1] + next[1]]:
                    # What to build
                    for building in agent.base.getBuildList():
                        if building[0] == "coalFurnace":
                            if building[1] == 0 or building[1] == agent.getId():
                                readyToBuild = agent.base.buildCoalFurnace(agent, (pos[0] + next[0], pos[1] + next[1]))
                                if readyToBuild == True:
                                    agent.setPos((pos[0] + next[0], pos[1] + next[1]))
                                    building[1] = agent.getId()
                                    agent.setLocked(True)
                                break

                        elif building[0] == "smeltery":
                            if building[1] == 0 or building[1] == agent.getId():
                                readyToBuild = agent.base.buildSmeltery(agent, (pos[0] + next[0], pos[1] + next[1]))
                                if readyToBuild == True:
                                    agent.setPos((pos[0] + next[0], pos[1] + next[1]))
                                    building[1] = agent.getId()
                                    agent.setLocked(True)
                                break

                        elif building[0] == "blacksmith":
                            if building[1] == 0 or building[1] == agent.getId():
                                readyToBuild = agent.base.buildBlacksmith(agent, (pos[0] + next[0], pos[1] + next[1]))
                                if readyToBuild:
                                    agent.setPos((pos[0] + next[0], pos[1] + next[1]))
                                    building[1] = agent.getId()
                                    agent.setLocked(True)
                                break

                        elif building[0] == "trainingCamp":
                            if building[1] == 0 or building[1] == agent.getId():
                                agent.base.buildTrainingcamp(agent, (pos[0] + next[0], pos[1] + next[1]))
                                building[1] = agent.getId()
                                if readyToBuild:
                                    agent.setPos((pos[0] + next[0], pos[1] + next[1]))
                                    agent.setLocked(True)
                                break
                    break
        elif agent.getPos() == agent.getJob()[1]:
            diff = (time.time() - agent.getTimer()) * TimeMultiplier.timeMultiplier

            if agent.getJob()[0] == "coalFurnace*":
                if diff >= StatParser.statDict["cfBuildTime"]:
                    agent.base.addBuilding(BaseManager.coalFurnace(agent.getPos()))
                    agent.setJob("builder")
                    agent.setLocked(False)
                    agent.setState(returnHome())

            elif agent.getJob()[0] == "smeltery*":
                if diff >= StatParser.statDict["smelteryBuildTime"]:
                    agent.base.addBuilding(BaseManager.smeltery(agent.getPos()))
                    agent.setJob("builder")
                    agent.setLocked(False)
                    agent.setState(returnHome())

            elif agent.getJob()[0] == "blacksmith*":
                if diff >= StatParser.statDict["bsBuildTime"]:
                    agent.base.addBuilding(BaseManager.blacksmith(agent.getPos()))
                    agent.setJob("builder")
                    agent.setLocked(False)
                    agent.setState(returnHome())

            elif agent.getJob()[0] == "trainingCamp":
                if diff >= StatParser.statDict["tcBuildTime"]:
                    agent.base.addBuilding(BaseManager.trainingCamp(agent.getPos()))
                    agent.setJob("builder")
                    agent.setLocked(False)
                    agent.setState(returnHome())


            # When to hire
            elif agent.getJob()[0] == "coalFurnace":
                if StatParser.statDict["cfBuildTime"] - (time.time() - agent.getTimer()) <= StatParser.statDict["artisanUpgradeTime"]:
                    Agents.addToJobList("coalWorker")
                    agent.setJob(("coalFurnace*", agent.getJob()[1]))
            elif agent.getJob()[0] == "smeltery":
                if StatParser.statDict["smelteryBuildTime"] - (time.time() - agent.getTimer()) <= StatParser.statDict["artisanUpgradeTime"]:
                    Agents.addToJobList("smelteryWorker")
                    agent.setJob(("smeltery*", agent.getJob()[1]))
            elif agent.getJob()[0] == "blacksmith":
                if StatParser.statDict["bsBuildTime"] - (time.time() - agent.getTimer()) <= StatParser.statDict["artisanUpgradeTime"]:
                    Agents.addToJobList("weaponSmith")
                    agent.setJob(("blacksmith*", agent.getJob()[1]))

        elif agent.base.getBuildList() == []:
        # When finished go idle until build list has content
            agent.setState(returnHome())

    def getStateName(self):
        return "build"


class idle:
    def execute(self, agent):
        if agent.getRole() == "builder" and agent.base.getBuildList() != []:
            agent.setState(build())
        elif agent.getRole() == "builder":
            agent.setJob("idle")

    def getStateName(self):
        return "idle"


class upgrading:
    def execute(self, agent):
        if not agent.getLocked():
            agent.setTimer(time.time())
            agent.setLocked(True)

        diff = (time.time() - agent.getTimer()) * TimeMultiplier.timeMultiplier

        if agent.getJob() == "explorer":
            if diff >= StatParser.statDict["explorerUpgradeTime"]:
                agent.setRole("explorer")
                agent.setState(explore())
                agent.setLocked(False)

        elif agent.getJob() in ("coalWorker", "weaponSmith", "smelteryWorker", "builder"):
            if diff >= StatParser.statDict["artisanUpgradeTime"]:
                if agent.getJob() == "builder":
                    agent.setRole("builder")
                elif agent.getJob() == "coalWorker":
                    agent.setRole("coalWorker")
                elif agent.getJob() == "weaponSmith":
                    agent.setRole("weaponSmith")
                elif agent.getJob() == "smelteryWorker":
                    agent.setRole("smelteryWorker")

                agent.setState(returnHome())
                agent.setLocked(False)

        elif agent.getJob() == "soldier":
            if diff >= StatParser.statDict["soldierUpgradeTime"]:
                agent.setRole("soldier")
                agent.setState(idle())
                agent.setLocked(False)

        elif agent.getJob() in ("woodCutter", "miner"):
            agent.setState(locateMaterials())
            agent.setLocked(False)

    def getStateName(self):
        return "upgrading"