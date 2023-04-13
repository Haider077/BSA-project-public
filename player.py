
import random as rand
from ursina import *
from building import *
class Player():
    def __init__(self, name, markets, is_AI, world_interface):
        self.w = world_interface
        self.is_AI = is_AI
        self.name = name
        self.cash = 500000
        self.income = 0
        self.expense = 0
        self.total_income = 0
        self.total_expense = 0
        self.marketingBudget = 0
        # a list of store object
        self.markets = markets
        self.warehouses = []
        self.product_sale = 0
        self.production_cost = 0
        self.store_cost = 0
        self.loan = 0
        self.maturity_date = 0
        self.maintenance_cost = 0
        self.bankrupted = False

    def getCash(self): 
        return self.cash

    def getIncome(self): 
        return self.income

    def getMarkets(self): 
        return self.markets

    def addCash(self, amount, type = None):
        self.cash += amount
        self.income += amount
        self.total_income += amount
        if type == "sale":
            self.product_sale += amount
        # handling loan
        elif type == "loan":
            # if the maturity date is 0, meaning the player has repaid all loan
            # allow the user to refresh the maturity date upon new loan
            if self.maturity_date == 0:
                self.maturity_date = 2
            # if the player has loan, and the amount borrowed is bigger then the current loan,
            # allow the user refresh the maturity date
            # this also prevents player from borrowing small amount to refresh the maturity date
            elif self.loan != 0 and amount > self.loan:
                # the maximum that the maturity date can expand is 3 quarters
                if self.maturity_date < 3:
                    self.maturity_date += 1
                else:
                    self.maturity_date = 3
            # loan does not count towards income, interest does
            self.income -= amount
            self.total_income -= amount
            # add the interest to the expense
            self.total_expense += amount * 1.2 - amount
            # 20% fixed rate interest
            self.loan += amount * 1.2

    
    def removeCash(self, amount, type = None):
        self.cash -= amount
        self.expense += amount
        self.total_expense += amount
        if type == "produce":
            self.production_cost += amount
        elif type == "buy":
            self.store_cost += amount
        elif type == "loan":
            # loan does not count towards expense
            # interest does
            self.expense -= amount
            self.total_expense -= amount
            # if the maturity date comes, the interest will be increased by 30%, put it into expense too
            if self.maturity_date == 0:
                self.expense += amount - amount // 1.3
                self.total_expense += amount - amount // 1.3
                # update the loan with new interest first if the 30% is newly added upon
                self.loan += amount - amount // 1.3
            # if the loan is still more than the amount, deduct the amount
            # if the loan is less than the amount, reset the loan to 0 (loan - loan)
            self.loan -= amount if self.loan >= amount else self.loan
            # if all loan is paid off, reset maturity date
            if self.loan == 0:
                self.maturity_date = 0

    def setCash(self, amount):
        self.cash = amount

    def aiPurchaseWarehouse(self,city):
            if(self.cash > WAREHOUSE_COST and rand.randint(0,100) > 75):
                warehouse = Warehouse(city.position + Vec3(rand.uniform(-0.3,0.3),0,rand.uniform(-0.3,0.3)))
                self.cash -= WAREHOUSE_COST

    def aiPurchaseStore(self, city_list):
        if self.bankrupted: return
        # shuffle the city list every time
        random.shuffle(city_list)
        for i, city in enumerate(city_list):
            # about 5 out of 15 cities they will buy store in
            if i % 3 == 0:
                for store in city.stores:
                    # about 50% of the store they will check in
                    if random.randint(0, 100) > 50:
                        # they will only buy store if they have 10 times more cash and the store is worth acquiring
                        if self.cash >= store.cost * 10 or (len(self.markets) == 0 and self.cash >= store.cost):
                            if store.owner == None:
                                self.addStore(store)
                                self.removeCash(store.cost, "buy")
                                self.w.log.log(self.name + " purchased a " + store.name + " store in " + city.name + ".")
                            elif store.owner != self:
                                # about 30% of the chance they will buy a store from others
                                if random.randint(0, 100) > 70 and store.profitability >= 0:
                                    original_owner = store.owner
                                    original_owner.markets.remove(store)
                                    original_owner.addCash(store.cost)
                                    self.addStore(store)
                                    self.removeCash(store.cost, "buy")
                                    self.w.log.log(self.name + " acquired a " + store.name + " in " + city.name + " from " + original_owner.name + ".")

    def aiMarketingBudget(self):
        self.marketingBudget = self.cash/10 #temporary

    
    def aiSetProduction(self):
        if self.bankrupted: return
        for store in self.markets:
            for product in store.products:
                # here determine the maximum amount that each product can be produced
                max = int((store.cost) / product.cost / len(store.products) * (store.productivity / 100))
                max = 0 if max <= 0 else max
                num_to_produce = 0
                # factor to determine how many product the AI produce
                high_produce = random.randint(90, 100) / 100
                mid_produce = random.randint(80, 90) / 100
                low_produce = random.randint(70, 80) / 100
                # here limit how many products AI will produce
                
                # if the stock is already a lot, meaning the product does not sell much, stop producing
                # if the profitability is too low, stop producing
                # always leave some cash so that the AI won't go bankrupt in short
                if store.profitability >= -store.og_cost * 5 and self.cash > store.og_cost / 10:
                    # if there is profitability, max out the product that one can produce
                    if self.cash > product.cost * max and store.profitability >= store.og_cost * 2:
                        num_to_produce = max
                    elif self.cash > product.cost * (max * high_produce) and store.profitability >= store.og_cost:
                        num_to_produce = max * high_produce
                    elif self.cash > product.cost * (max * mid_produce) and store.profitability >= 0:
                        num_to_produce = max * mid_produce
                    elif self.cash > product.cost * (max * low_produce) and store.profitability < 0:
                        num_to_produce = max * low_produce

                product.quantity += int(num_to_produce)
                self.removeCash(int(num_to_produce) * product.cost, "produce")
                store.profitability -= product.quantity * product.cost

    """
    Handling AI borrowing loan and repaying loan actions.
    """
    def ai_loan_handling(self):
        if self.bankrupted: return
        # this flag is to prevent the ai repay the money and then borrow right after
        repaid = False
        repay_amount = 0
        # here determines when the AI repay the loan
        if self.maturity_date == 1:
            # if next quarter is the due date then repay all the loan to prevent 30% penalty
            if self.cash > self.loan:
                repay_amount = self.loan
            # in case where player does not have much money, also leave 10k for production in case the loan is un-repayable
            # that way the AI can risk producing product hoping to get more profit to repay the loan
            else:
                # if the player has more than 10k, then pay all the exceeding amount and leave 10k
                if self.cash > 100000:
                    repay_amount = self.cash - 100000
                # if the player has less than 10k, then leave 50%
                else:
                    repay_amount = self.cash * 0.5
       
        if repay_amount != 0:
            self.removeCash(repay_amount, "loan")
            repaid = True

        # here determines how many loan will the AI actually borrow
        borrow_amount = 0
        # here determines the maximum amount that the AI can loan
        max_amount = 0

        # here determines how much the AI will loan
        if not repaid:
            for store in self.markets:
                max_amount += (store.cost + store.profitability) / 1.5
            max_amount = int(max_amount - self.loan) if self.cash > 0 else 0
            max_amount = max_amount if max_amount > 0 else 0

            # if the player has loan
            if self.loan != 0:
                # if the amount is bigger than the amount the AI owned, borrow slightly more than the amount owned to extend the maturity date
                if max_amount > self.loan:
                    borrow_amount = self.loan * 1.1 if self.loan * 1.1 < borrow_amount else max_amount
                # if loan cannot be extended due to small available amount, but the AI has the potential to payback
                elif self.cash >= max_amount:
                    borrow_amount = max_amount
                # this option is risky, the AI wants to borrow more than what he has, gamblier mindset
                elif self.cash <= max_amount:
                    borrow_amount = self.cash * (random.ranint(0, ))

                # the AI risks it all
                if self.cash < 100000:
                    borrow_amount = max_amount

            # if the player does not have loan
            else:
                borrow_amount = max_amount * (random.randint(60, 100) / 100)
            
            # add money to the AI
            if borrow_amount != 0:
                self.addCash(borrow_amount, "loan")

    def addStore(self, store):
        store.owner = self
        self.markets.append(store)

    def turn_reset(self):
        self.income = 0
        self.expense = 0
        self.maintenance_cost = 0
