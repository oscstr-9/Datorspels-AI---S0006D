import time
import Person
import State
from random import randrange

def main():
    nameId = 1
    eat = randrange(20, 80)
    drink = randrange(20, 80)
    sleep = randrange(20, 80)
    work = randrange(20, 80)
    shop = randrange(20, 80)
    happiness = randrange(20, 80)
        
    x = int(input("Please enter how many people exist: "))

    personList = []
    for i in range(x):
        workplace = divmod(i, 2)
        print(workplace)
        personList.append(Person.Person(i, workplace[1], eat, drink, sleep, work, shop, happiness))
        personList[i].nameId = i

    timerFunc(personList)



def timerFunc(personList):
    t0 = time.time()
    timeMultiplier = 3600
    then = 0
    now = 0
    while True:
        timer = (time.time() - t0) * timeMultiplier
        hour = divmod(timer, 3600.0)
        day = divmod(hour[0], 24)
        year = divmod(day[0], 365)

        now = hour[0]

        if(then < now):
            diff = now - then
            then = now
            updateAgents(personList, int(diff))
            


def updateAgents(personList, diff):
    for i in range(diff):
        for person in personList:
            person.Update()



main()

