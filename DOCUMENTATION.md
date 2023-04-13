# Documentation 

Daniel Faratro

Haider Amin

Sam Tang

Moonum Azmi

Instructor: Yasaman Amannejad

Date: 08 Dec 2022

###

## Installation Guidelines 

1. To run the program, proper dependencies must be installed into the system. If run without them, this program will not function. Please note that quotations are there to make it easier to define the exact command from the text, and thus must be removed when inputting them into the console. 

    * If you do not have Python installed, please download the newest version or relatively new version of Python here: https://www.python.org/downloads/. The latest version of python is --version 3.11, if this does not work install python --version 3.10.9

    * Begin by installing Ursina --Version 5.0.0. Be very careful not to install via the command "pip install Ursina", as that will download a version that is incompatible with our program. Instead, try "pip install ursina==5.0.0"

    * Install decouple via the command "pip install python-decouple", be very careful not to input the command "pip install decouple" as this 
      will not run the program correctly.  

    * Install the requests module via the command "pip install requests"

    * Install the numpy module via the command "pip install numpy"

2. After installing these dependencies, your program should be good to go. If the server is not functional, please email <Sam's Email> in order for him to activate the server that holds the database. After all that is done, your program should be good to go. 

**World**

The generation for the actual world is primarily done in World.py, and more specifically the createWorld method. Using built in Ursina methods, we: 

 * Set a skybox and a terrain
 * Colored the skybox black 
 * Used a world map image called render.png, for the terrain. We also set and scaled the image accordingly to fit the size of the screen. These scaling parameters are contained within Settings

## Program description 

**Interface** 

The UI interface is primarily handled within the WorldInterface class in interface.py, though other classes have a hand in manipulating the information shown in the generated interfaces. Most of the UI onscreen is generated through the interface class, though some exceptions do exist like the event window.

Interfaces generated include: 
    * Log Button 
    * Menu Button 
    * Next turn button 
    * Back to world button 
    * City information window 
    * Dropdown menu 
    * Store buying window
    * Cash tab
    * Personal info 
    * Loan window

As stated before, information within the menu's are manipulated in other classes depending on the information needing to be shown. City and store menus utilize city object information, and with world interface being a parameter passed during the creation of cities we can easily access methods and world interface information to load up content pertaining to information of a unique city object and its stores. Additional logic pertaining to the ability to buy and trade stores are also contained other classes like city and/or store.

**Simulation** 

Simulation is handled within the simulation class, and will deal with behavior related to turning the time of the simulation and activating the resulting effects of time passing. Such effects may include the generation of events, the finalizing of store sales, adjustment of product prices, store maintenance costs, demand adjustments within every city and their respective stores, tax application and loan handling. It contains: 

    *AI player list 
    *The player
    *Current Year 
    *Current quarter
    *World_ui for world interface interaction 
    *A list of all players 

Simulation and it's related methods will focus on altering some of the UI to indicate that the year or quarter has changed, and will also determine if a player is bankrupted, will activate player ai behaviors which are detailed in the AI section, having customers purchase an X amount of products depending on demand which is dependant, create a constantly changing economic environment thorugh product price adjustments and demand adjustments, as well as determining loan status by increasing maturity and removing player cash.  

**Cities**

The generation of cities begins in the World class. It is here that information from the database regarding cities is loaded into individual city objects, with each city object containing information unique to a city. Such information includes: 

    * Name of the city  
    * Longitude and latitude of the city 
    * Population of the city 
    * The wealth level of the city 
    * The types of stores the city may contain 
    * The world interface itself, so that the interface may link with and produce User interfaces containing information unique to a city

Cites on the map are represented by models city1.obj and are textured with bld1.png. These models, with the help of ursina, can be interacted with by a mouse click which will then generate the requisite information utilizing interfaces. They will be positioned according to the longitude and latitude parameters of the city. Cities also contain hidden parameters like demand which are influenced by the cities wealth level. The city's wealth value is also able to influence store productivity levels to simulate the behavior. Contained within the City class are also methods to update the interface, and depending on the player's state, the cities state, and another AI's state, will be updated accordingly 

