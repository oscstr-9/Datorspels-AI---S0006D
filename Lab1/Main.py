import time
import Person
import State
from random import randrange

def main():        
    x = int(input("Please enter how many people exist: "))
    timeMultiplier = int(input("Please enter how many seconds per second should pass (updates happen every hour):"))

    personList = []
    for i in range(x):
        workplace = divmod(i, 2)

        #Randomizes all stats for each agent 
        eat = randrange(40, 80)
        drink = randrange(40, 80)
        sleep = randrange(40, 80)
        work = randrange(40, 80)
        shop = randrange(40, 80)
        happiness = randrange(40, 80)
    
        personList.append(Person.Person(i+1, workplace[1], eat, drink, sleep, work, shop, happiness))

    timerFunc(personList, timeMultiplier)


#Keeps track of time and when to update the agents. Takes a list of all agents as a parameter
def timerFunc(personList, timeMultiplier):
    t0 = time.time()
    #To speed up the passing of time
    then = 0
    now = 0
    
    updateAgents(personList, 1)
    while True:
        timer = (time.time() - t0) * timeMultiplier
        #Calculates date depending on seconds passed
        hour = divmod(timer, 3600.0)
        day = divmod(hour[0], 24)
        year = divmod(day[0], 365)

        now = hour[0]

        if(then < now):
            diff = now - then
            then = now
            updateAgents(personList, int(diff))
            

#Determines how many times an agent should be updated depending on times that has passed
#as well as if an agent should send message to meet up.
#Takes a list of all agents and the hours that has passed as parameters
def updateAgents(personList, diff):
    for i in range(diff):
        for person in personList:
            
            

            if(person.happiness <= 30 and person.hasPlans == person.sentMsg and person.state.getStateName != "sleeping"):
                person.sendMsg(personList)

            print("\n") 
            person.Update(personList)
            print("Agent " + str(person.nameId) + "'s stats:")
            print("Eat: " + str(person.eat))
            print("Drink: " + str(person.drink))
            print("Sleep: " + str(person.sleep))
            print("Work: " + str(person.work))
            print("Shop: " + str(person.shop))
            print("Happiness: " + str(person.happiness))
            print("\n")


main()

