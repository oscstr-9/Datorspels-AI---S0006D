import StateManager
import time
jobList = []

# The agent class has all information about the agents.
# It also has getters and setters for almost all variables
class agent:
    def __init__(self, pos, base, id):
        self.x = pos[0]
        self.y = pos[1]
        self.id = id
        self.role = "worker"
        self.state = StateManager.idle()
        self.timer = time.time()
        self.path = []
        self.locked = False
        self.inventory = "empty"
        self.base = base
        self.job = "idle"

    def getPos(self):
        return (self.x, self.y)
    def setPos(self, pos):
        if not self.locked:
            self.x = pos[0]
            self.y = pos[1]

    def getId(self):
        return self.id

    def getState(self):
        return self.state.getStateName()
    def setState(self, state):
        self.state = state

    def getRole(self):
        return self.role
    def setRole(self, role):
        self.role = role

    def getTimer(self):
        return self.timer
    def setTimer(self, timer):
        self.timer = timer

    def getPath(self):
        return self.path
    def setPath(self, path):
        self.path = path
    def popPath(self):
        self.path.pop(0)
        return self.path

    def setLocked(self, locked):
        self.locked = locked
    def getLocked(self):
        return self.locked

    def getInventory(self):
        return self.inventory
    def setInventory(self, inventory):
        self.inventory = inventory

    def getJob(self):
        return self.job
    def setJob(self, job):
        self.job = job

# Adds and removes jobs from the job list that all agents share
def addToJobList(job):
    global jobList
    jobList.append(job)
def removeFromJobList():
    global jobList
    jobList.pop(0)
