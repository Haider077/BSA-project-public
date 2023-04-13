import json
from settings import *
from ursina import invoke

def load_json(filename):
    file = open(filename)
    data = json.load(file)
    file.close()
    return data

def getXYCoordinates(lati, longi):
    longi = (longi/LONG_RANGE) * LONG_FACTOR
    lati = (lati/LATI_RANGE) * LATI_FACTOR
    coordinates = [longi, lati]
    return coordinates