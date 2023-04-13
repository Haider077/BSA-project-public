from settings import *
import random as rand
import world as w
import eventhandler as e
import random

# turn object to increment year and quarter for each turn
class Turn():
    def __init__(self, player, AI_list, world_interface):
        self.AI_list = AI_list
        self.player = player
        self.current_year = INIT_YEAR
        self.q_index = 0
        self.world_ui = world_interface
        self.all_player = AI_list + [player]
        self.eventObj = e.eventhandler(self.world_ui)
        

    def nextTurn(self):
        self.world_ui.log.handleLogTurn(str (self.current_year ) + " Q# " + str(self.q_index + 1))
        self.eventObj.activate_event(rand.randint(1, 11))
        self.processSamplePlayer()
        self.process_Cities()
        self.process_year()
        self.tax_handling()
        self.world_ui.update_player_value()
        
        for player in self.all_player:
            # do not log if tha player go bankrupted
            if not player.bankrupted:
                self.world_ui.log.log("------")
                self.world_ui.log.log(f"{player.name} spent ${round(player.income / 10)} on taxation and ${round(player.maintenance_cost)} on store maintenance.")
                if player.expense == player.income:
                    self.world_ui.log.log(f"{player.name} did not generate any net profit this quarter.")
                elif player.expense > player.income:
                    self.world_ui.log.log(f"{player.name} lost ${round(player.expense - player.income)} this quarter.")
                else:
                    self.world_ui.log.log(f"{player.name} generated ${round(player.income - player.expense)} net profit this quarter.")

            player.income = 0
            player.expense = 0
        
        self.world_ui.log.update_log()

        for player in self.all_player:
            player.turn_reset()
        
        self.world_ui.log.open()
        

    def process_year(self):
        if self.q_index == 3:
            self.q_index = 0
            self.current_year += 1
        else:
            self.q_index += 1

    def processSamplePlayer(self):
        for AI in self.AI_list:
            if not AI.bankrupted:
                # borrow loan before buying or producing, also does not get activated in the first turn
                AI.ai_loan_handling()
                AI.aiPurchaseStore(w.global_cities)
                AI.aiSetProduction()
                AI.aiPurchaseWarehouse(self.getRandomCity())

        self.loan_handling()
        
    def process_Cities(self):
        """
        Calculate how many product each customer buy each turn.
        """
        def customer_purchase():
            if store.owner != None:
                for product in store.products:
                    # randomize the factor
                    factor = (random.randint(40, city.demand)) / 100
                    # tier factor for higher price's product
                    ratio = store.cost / product.value
                    if ratio < 5000:
                        factor *= 1.8
                    if ratio < 1000:
                        factor *= 1
                    if ratio < 500:
                        factor *= 0.8
                    if ratio < 100:
                        factor *= 0.6
                    if ratio < 50:
                        factor *= 0.4
                    if ratio < 10:
                        factor *= 0.1
                    num_to_buy = int(factor * (city.population / city.og_population) * product.quantity)
                    num_to_buy = 0 if num_to_buy <= 0 else num_to_buy
                    num_to_buy = product.quantity if num_to_buy > product.quantity else num_to_buy
                    product.quantity -= num_to_buy
                    
                    store.profitability += num_to_buy * product.value
                    store.owner.addCash(num_to_buy * product.value, "sale")

        """
        Slowly inflat product price and cost.
        """
        def adjust_products_price():
            for product in store.products:
                product.value *= 1 + (city.demand / 5 + random.randint(-int(city.demand / 10), int(city.demand / 10))) / 1000
                product.cost *= 1 + (city.demand / 5 + random.randint(-int(city.demand / 8), int(city.demand / 8))) / 1000

        def store_maintenance():
            if store.owner != None:
                store.owner.removeCash(store.cost * 0.05)
                # this will count towards expense
                store.owner.maintenance_cost += store.cost * 0.05
        
        def adjust_demand():
            # adjust wealth and demand of a city
            total_profit = 0
            # indicate whether the city has active stores
            empty_city = True
            for store in city.stores:
                total_profit += store.profitability
                if store.owner != None:
                    empty_city == False

            if not empty_city:
                if total_profit > 0:
                    city.wealth += random.randint(0, 1)
                    city.demand = int(city.wealth * (1 + round(random.uniform(0, 0.05), 2)))
                # if the profit is exactly 0, meaning that the city has not had any store bought, still wealth decreases
                else:
                    city.wealth -= random.randint(-1, 0)
                    city.demand = int(city.wealth * (1 + round(random.uniform(-0.025, 0.025), 2)))

        # decide how many product is bought here
        for city in w.global_cities:
            for store in city.stores:
                profitability = store.profitability if store.profitability > 0 else 0
                # here update the selling price of each store
                store.adjust_store_price()
                # reset the produced status
                store.produced = False
                customer_purchase()
                adjust_products_price()
                store_maintenance()

            # adjust demand for each city
            adjust_demand()
            # adjust the population
            city.calculatePop()

    def tax_handling(self):
        for player in self.all_player:
            if not player.bankrupted:
                # this will count towards expense
                player.removeCash(player.income * 0.1)

    def loan_handling(self):
        for player in self.all_player:
            # if the player has loan, deduct its maturity date
            player.maturity_date = player.maturity_date - 1 if player.maturity_date > 0 else 0
            if player.loan != 0 and player.maturity_date == 0:
                player.removeCash(player.loan * 1.3, "loan")
        
            # bankrupted handling
            if player.cash <= 0 and not player.bankrupted:
                player.cash = 0
                player.loan = 0
                self.world_ui.log.log(f"{player.name} has been kicked out from this cruel business world.")
                player.name += " (BANKRUPTED)"
                player.bankrupted = True
                for store in player.markets:
                    store.owner = None
                player.markets.clear()
            

    """
    Utility method to get random city.
    """
    def getRandomCity(self):
        return w.global_cities[rand.randint(0, len(w.global_cities) - 1)]


#CITIES

    # PROCESS CITY
    # city_demand += city_population + randomRange(0,city_population / 2)
    # city_population += randomRange(0,city_population / 10)


    # PROCESS STORES
    # foreach customer in city
    # odds for customer to buy product =  (productValue + city_demand) - (product_price * (city_wealth / 100)) 
    # if customer buys product : player_income += product_price, city_demand -= 1 