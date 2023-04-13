from settings import *
from product import Product
import json
from api import *

products = get_products()

class Store():
    def __init__(self, name, city, cost, productivity):
        # name of the store, e.g., Vehicle Store
        self.name = name
        # the city where it belongs
        self.city = city
        # None means it is not owned by any player
        self.owner = None
        self.cost = cost
        self.og_cost = cost
        self.productivity = productivity
        self.profitability = 0
        # a list storing Product object that available in that store
        self.products = []
        # indicate if the player has already produced products in that store
        self.produced = False
        self.create_products()
        self.adjust_store_price()
    
    def create_products(self):
        for product in products:
            if product["name"] in STORE_MAP[self.name]:
                value = product["value"]
                cost = product["cost"]
                self.products.append(Product(product["name"], value, cost))

    def adjust_store_price(self):
        store_cost_increase = 0
        for i, product in enumerate(self.products):
            store_cost_increase = product.value * (len(self.products) - i) * 10
        if self.profitability / 2 + self.og_cost + store_cost_increase > self.og_cost:
            self.cost = self.profitability / 2 + self.og_cost + store_cost_increase
        else:
            self.cost = self.og_cost

    def getCity(self):
        return self.city