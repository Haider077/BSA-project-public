import json

## reads the json files and prints as insert statements in console

#sketchy, but it works

with open('./json/store_info.json', 'r') as f:
    store_json = json.load(f)

    for key in store_json:
        name = key
        cost = store_json[key]["cost"]
        productivity = store_json[key]["productivity"]
        
        query = f'INSERT INTO store VALUES (\'{name}\', {cost}, {productivity});'
        print(query)


with open('./json/event.json', 'r') as f:
    event_json = json.load(f)

    for key in event_json:
        id = key
        name = event_json[key]["name"]
        desc = event_json[key]["description"]
        
        query = f'INSERT INTO events VALUES ({id}, \'{name}\', \'{desc}\');'
        print(query)

with open('./json/product_info.json', 'r') as f:
    prod_json = json.load(f)

    for key in prod_json:
        name = key
        value = prod_json[key]["value"]
        cost = prod_json[key]["cost"]
        
        query = f'INSERT INTO product VALUES (\'{name}\', {value}, {cost});'
        print(query)

with open('./json/city_info.json', 'r') as f:
    city_json = json.load(f)

    for key in city_json:
        name = key
        country = city_json[key]["country"]
        population = city_json[key]["population"]
        position = city_json[key]["position"]
        desc = city_json[key]["description"]
        wealth = city_json[key]["wealth"]
        store = city_json[key]["store"]
        
        query = f'INSERT INTO city VALUES (\"{name}\", \"{country}\", {population}, \"{position}\", \"{desc}\", {wealth}, \"{store}\");'
        print(query)
