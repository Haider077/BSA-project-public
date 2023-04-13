from asyncio.windows_events import NULL
from ursina import *
from settings import *
from store import Store
from utils import getXYCoordinates
import json
from random import randint, uniform
from api import *
import random

stores = get_stores()

class City(Entity):
    def __init__(self, name, country, pos, population, wealth, description, stores, world_interface):
        super().__init__(
            # model = Cylinder(12, start = -0.5),
            model = 'resources/city1.obj',
            color = color.color(*CITY_NODE_COLOR),
            texture = 'resources/bld1.png',
            position = (getXYCoordinates(*pos)[0], 0.1, getXYCoordinates(*pos)[1]),
            scale = .05,
            collider = 'mesh',
            rotation = (0, 45, 0),
            on_click = self.show_city_info)

        # randomize the starting frame
        self.rotation_y = random.randint(0, 360)
        self.click = Audio("resources/confirmation_001.ogg", pitch=1, loop=False, autoplay=False)
        # the city info ui that show the city name and population
        self.world_ui = world_interface
        self.country = country
        self.name = name
        self.population = population
        self.og_population = population
        self.description = description
        self.wordwrap = 40
        self.wealth = wealth
        # the inital demand will determined by wealth +- 10% for rich countries
        # 0% to +20% to poor country
        self.demand = int(wealth * (1 + round(random.uniform(-0.2, 0.1), 2))) if wealth >= 80 \
            else int(wealth * (1 + round(random.uniform(0.0, 0.2), 2)))
       
        # a list storing the string of the store
        # e.g., ["Vehicle Store", "Computer Store"]
        self.store_list = stores.split(",")

        # a list storing Store object
        self.stores = []
        self.create_stores()

        #tooltip creator over cities 

    def create_stores(self):
        for store_str in self.store_list:
            for store in stores:
                if store_str == store["name"]:
                    cost = store["cost"] * (1 + self.wealth / 100) * (1 + (randint(-30, 30) / 100))
                    productivity = store["production"]
                    self.stores.append(Store(store["name"], self, cost, productivity))

    """
    Show city related information on the city info ui upon click
    """
    def show_city_info(self):
        self.click.play()
        self.world_ui.selected_city = self
        # change the title of the box, which contains the name of the city
        self.world_ui.city_info.text = self.name

        # make different window panels visible or invisible
        self.world_ui.city_info.enabled = True
        self.world_ui.dropdown.enabled = True
        self.world_ui.store_info.enabled = False
        for window in self.world_ui.full_screen_window:
            window.enabled = False

        # reset selected store index
        self.world_ui.selected_store = 0

        # change the text of the text entity of the WorldInterface
        # will also change the text shown in the city_info_ui of the WorldInterface
        self.world_ui.population_entity.text = "Population: " + f"{self.population: ,}"
        self.world_ui.country_entity.text = "Country: " + self.country
        self.world_ui.wealth_entity.text = "Wealth: " + str(round(self.wealth))
        self.world_ui.description_entity.text = "Description: " + self.description

        # warp the description
        self.world_ui.description_entity.wordwrap = self.wordwrap
        self.zoom()
    
    def show_store_info(self):
        # make different window panels visible or invisible
        self.world_ui.store_info.enabled = True
        for window in self.world_ui.full_screen_window:
            window.enabled = False
        # reset all slider
        for slider in self.world_ui.slider_entities:
            slider.value = 0

        store = self.stores[self.world_ui.selected_store]
        # displayer the store name and index
        self.world_ui.store_info.text = f"{store.name} [{self.world_ui.selected_store + 1}/{len(self.stores)}]"
        # display the name of the owner
        self.world_ui.owner_entity.text = "Owner: " + store.owner.name + " <image:resources/personal.png>"\
            if store.owner != None \
                else "Owner: None"
        # display the selling price of the selected store
        self.world_ui.cost_entity.text = f"Selling price: ${round(store.cost): ,}"
        # display the profitability
        self.world_ui.profitability_entity.text = f"Profitability: ${round(self.stores[self.world_ui.selected_store].profitability)}"
        
        # disable all the product and slider, and re-enable it later according to its presence
        for content in self.world_ui.store_info.content:
            if content in self.world_ui.product_entities or content in self.world_ui.slider_entities:
                content.enabled = False
        
        self.display_product_info()
        self.change_button_color()

        # when ever change to another store, reset the total cost
        self.world_ui.total_cost_entity.cost = 0
        self.world_ui.total_cost_entity.text = f"Total Cost: ${round(self.world_ui.total_cost_entity.cost): ,}"

        if store.produced:
            self.world_ui.total_cost_entity.enabled = False
        else:
            self.world_ui.total_cost_entity.enabled = True

    """
    Show the product info according to how many products one store has.
    """
    def display_product_info(self):
        # short instance of selected store
        store = self.stores[self.world_ui.selected_store]

        for i, product in enumerate(store.products):
            # for product information
            if store.owner == self.world_ui.player:
                self.world_ui.product_entities[i].text = f"{product.name} (Price: ${round(product.value): ,} / Cost: ${round(product.cost): ,}) [Stock: {str(product.quantity)}]"
                self.world_ui.slider_entities[i].enabled = True
            else:
                self.world_ui.product_entities[i].text = f"{product.name} (Price: ${round(product.value): ,})"

            self.world_ui.product_entities[i].enabled = True

            if not store.produced:
                # determinate how many product can be produced each round according to product cost, number of product, and productivity
                max = int((store.cost) / product.cost / len(store.products) * (store.productivity / 100))
                max = 0 if max <= 0 else max
                self.world_ui.slider_entities[i].max = max
            else:
                self.world_ui.slider_entities[i].enabled = False

    """
    Change the color button depending on different situation.
    Also changing the prompt of the tooltips
    """
    def change_button_color(self):
        # short instance of selected store
        store = self.stores[self.world_ui.selected_store]

        for entity in self.world_ui.store_info.content:
            if type(entity) == Button:
                # disable the tooltip to prevent it from constantly popping
                if entity.action == "buy":
                    entity.tooltip.enabled = False
                    # change buy option to acquisition if the store is owned by someon
                    if store.owner != self.world_ui.player and store.owner != None:
                        entity.text_entity.text = "Acquisition <image:resources/acquire.png>"
                        entity.tooltip =  Tooltip("Make an acquisition request to the store owner", scale = 0.7)
                    elif store.owner == self.world_ui.player:
                        entity.text_entity.text = "Owned <image:resources/personal.png>"
                        entity.tooltip = Tooltip("You already owned this store", scale = 0.7)
                    else:
                        entity.text_entity.text = "Buy Store <image:resources/buy.png>"
                        entity.tooltip = Tooltip("Purchase this store", scale = 0.7)

                    # turn the buy store button to grey if the player does not have enough money
                    # also if the player own the store, it shows that the store is not allowed to buy again
                    if self.world_ui.player.cash < self.stores[self.world_ui.selected_store].cost \
                        or store.owner == self.world_ui.player:
                        entity.color = GREY
                        entity.highlight_color = GREY
                        entity.pressed_color = GREY
                    else:
                        entity.color = color.azure
                        entity.highlight_color = color.azure.tint(.2)
                        entity.pressed_color = color.azure.tint(-.2)

                if entity.action == "produce":
                    # disable the tooltip to prevent it from constantly popping
                    entity.tooltip.enabled = False
                    # if the store is owned by other
                    if store.owner != self.world_ui.player and store.owner != None:
                        entity.text_entity.text = "Production Owned by Others <image:resources/notallowed.png>"
                        entity.tooltip = Tooltip("You need to make an acquisition to start producing", scale = 0.7)
                    # if the store is owned by the player and has produced
                    elif store.owner == self.world_ui.player and store.produced:
                        entity.text_entity.text = "Produced  <image:resources/done.png>"
                        entity.tooltip = Tooltip("This store is producing products", scale = 0.7)
                    elif store.owner == self.world_ui.player and not store.produced:
                        entity.text_entity.text = "Produce Product <image:resources/produce.png>"
                        entity.tooltip = Tooltip("Start producing selected products", scale = 0.7)
                    else:
                        entity.text_entity.text = "Production Disabled <image:resources/notallowed.png>"
                        entity.tooltip = Tooltip("Buy the store to start production", scale = 0.7)

                    # in case the store owner is not the player or the store already produced
                    if store.owner != self.world_ui.player \
                        or store.produced \
                        or self.world_ui.total_cost_entity.cost > self.world_ui.player.cash \
                        or self.world_ui.total_cost_entity.cost == 0:
                        entity.color = GREY
                        entity.highlight_color = GREY
                        entity.pressed_color = GREY
                    # if the store is not owned by the player and the store has not produced
                    else:
                        entity.color = color.azure
                        entity.highlight_color = color.azure.tint(.2)
                        entity.pressed_color = color.azure.tint(-.2)

    """
    Zoom to the correct position using the city node as the center
    """
    def zoom(self):
        self.world_ui.city_info.visible = True
        # move the camerea x to the node x
        camera.animate_x(self.position.x, duration = 0.7)
        # move the camera y (height) to set height
        camera.animate_y(ZOOM_HEIGHT, duration = 0.7)
        camera.animate_z(self.position.z - 7, duration = 0.7)

    # update method in Entity will be called every loop
    def update(self):
        # reset color
        self.color = color.yellow
        # self rotating
        self.rotation_y += 30 * time.dt
        # change color if the owner has store in that city
        for store in self.stores:
            if store.owner == self.world_ui.player:
                self.color = color.azure
        
        # assuming that not every store in that city is produced
        fully_produced = False
        # if the color == azure, player has store in that city, then assume all the stores are produced
        if self.color == color.azure:
            fully_produced = True
        for store in self.stores:
            if store.owner == self.world_ui.player:
                if not store.produced:
                    # turn this flag to false if there is a store not producing
                    fully_produced = False

        # change the color when the player has produced in all store in that city
        if fully_produced:
            self.color = color.green
            

    #determines the cities population at the end of each turn
    def calculatePop(self):
        self.population += int(random.randint(-int(self.population + self.wealth), int(self.wealth + self.population))/(self.population / 10000))

    
