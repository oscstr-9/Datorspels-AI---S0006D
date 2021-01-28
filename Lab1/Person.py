import State

class Person:
    def __init__(self, nameId, workplace, eat, drink, sleep, work, shop, happiness):
        self.nameId = nameId
        self.workplace = workplace
        
        self.eat =  eat
        self.drink = drink
        self.sleep = sleep
        self.work = work
        self.shop = shop
        self.happiness = happiness
        
        self.state = State.sleeping()
        self.plans = 0
        
    def Update(self):
        self.state.execute(self)
