import time
import _thread

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

class State:
    def Working(person):
        person.hunger -= 5
        person.thirst -= 5
        person.energy -= 5
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


        
x = int(input("Please enter how many people exist: "))

personList = []
for i in range(x):
    personList.append(Person(i, maxHunger, maxFood, maxThirst, maxWater, maxEnergy, startMoney, maxHappy, 0))
    personList[i].nameId = i

for i in range(x):
    print(personList[i].nameId)

print(personList[0].money)
personList[0].money += 10
print(personList[0].money)
personList[0].money += 10
print(personList[0].money)

t0 = time.time()
timeMultiplier = 60

def timer():
    while True:
        date = (time.time() - t0) * timeMultiplier
        hour = divmod(date, 3600.0)
        day = divmod(hour[0], 24)
        year = divmod(day[0], 365)
        print(hour)
    
_thread.start_new_thread(timer())

while True:
    timeMultiplier = input()

    
    