City methods deal primarily in the alteration of the Interfaces, though other methods do exist allowing it function outside of that specific purpose. The zoom method is the code that allows the camera to home in on a city that is clicked to serve as a visual confirmation that the user is indeed interacting with that store at that location. The other method, update, is related to the behavior of the 3D models, its change in color, and it's rotation 

**Store** 

Stores will be appended to each city depending on the parameters the cities were loaded in with from the api. Each store will contain a unique set of products indicated within the STORE_MAP value inside of Settings, through which the user will be able to produce during an in game session. 

Stores themselves will contain variables that define a store and work in tandem with the game's simulated economic system to produce invariance within buying behavior and thus requiring the player to strategize in order to acheive success. Stores also have a hand in producing interfaces through loading it with information that is unique to each store within a set of stores contained by the city. 

Products are also created within the store class through a method and are stored as product objects within it, utilizing the aforementioned STORE_MAP in order to populate the list. 

The store class also contains a method relating to store costs, which will adjust a store's cost value. 

**Player** 

There will be five players in a game at any given moment, and one of them will be the main player. Represented by the name "Human", the Player contains many values that are central to interacting with and operating within the game's economic system. Such values include 

    * w for World Interface interaction 
    * is_Ai to determine if the player is AI or not 
    * name 
    * Cash
    * Income for current quarter
    * Expenses for current quarter  
    * Total Income  
    * Total Expenses 
    * Markets (which is stores)
    * Loan
    * Maturity date 
    * Bankrupted status which will turn true when bankrupted 

Some values are excluded since they pertain only to an AI player, though AI player's share all of the same values as human player does. 

Most player methods pertain to AI which will be explained in the next section, but standard player methods include adding, getting, setting or removing cash, retrieving income, retrieving markets adding stores via appending a player as an owner, and a reset to reset income, expense and maintenance costs. Within the cash methods, loan behavior is also defined and changes certain values like maturity date in order to simulate the financial effects a loan may have on a person/company. 

**AI** 

This is the second type of player that is produced, and is an integral part in the game as it produces the competition necessary to simulate a regular economy. An AI player is liable to act and interact with the world on a similar level to the player albeit artificially. This includes buying stores, taking loans, getting bankrupt, repaying loan in time to prevent extra 30% interest, borrowing more loan to extend the maturity date.

A lot of AI player behavior is defined within the player class, and is crucial to creating and simulating behavior to have them change the economic landscape surrounding the player. 

Ais are able to buy stores based upon a randomly generated value through the API retrieved list of cities. When it has chosen a city, it will decide to buy a store based on a variety of factors:
    
    * They will only check 1/3 of the stores 
    * They have 10 times more cash than the store is worth 
    * If the store is worth acquiring

Additionally, they will be able to purchase stores from other players based on a 30 percent chance. Should they buy a store from another player, costs incurred during production will not be transferred over to them. 

AI will have additional behavior to begin producing items within stores to make money. By determining the max amount of products that can be stored, producing high, mid and low produce factors, and checking existing stock states, as well as having prebuilt behavior to prevent the AI from bankrupting theirselves in buying profitability, we can simulate behavior to restock their stores. 

AI will also have the ability to obtain loans, and will have factors to randomize when they will pay it off, if they can pay it off, how much they've borrowed and how much do they want to borrow while weighing it according to their current state

AI activity within cities will produce a warehouse model by the city as a visual indicator that a competitor is residing at that city.   

AI presence within a store will be indicated by warehouse models on the map.

**Demand** 

Demand of a city is randomized and will be dependant on a city's wealth value. Demand is important to consider since within a particular store, if the demand for a product is particularly low little profit will be generated for sales, though items in stock can always be sold later. 

**Logger** 

There is a logger at the bottom of the screen that generates ai player activity such as store purchasing, loans, bankrupt status and event generation. 

Logger is specifically modified built-in Ursina textfield that will not allow players to edit text but merely view it. Logger will only view information from the last quarter in order to allow the player to plan their next approach and also to remember any moves made in the last quarter 

**Settings**

Our settings contain information that is related to UIs, specifically size and positional coordinates, model colors, button colors, Camera coordinates and position in the Ursina generated world, coordinates, and a map of store products that a particular store will have available to produce.

