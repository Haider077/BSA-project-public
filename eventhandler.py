from events import *
import json
from ursina import *
from settings import *
import world as w
import random as rand
import textwrap


#class event 
# id is tbd 
# name is name of the event 
# description will be used to output UI describing the event that has occured 
# event, a 3d list, will hold specifications for what an exactly how much some param will be affected 
# date will mark when the effect will occur 
class eventhandler():
    def __init__(self,world_interface):
        self.events = []
        self.wi = world_interface
        self.banned_cities = []
        self.disabled_stores = []
        self.wordwrap = 55
        self.createUIEvent()

        self.click = Audio("resources/confirmation_001.ogg", pitch=1, loop=False, autoplay=False)

    #helper methods 

    #will create events
    def create_events(self): 
        # TODO: fetch API here
        with open('./json/event.json', 'r') as f:
            data = json.load(f)
            
            for i in range(len(data)):
                id = data[i]
                name = data[i]["name"]
                description = data[i]["description"]
                self.events.append(Event(id, name, description))

    # adds event interface popup window
    def show_event_window(self):
        self.event_window.enabled = True

    def close_event_window(self):
        self.click.play(0)
        self.event_window.enabled = False

    def feed_event(self, name, id, description):
        description = textwrap.TextWrapper(width = self.wordwrap).fill(text = description)
        self.event_window.text_entity.text = (f"Event {id}: {name}")
        self.description_entity.text = description
        self.event_window.enabled = True
    
    def createUIEvent(self):
        self.description_entity = Text("\n\n")
        self.description_entity.scale = 0.8

        self.event_window = WindowPanel(
            scale = CONFIRM_WIN_SIZE,
            color = WINDOW_COLOR,
            position = CONFIRM_WIN_POS,
            content = [
                self.description_entity,
                Button(
                    "Accept",
                    color = color.azure,
                    on_click = self.close_event_window,
                    scale = 0.8)],
            enabled = False)

        self.event_window.content[1].scale *= 0.8
        self.wi.full_screen_window.append(self.event_window)

    # Uses Switch statement to determine which events will be active or not 
    # install python 3.10+ to use match case statements 
    def activate_event(self, id): 
        match id: 
            case 1:
                effectedCity = w.global_cities[rand.randint(0,len(w.global_cities)- 1)]
                self.feed_event("Local Market Boom","3687", effectedCity.name + " is experiencing a local market boom and will gain " + f'{round(effectedCity.wealth * 0.1): ,}' + " units of wealth.") 
                self.wi.log.log(effectedCity.name + " gained " + str(round(effectedCity.wealth * 0.1)) + " units of wealth this qaurter.")
                effectedCity.wealth += round(effectedCity.wealth * 0.1)
                #War case methods tbd
                #Description: Will effect population, productivity, and wealth significantly. May endow other effects depending on feedback
                pass
            case 2:
                effectedCity = w.global_cities[rand.randint(0,len(w.global_cities)- 1)]
                self.feed_event("Baby Boom","1895", effectedCity.name + " is experiencing a huge baby boom and will gain " + f'{round(effectedCity.population * 0.05): ,}' + " population.") 
                self.wi.log.log(effectedCity.name + " gained " + f'{round(effectedCity.population * 0.05): ,}' + " population this qaurter.")
                effectedCity.population += int(effectedCity.population * 0.1)

                #Alliance method tbd
                #Description: Will effect productivity and wealth
                pass
            case 3:
                if(rand.randint(0,100) > 95):
                    for i in w.global_cities :
                        if(i.name == "Beijing"):
                            effectedCity = i
                            self.feed_event("Xi Jin Ping Spa","8457","Xi jin ping is shutting down " + effectedCity.name + " and it will be removed to build a personal spa resort for himself (only Xi jin ping and his entourage remain in former bejing).")
                            effectedCity.name = "Xi Jin Ping Spa"
                            effectedCity.wealth = 0
                            effectedCity.population -= round(effectedCity.population/2)
                            effectedCity.description = "A happy spa for the glorius chairman of CCP."
                            self.wi.log.log("Nothing different happened this qaurter, Beijing was always a spa for Xi Jin Ping. Any claim it was a real city is propaganda.")
                
                pass
            case 4:
                if(rand.randint(0,100) > 95): 
                    effectedCity = w.global_cities[rand.randint(0,len(w.global_cities)- 1)]
                    #Inflation methods tbd
                    self.feed_event("Hobo invasion","5436","hobos have plagued " + effectedCity.name + " and it will lose " + str(round(effectedCity.wealth / 2)) + " units of wealth but gain " + f'{round(effectedCity.population / 5): ,}' + " population.")
                    effectedCity.wealth = round(effectedCity.wealth / 2)
                    effectedCity.population += round(effectedCity.population / 5)
                    self.wi.log.log("A hobo invasion happend to " + effectedCity.name + ".")
                    #Description: Will effect productivity, wealth and income 
                pass
            case 5:
                if(rand.randint(0,100) > 90):
                    self.feed_event("Global Market Crash","G125", " The global market has crashed, hide your cash (wealth in all cities greatly reduced).") 
                    for i in w.global_cities :
                        i.wealth *= 0.8
                    self.wi.log.log("A global market crash happened this qaurter.")
                    #Depression case methods tbd
                    #Description: Will effect productivity, wealth, income and pop 
                pass
            case 6:
                if(rand.randint(0,100) > 10): 
                    self.feed_event("Robbed","0985", " A pack of idiots break into your office, beat you up, and take the money from your safe.") 
                    self.wi.log.log("You got beat up and lost $" + f'{round(self.wi.player.getCash()* 0.05): ,}' + " cash.")
                    self.wi.player.removeCash(round(self.wi.player.getCash()* 0.05))
                    #cyberattack method tbd
                    #Description: Will effect ability for stores to trade
                pass
            case 7:
                investors = ["Jimmy Neutron","Jim Carrey","Xi Jin Ping","Kiryu Kazuma","The bald guy from shark tank","Adof Hilter","Elon Musk","Jack Ma","Some guy named Smith","Bill Gates","The Pope"]

                if(rand.randint(0,100) > 10): 
                    self.feed_event("Investment","9985", investors[rand.randint(0,10)] + " has decided to buy shares and invest in your corporation. You will receive " + str(round(self.wi.player.getCash()* 0.05)) + " cash from the investor.") 
                    self.wi.log.log("An investor gave you $" + f'{round(self.wi.player.getCash()* 0.05): ,}' + " cash this qaurter.")
                    self.wi.player.addCash(round(self.wi.player.getCash()* 0.05))

                #ransomware methods tbd
                #Description: Will effect cash and store selling status directly to unlock the stores
                pass
            case 8:
                if(rand.randint(0,100) > 10 and len(self.wi.player.getMarkets()) > 0):
                    product = self.wi.player.getMarkets()[rand.randint(0,len(self.wi.player.getMarkets())- 1)].products[rand.randint(0,3)]
                    if(rand.randint(0,100) > 20): 
                        self.feed_event("Efficent Factories","0056", "A new technology has made it possible to produce " + product.name + " for less cost." ) 
                        self.wi.log.log("A new technology lowered the cost of " + product.name + " by $" + f'{round(product.cost * 0.1): ,}' + " cash.")

                        product.cost -= round(product.cost * 0.1)

                pass
            case 9: 
                 if(rand.randint(0,100) > 10):
                     effectedCity = w.global_cities[rand.randint(0,len(w.global_cities)- 1)]
                     self.feed_event("Government investment","0756", effectedCity.name + " is receiving government investment to improve infrastructure, there is a 50 percent chance this this will have no effect. If successful the cities wealth will increase by 5%") 
                     if(rand.randint(0,100) > 50):
                        self.wi.log.log("The government investment succeeded in adding " + str(round(effectedCity.wealth * 0.05)) + " wealth to " + effectedCity.name + ".")
                       
                        effectedCity.wealth += round(effectedCity.wealth * 0.05)
                     else:
                        self.wi.log.log("The government ended up building a giant ferris wheel with your tax money, and you don't get anything.")
                    #Alliance method tbd
                    #Description: Will effect productivity and wealth

            case 10: 
                if(rand.randint(0,100) > 10 and len(self.wi.player.getMarkets()) > 0):
                        product = self.wi.player.getMarkets()[rand.randint(0,len(self.wi.player.getMarkets())- 1)].products[rand.randint(0,3)]
                        if(rand.randint(0,100) > 20): 
                            self.feed_event("Hot Product","0057", product.name + " is a hot commodity this qaurter, the value of the product has been slightly increased." ) 
                            self.wi.log.log("Consumer demand increased the value of " + product.name + " by " + f'{round(product.value * 0.05): ,}' + " cash.")
                            product.cost += round(product.value * 0.05)

                pass
            case 11: 
                if(rand.randint(0,100) > 10 and len(self.wi.player.getMarkets()) > 0):
                    product = self.wi.player.getMarkets()[rand.randint(0,len(self.wi.player.getMarkets())- 1)].products[rand.randint(0,3)]
                    if(rand.randint(0,100) > 20): 
                        self.feed_event("Weird Van Found","0052", "You found a weird van containing an absurd amount of " + product.name + ". You take it and stock your store with its contents." ) 
                        self.wi.log.log("Wait... Your stock is up, but isn't theft by finding kind of illegal?")
                    
                        product.quantity += product.quantity * 0.5
                pass
            case 12: 
                #stockmarketcrash methods tbd 
                #Description: Will effect wealth and income
                pass
            case 13: 
                #economic boom methods tbd 
                #Description: Will effect productivity and wealth
                pass
            case 14:
                #Surging demand methods tbd
                #Description: Will effect 
                pass
            case 15:
                #celebrity promotions methods tbd
                #Description: Will effect productivity and income 
                pass
            case 16:
                #Baby boom methods tbd
                #Description: Will effect pop significantly 
                pass
            case 17:
                #investment methods tbd
                #Description: Will effect wealth and productivity 
                pass
                
        self.wi.log.log("------")
                
    # Disables trade with certain cities for events such as war or protests  
    def disable_cities(self, name, id, effect, cities):
        self.banned_cities = cities

        for i in len(self.banned_cities): 
            i.toggle_tradability = False

    def enable_cities(self, name, id, effect, cities): 
        for i in len(self.banned_cities): 
            i.toggle_tradability = True 
        self.banned_cities = []

    # Disables stores within certain cities due to events like strikes
    def disable_stores(self, name, id, effect, stores): 
        self.disabled_stores = stores 

        for i in len(self.disabled_stores): 
            i.owner = "Disabled" 

    # enables stores to be operable again
    def enable_stores(self, player_name, name, id, effect, stores): 
        for i in len(self.disabled_stores): 
            i.owner = player_name
        self.disabled_stores = []

    #will use 3D list effect to extract prod boost and from prod boost, extract exact values to effect productivity
    def productivity_effect(self, name, id, productivity, effect):
        self.effect = effect 

        for i in len(effect): 
            if i[0] == "prod_boost":
                return productivity * i[1]
            elif i[0] == "prod_reduce": 
                return productivity / i[1]

    #will disable the effect and return everything to normal when the event is over
    def disable_prod_effect(self, name, id, productivity, effect): 
        self.effect = effect 

        for i in len(effect): 
            if i[0] == "prod_boost":
                return productivity / i[1]
            elif i[0] == "prod_reduce": 
                return productivity * i[1]

    #will use 3D list effect to extract income boost and from effect, extract exact values to effect productivity
    def income_effect(self, name, id, income, effect):
        self.effect = effect 

        for i in len(effect): 
            if i[0] == "income_boost":
                return income * i[1]
            elif i[0] == "income_reduce": 
                return income / i[0]

    #will disable the effect and return everything to normal when the event is over
    def disable_income_effect(self, name, id, income, effect): 
        self.effect = effect 

        for i in len(effect): 
            if i[0] == "income_boost":
                return income * i[1]
            elif i[0] == "prod_reduce": 
                return income / i[1]

    #Will effect wealth and depending on effect value, will reduce or boost it
    def wealth_effect(self, name, id, wealth, effect): 
        self.effect = effect 

        for i in len(effect): 
            if i[0] == "wealth_boost": 
                return wealth * i[1]
            elif i[0] == "wealth_reduce": 
                return wealth / i[1]

    #will disable the effect and return everything to normal when the event is over
    def disable_wealth_effect(self, name, id, wealth, effect): 
        self.effect = effect 

        for i in len(effect): 
            if i[0] == "wealth_boost": 
                return wealth / i[1]
            elif i[0] == "wealth_reduce": 
                return wealth * i[1]

    #Will effect pop and depending on value of effect, will reduce or boost pop by a certain amount
    #doesn't need a counter method
    def population_effect(self, name, id, population, effect): 
        self.effect = effect 
        
        for i in len(effect): 
            if i[0] == "pop_boost":
                return population * i[1]
            elif i[0] == "pop_reduce": 
                return population * i[1]