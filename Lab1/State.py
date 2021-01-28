import Person

class working:
    def execute(self, person):
        person.eat -= 1
        person.drink -= 1
        person.sleep -= 1
        person.work += 6
        person.shop -= 1
        person.happiness -= 1

        if(person.work > 50):
            person.state = eating()

        print("Working")

class eating:
    def execute(self, person):
        person.eat += 6
        person.drink -= 1
        person.sleep -= 1
        person.work -= 1
        person.shop -= 1
        person.happiness -= 1

        if(person.eat > 50):
            person.state = drinking()

        print("Eating")
    
class drinking:
    def execute(self, person):
        person.eat -= 1
        person.drink += 6
        person.sleep -= 1
        person.work -= 1
        person.shop -= 1
        person.happiness -= 1

        if(person.drink > 50):
            person.state = sleeping()

        print("Drinking")

class sleeping:
    def execute(self, person):
        person.eat -= 1
        person.drink -= 1
        person.sleep += 6
        person.work -= 1
        person.shop -= 1
        person.happiness -= 1
        
        if(person.sleep > 50):
            person.state = shopping()
            
        print("Sleeping")

class shopping:
    def execute(self, person):
        person.eat -= 1
        person.drink -= 1
        person.sleep -= 1
        person.work -= 1
        person.shop += 6
        person.happiness -= 1

        if(person.shop > 50):
            person.state = socializing()
            
        print("Shopping")

class socializing:
    def execute(self, person):
        person.eat -= 1
        person.drink -= 1
        person.sleep -= 1
        person.work -= 1
        person.shop -= 1
        person.happiness += 6

        if(person.happiness > 50):
            person.state = working()

        print("Socializing")
