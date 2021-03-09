import State

#Keeps all variables for each agent and looks over all updates of said agents.
#This class also lets the agents send and recieve messages about hanging out.
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
        if(self.happiness <= 20 && self.state != socializing()):
            #send message
        self.state.execute(self)

    def sendMsg(self, personList):
        if(self.hasPlans == False):#Has no plans / needs to make plans
            print("Agent " + str(self.nameId) + ": Hey everyone! Anyone want to hang out at the park in an hour?")
            for person in personList:
                if(person.nameId != self.nameId):#If not me
                    if(person.recvMsg(personList) == True):#If recipient of message said yes
                        self.hasPlans = True
                        self.sentMsg = True
                    
        else:#Has plans
            print("Agent " + str(self.nameId) + ": I'm going to the park you all still comming?")
            for person in personList:
                if(person.hasPlans == True and person.nameId != self.nameId):#Recipient still saying yes and is not me
                    if(person.recvMsg(personList) == True and self.state.getStateName() != "socializing"):
                        self.state = State.socializing()
                if(self.state.getStateName() != "socializing"):#Everyone said no
                    self.hasPlans = False
            self.sentMsg = False
                    

    def recvMsg(self, personList):
        if(self.hasPlans == False):
            if (self.state.getStateName() == "sleeping"):
                print("No respons. Agent " + str(self.nameId) + " is currently sleeping.")
                return False
            else:
                print("Agent " + str(self.nameId) + ": Yes, that sounds fun!")
                self.hasPlans = True
                return True

        else:
            if(self.state.getStateName() == "sleeping"):
                print("Agent " + str(self.nameId) + " did not respond and is currently sleeping.")
                self.hasPlans = False
                return False
            if(self.state.getStateName() == "socializing"):
                print("Agent " + str(self.nameId) + ": we are already hanging out, come join us!.")
                self.state = State.socializing()
                return True
            elif(self.eat <= 20 or self.drink <= 20):
                print("Agent " + str(self.nameId) + ": Sorry something came up. Maybe next time.")
                self.hasPlans = False
                return False
            else:
                print("Agent " + str(self.nameId) + ": Yes, I'm on my way as well.")
                self.state = State.socializing()
                return True

    #Calls for appropriate state execute func to update agents stats
    def Update(self, personList):
        if(self.state.getStateName() != "socializing"):
            self.state.execute(self)
        else:
            self.state.execute(self,personList)

>>>>>>> origin/master
