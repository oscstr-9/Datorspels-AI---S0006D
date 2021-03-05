import StateManager
import time

class agent:
    def __init__(self, pos, state):
        self.x = pos[0]
        self.y = pos[1]
        self.role = "worker"
        self.state = StateManager.idle()
        self.timer = time.time()
        self.path = []
        self.locked = False
        self.inventory = "empty"

    def getPos(self):
        return [self.x, self.y]
    def setPos(self, pos):
        if not self.locked:
            self.x = pos[0]
            self.y = pos[1]

    def getState(self):
        return self.state
    def setState(self, state):
        if not self.locked:
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

    def getInventory(self):
        return self.inventory
    def setInventory(self, inventory):
        self.inventory = inventory
