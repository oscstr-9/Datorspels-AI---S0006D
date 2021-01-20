import time

class Person:

    def __init__(self, nameId, hunger, food, thirst, water, energy, money, happiness, state):
        self.nameId = nameId
        self.hunger =  hunger
        self.food = food
        self.thirst = thirst
        self.water = water
        self.energy = energy
        self.money = money
        self.happiness = happiness
        self.state = state

nameId = 1
maxHunger = 10
maxFood = 10
maxThirst = 10
maxWater = 10
maxEnergy = 10
startMoney = 0
maxHappy = 10

defaultPerson = Person(nameId, maxHunger, maxFood, maxThirst, maxWater, maxEnergy, startMoney, maxHappy, 0)

class State:
    def Working(person):
        person.hunger -= 5
        person.thirst -= 5
        person.energy -=5
        person.money +=5
        person.happiness -=5
        person.state = 1

    def Shopping(person):
        person.hunger -= 5
        person.food += 5
        person.thirst -= 5
        person.water += 5
        person.energy -= 5
        person.money -= 5
        person.happiness =5
        person.state = 2
        
    def Sleeping(person):
        person.hunger -= 5
        person.thirst -= 5
        person.energy += 5
        person.happiness += 5
        person.state = 3
        
    def Eating(person):
        person.hunger += 5
        person.food -= 5
        person.energy += 5
        person.happiness += 5
        person.state = 4
        
    def Drinking(person):
        person.thirst += 5
        person.water -= 5
        person.energy += 5
        person.happiness += 5
        person.state = 5

    def Socializing(person):
        person.hunger -= 5
        person.thirst -= 5
        person.energy -=5
        person.happiness += 5
        person.state = 6


bob = defaultPerson

def live(person):
    if
print(bob.money)
bob.money += 10
print(bob.money)
bob.money += 10
print(bob.money)

print(divmod(8.0,3))

