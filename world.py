from ursina import *
from city import City
from utils import load_json
from settings import *
from api import *

global_cities = []

"""
Create nodes for different city according to the city_info.json
Return a dict: {name: City object}
"""
def create_city(world_interface):
    city_info = get_cities()
    for city in city_info:
        # pass in name of the city, latitude and longitude, and population info
        city_obj = City(city["name"],
            city["country"],
            [city["latitude"], city["longitude"]],
            city["population"],
            city["wealth"],
            city["desc"],
            city["store"],
            world_interface)

        global_cities.append(city_obj)


def createWorld():
    Sky(color = color.black)
    world = Entity(
        model = Terrain('resources/render.png', skip = 8),
        scale = (WORLD_X_SIZE, WORLD_HEIGHT, WORLD_Y_SIZE),
        texture='resources/render.png')
    return world
