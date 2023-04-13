import requests # Use pip install requests, this is the library used to make GET requests
from decouple import config #ensure python-decouple is installed, not decouple, they are different libraries

IP = "34.68.120.149"
PORT = "8080"

ADDRESS = "http://" + IP + ":" + PORT + "/"


#API Endpoints:

# Get Status - Check if Server is running
# Get Cities - Acquire list of cities from API
# Get Stores - Acquire list of stores from API
# Get Products - Acquire list of products from API
# Get Events - Acquire list of events from API

def get_status():
    response = requests.get(ADDRESS)

    if (response.status_code==200):
        return True
    else:
        return False

def get_cities():
    response = requests.get(ADDRESS + "api/cities/")

    if (response.status_code==200):
        data = response.json()
        return data
    else:
        return 0


def get_stores():
    response = requests.get(ADDRESS + "api/stores/")

    if (response.status_code==200):
        data = response.json()
        return data
    else:
        return 0


def get_products():
    response = requests.get(ADDRESS + "api/products/")

    if (response.status_code==200):
        data = response.json()
        return data
    else:
        return 0

def get_events():
    response = requests.get(ADDRESS + "api/events/")

    if (response.status_code==200):
        data = response.json()
        return data
    else:
        return 0
