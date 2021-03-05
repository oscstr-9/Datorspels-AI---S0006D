import Agents
import TimeMultiplier
import StateManager
import Map
import time

class base():
    def __init__(self, pos):
        self.wood = 0
        self.minerals = 0
        self.coal = 0
        self.iron = 0
        self.sword = 0
        self.pos = pos
        self.buildings = []

    def addWood(self):
        self.wood += 1

    def addMinerals(self):
        self.minerals += 1

    def addBuilding(self, building):
        self.buildings.append(building)

    def createCoal(self):
        self.wood -= 2
        self.coal += 1

    def createIron(self):
        self.minerals -= 2
        self.coal -= 3
        self.iron += 1

    def createSword(self):
        self.iron -= 1
        self.coal -= 2
        self.sword += 1

    def buildCoalFurnace(self, agent):
        self.wood -= 10

        if agent.getInventoy() != "coalFurnace":
            agent.setTimer(time.time)
            agent.setInventoy("coalFurnace")
            agent.setLocked(True)
        else:
            diff = time.Time() - time * TimeMultiplier.timeMultiplier
            if diff >= 60:
                self.addBuilding(append(coalFurnace(agent.getPos())))
                agent.setInventoy("empty")
                agent.setLocked(False)
                agent.setState(StateManager.idle())

    def buildSmeletery(self, agent):
        self.wood -= 10
        self.iron -= 3

        if agent.getInventoy() != "smeletery":
            agent.setTimer(time.time)
            agent.setInventoy("smeletery")
            agent.setLocked(True)
        else:
            diff = time.Time() - time * TimeMultiplier.timeMultiplier
            if diff >= 120:
                self.addBuilding(append(smeletery(agent.getPos())))
                agent.setInventoy("empty")
                agent.setLocked(False)
                agent.setState(StateManager.idle())

    def buildBlacksmith(self, agent):
        self.wood -= 10

        if agent.getInventoy() != "blacksmith":
            agent.setTimer(time.time)
            agent.setInventoy("blacksmith")
            agent.setLocked(True)
        else:
            diff = time.Time() - time * TimeMultiplier.timeMultiplier
            if diff >= 180:
                self.addBuilding(append(blacksmith(agent.getPos())))
                agent.setInventoy("empty")
                agent.setLocked(False)
                agent.setState(StateManager.idle())

    def buildTrainingCamp(self, agent):
        self.wood -= 10

        if agent.getInventoy() != "trainingCamp":
            agent.setTimer(time.time)
            agent.setInventoy("trainingCamp")
            agent.setLocked(True)
        else:
            diff = time.Time() - time * TimeMultiplier.timeMultiplier
            if diff >= 120:
                self.addBuilding(append(trainingCamp(agent.getPos())))
                agent.setInventoy("empty")
                agent.setLocked(False)
                agent.setState(StateManager.idle())

class coalFurnace:
    def __init__(self, pos):
        self.pos = pos
        Map.changeMap("CF", pos)
        self.timer = time.time()
        self.working = False

    def work(self):
        return

class smeltery:
    def __init__(self, pos):
        self.pos = pos
        Map.changeMap("SM", pos)
        self.timer = time.time()
        self.working = False

    def work(self):
        return

class blacksmith:
    def __init__(self, pos):
        self.pos = pos
        Map.changeMap("BS", pos)
        self.timer = time.time()
        self.working = False

    def work(self):
        return

class trainingCamp:
    def __init__(self, pos):
        self.pos = pos
        Map.changeMap("TC", pos)
        self.timer = time.time()
        self.working = False

    def work(self):
        return
