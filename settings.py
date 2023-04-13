from ursina import color

RESOLUTION = (1920, 1080)

CITY_NODE_COLOR = (60, 1 , 1 ,0.6)
THEME_COLOR = color.rgba(0, 255, 255, 255)
WINDOW_COLOR = color.rgba(0, 0, 0, 255)
GREY = color.rgba(150, 150, 150)

CITY_INFO_FILE = ".\\json\\city_info.json"

WORLD_X_SIZE = 10
WORLD_Y_SIZE = 10
WORLD_HEIGHT = 0.1

LONG_FACTOR = 2.7
LATI_FACTOR = 6.25
LONG_RANGE = 90
LATI_RANGE = 180

CAMERA_POS = (0, 10, -10)
CAMERA_ROTATION_X = 45

ZOOM_HEIGHT = 7

# window Panels
CITY_INFO_SIZE = (0.45, 0.052)
CITY_INFO_POS = (-0.65, 0.482)
STORE_INFO_SIZE = (0.5, 0.038)
STORE_INFO_POS = (-0.16, 0.482)
CONFIRM_WIN_SIZE = (0.56, 0.08)
CONFIRM_WIN_POS = (0, 0.2)
MENU_WIN_SIZE = (0.6, 0.08)
MENU_WIN_POS = (0, 0.3)
HOW_TO_SIZE = (0.75, 0.045)
HOW_TO_POS = (0, 0.4)
PLAYER_INFO_SIZE = (0.42, 0.035)
PLAYER_INFO_POS = (0.315, 0.482)
LOAN_PANEL_SIZE = (0.34, 0.05)
LOAN_PANEL_POS = (0.71, 0.34)
REPAY_PANEL_POS = (0.71, 0.068)
SERVER_WIN_SIZE = (0.5, 0.04)

# dropdown Menus
DROPDOWN_POS = (-0.875, 0.22)

# buttons
BACK_TO_WORLD_SIZE = (0.15, 0.08, 0.15)
BACK_TO_WORLD_POS = (0.8, -0.445)
NEXT_TURN_SIZE = (0.15, 0.08, 0.15)
NEXT_TURN_POS = (0.8, -0.36)
PLAYER_BUTTON_SIZE = (0.15, 0.08, 0.15)
PLAYER_BUTTON_POS = (-0.8, -0.36)
MENU_BUTTON_SIZE = (0.15, 0.08, 0.15)
MENU_BUTTON_POS = (-0.8, -0.445)

# info tab
CASH_TAB_SIZE = (0.17, 0.08, 0.20)
CASH_TAB_POS = (0.79, 0.435)

# a map that list what products are available in which store
STORE_MAP = {
    "Vehicle Store": ["Sedan", "Truck", "SUV", "Electric Vehicle", "Luxury Vehicle"],
    "Computer Store": ["Cell Phone", "Laptop", "Office PC", "Gaming PC", "Workstation PC"],
    "Fashion Store": ["Luxury Accessories", "Luxury Clothes", "Luxury Handbag", "Luxury Watch"],
    "Bicycle Store": ["Tricycle", "City Bike", "Mountain Bike", "Racing Bike"],
    "Shoe Store": ["Basic Sneakers", "Shoes", "Boot", "Brand Shoes"],
    "Media Store": ["Music DVD", "Vinyl Album", "Video Game", "Movie DVD"],
    "Hardware Store": ["Basic Tools", "Quality Tools", "Power Tools"],
    "Book Store": ["Novel", "Cook Book", "Art Book", "Textbook"],
    "Boat Store": ["Dinghy", "Jet Ski", "Motorboat", "Jet Boat", "Yacht"]
}

# initial values for current year and quarter
INIT_YEAR = 2022
QUARTERS = ["Q1", "Q2", "Q3", "Q4"]