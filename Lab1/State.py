import Person

#These classes all can be used to change the stats of an agent and to get the state name
class eating:
    def execute(self, person):
        person.eat += 5
        person.drink -= 1
        person.sleep -= 1
        person.work -= 1
        person.shop -= 1
        person.happiness -= 1

        if(person.eat > 50):
            person.state = drinking()

        print("Agent " + str(person.nameId) + " is Eating.")

    def getStateName(self):
        return "eating"
    
class drinking:
    def execute(self, person):
        person.eat -= 1
        person.drink += 5
        person.sleep -= 1
        person.work -= 1
        person.shop -= 1
        person.happiness -= 1

        if(person.drink > 50):
            person.state = sleeping()

        print("Agent " + str(person.nameId) + " is Drinking.")

    def getStateName(self):
        return "drinking"

class sleeping:
    def execute(self, person):
        person.eat -= 1
        person.drink -= 1
        person.sleep += 5
        person.work -= 1
        person.shop -= 1
        person.happiness -= 1
        
        if(person.sleep > 50):
            person.state = working()
            
        print("Agent " + str(person.nameId) + " is Sleeping.")

    def getStateName(self):
        return "sleeping"
        
class working:
    def execute(self, person):
        person.eat -= 1
        person.drink -= 1
        person.sleep -= 1
        person.work += 5
        person.shop -= 1
        person.happiness -= 1

        if(person.work > 50):
            person.state = shopping()
            
        if(person.workplace == 0):
            print("Agent " + str(person.nameId) +" is Working at LTU.")
        else:
            print("Agent " + str(person.nameId) +" is Working at Krysset.")


    def getStateName(self):
        return "working"

class shopping:
    def execute(self, person):
        person.eat -= 1
        person.drink -= 1
        person.sleep -= 1
        person.work -= 1
        person.shop += 5
        person.happiness -= 1

        if(person.shop > 50):
            person.state = eating()
            
        print("Agent " + str(person.nameId) + " is Shopping.")

    def getStateName(self):
        return "shopping"

class socializing:
    def execute(self, person, personList):
        person.eat -= 1
        person.drink -= 1
        person.sleep -= 1
        person.work -= 1
        person.shop -= 1
        person.happiness += 5

        friends = -1
        alone = False
        
        #Checks if agent is currently alone and unable to socialize
        for x in personList:
            if(x.hasPlans == True):
                friends += 1
        if(friends == 0):
                alone = True
                
        if(person.happiness >= 50 or alone == True):
            person.hasPlans = False
            print("Agent " + str(person.nameId) + ": That was fun. See you later!")
            person.state = eating()

        print("Agent " + str(person.nameId) + " is Socializing.")

    def getStateName(self):
        return "socializing"
