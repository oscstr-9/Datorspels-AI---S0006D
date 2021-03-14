import Agents
import TimeMultiplier
import StateManager
import Map
import StatParser
import time

class base():
    def __init__(self, pos):
        self.pos = pos
        self.buildList = []
        self.buildings = []
        self.wood = 0
        self.minerals = 0
        self.coal = 0
        self.iron = 0
        self.sword = 0

    def getPos(self):
        pos = (self.pos[0], self.pos[1])
        return pos

    def getBuildList(self):
        return self.buildList
    def addToBuildList(self, building):
        self.buildList.append(building)
    def popBuildList(self):
        self.buildList.pop(0)

    def getBuildings(self):
        return self.buildings
    def addBuilding(self, building):
        self.buildings.append(building)

    def addWood(self):
        self.wood += 1
    def getWood(self):
        return self.wood

    def addMinerals(self):
        self.minerals += 1
    def getMinerals(self):
        return self.minerals

    def createCoal(self):
        self.coal += StatParser.statDict["coalReturn"]
    def getCoal(self):
        return self.coal
    def removeCoalCost(self):
        self.wood -= StatParser.statDict["coalWoodCost"]

    def removeIronCost(self):
        self.minerals -= StatParser.statDict["ironOreCost"]
        self.coal -= StatParser.statDict["ironCoalCost"]
    def createIron(self):
        self.iron += StatParser.statDict["ironReturn"]
    def getIron(self):
        return self.iron

    def removeSwordCost(self):
        self.iron -= StatParser.statDict["swordIronCost"]
        self.coal -= StatParser.statDict["swordCoalCost"]
    def createSword(self):
        self.sword += StatParser.statDict["swordReturn"]


    def buildCoalFurnace(self, agent, pos):
        if self.wood < StatParser.statDict["buildingWoodCost"]:
            return False

        elif agent.getJob()[0] != "coalFurnace" or agent.getJob()[0] != "coalFurnace*":
            self.wood -= StatParser.statDict["buildingWoodCost"]
            agent.base.popBuildList()
            agent.setTimer(time.time())
            agent.setJob(("coalFurnace", pos))
            Map.changeMap("construction", pos)
            return True

    def buildSmeltery(self, agent, pos):
        if self.wood < StatParser.statDict["buildingWoodCost"]:
            return False

        elif agent.getJob()[0] != "smeltery" or agent.getJob()[0] != "smeltery*":
            self.wood -= StatParser.statDict["buildingWoodCost"]
            agent.base.popBuildList()
            agent.setTimer(time.time())
            agent.setJob(("smeltery", pos))
            Map.changeMap("construction", pos)
            return True

    def buildBlacksmith(self, agent, pos):
        if self.wood < StatParser.statDict["buildingWoodCost"] or StatParser.statDict["bsIronCost"]:
            return False

        if agent.getJob()[0] != "blacksmith" or agent.getJob()[0] != "blacksmith*":
            self.wood -= StatParser.statDict["buildingWoodCost"]
            self.iron -= StatParser.statDict["bsIronCost"]
            agent.base.popBuildList()
            agent.setTimer(time.time())
            agent.setJob(("blacksmith", pos))
            Map.changeMap("construction", pos)
            return True

    def buildTrainingCamp(self, agent, pos):
        if self.wood < StatParser.statDict["buildingWoodCost"]:
            return

        self.wood -= StatParser.statDict["buildingWoodCost"]
        agent.base.popBuildList()

        if agent.getJob()[0] != "trainingCamp":
            agent.setTimer(time.time())
            agent.setJob(("trainingCamp", pos))
            Map.changeMap("construction", pos)
            return True


class coalFurnace:
    def __init__(self, pos):
        self.name = "coalFurnace"
        self.pos = pos
        Map.changeMap("CF", pos)
        self.timer = time.time()
        self.working = False
        self.occupied = False

    def getName(self):
        return self.name

    def getPos(self):
        return self.pos

    def getOccupied(self):
        return self.occupied
    def setOccupied(self, occupied):
        self.occupied = occupied

    def work(self, agent):
        if not self.working and agent.base.getWood() >= StatParser.statDict["coalWoodCost"]:
            agent.base.removeCoalCost()
            self.timer = time.time()
            self.working = True
        elif self.working:
            diff = (time.time() - self.timer) * TimeMultiplier.timeMultiplier
            if diff >= StatParser.statDict["coalTimeCost"]:
                agent.base.createCoal()
                self.working = False



class smeltery:
    def __init__(self, pos):
        self.name = "smeltery"
        self.pos = pos
        Map.changeMap("SM", pos)
        self.timer = time.time()
        self.working = False
        self.occupied = False

    def getName(self):
        return self.name

    def getPos(self):
        return self.pos

    def getOccupied(self):
        return self.occupied
    def setOccupied(self, occupied):
        self.occupied = occupied

    def work(self, agent):
        if agent.base.getCoal() >= StatParser.statDict["ironCoalCost"] and agent.base.getMinerals() >= StatParser.statDict["ironOreCost"]:
            agent.base.removeIronCost()
            agent.base.createIron()

class blacksmith:
    def __init__(self, pos):
        self.name = "blacksmith"
        self.pos = pos
        Map.changeMap("BS", pos)
        self.timer = time.time()
        self.working = False
        self.occupied = False

    def getName(self):
        return self.name

    def getPos(self):
        return self.pos

    def getOccupied(self):
        return self.occupied
    def setOccupied(self, occupied):
        self.occupied = occupied

    def work(self, agent):
        if not self.working and agent.base.getCoal() >= StatParser.statDict["swordCoalCost"] and agent.base.getIron() >= StatParser.statDict["swordIronCost"]:
            agent.base.removeSwordCost()
            self.timer = time.time()
            self.working = True
        elif self.working:
            diff = (time.time() - self.timer) * TimeMultiplier.timeMultiplier
            if diff >= StatParser.statDict["swordTimeCost"]:
                agent.base.createSword()
                self.working = False

class trainingCamp:
    def __init__(self, pos):
        self.name = "trainingCamp"
        self.pos = pos
        Map.changeMap("TC", pos)
        self.timer = time.time()
        self.working = False
        self.occupied = False

    def getName(self):
        return self.name

    def getPos(self):
        return self.pos

    def getTimer(self):
        return self.timer

    def setTimer(self, timer):
        self.timer = timer

    def getWorking(self):
        return working

    def setWorking(self, working):
        self.working = working

    def getOccupied(self):
        return self.occupied

    def setOccupied(self, occupied):
        self.occupied = occupied

    def work(self):
        return
