from ursina import *                    # Import the ursina engine
import textwrap
from settings import *
from ursina import invoke
from ursina.prefabs.dropdown_menu import DropdownMenu, DropdownMenuButton
from player import Player
from simulation import Turn
from events import *
import world as w
from Logger import *

class WorldInterface():
    def __init__(self):
        self.selected_city = None
        self.log = Logger(self)
        # index of the store that used to navigate through different stores within the same city
        self.selected_store = 0
        self.selected_player = 0
        self.player = self.create_player()
        self.AI_list = self.create_AI(["Daniel", "Haider", "Moonum", "Sam"])
        self.all_player = [self.player] + self.AI_list
        self.full_screen_window = []
        self.create_city_info()
        self.create_store_info()
        self.create_menu_window()
        self.create_howto()
        self.create_player_info()
        self.create_button()
        self.create_server_window()


        self.click = Audio("resources/confirmation_001.ogg", pitch=1, loop=False, autoplay=False)
        #self.confirm = Audio("resources/confirmation_001.ogg", pitch=1, loop=False, autoplay=False)
        self.a = Audio("resources/superbased.mp3", pitch=1, loop=True, autoplay=True)

        self.a.play()
        
        #create window that constantly reminds player of cash value 
        #self.create_tab(self.player.getCash())
        self.turn = Turn(self.player, self.AI_list, self)

        # creates a turn counter above the next turn button
        self.current_turn = Text(
            text = "Current Turn: \n    " + str(self.turn.current_year) + ", " + QUARTERS[self.turn.q_index],
            scale = 0.68,
            x = 0.75,
            y = -0.27)

    def create_player(self):
        wi = self
        player = Player("Human", [], False,wi)
        return player

    def create_AI(self,names):
        AI_list = []
        for name in names:
            AI = Player(name, [], True,self)
            AI_list.append(AI)
        return AI_list


    # dialogue window for case where API does not respond
    # there should be code for when get_status in api.py is called, this window appears

    def create_server_window(self):
        def close_server_window():
            self.click.play()
            self.server_window.enabled = False
            #retry connection method go here

        self.server_window = WindowPanel(
            scale = SERVER_WIN_SIZE,
            color = WINDOW_COLOR,
            position = CONFIRM_WIN_POS,
            text = "Connection Error",
            lock = Vec3(1, 1, 1),
            content=[
                Text("Could not connect to server,\n it may be offline at this time."),
                Button("Retry", onclick = close_server_window)],
            enabled = False)

        self.server_window.content[0].position = (-0.3, -1.6)
        self.server_window.content[0].scale *= 0.9
        self.server_window.content[1].position = (0, -3.8)
        self.server_window.content[1].scale *= 0.9

        self.full_screen_window.append(self.server_window)

        return self.server_window

    """
    A handy method that create the confirmation window panel.
    Take in a string that will pop up in the window.
    Also take in a function that will be called if "Yes" is clicked.
    """
    def create_confirm_window(self, function):
        def close_confirm_window():
            self.click.play()
            confirm_window.enabled = False
            # if the method is buy_store(), also re-enable the store ui after clicking "No"
            if function.__name__ == "buy_store":
                self.store_info.enabled = True
                # update the player info if it was initially there
                self.player_info.enabled = self.player_info.should_pop
                self.loan_window.enabled = self.loan_window.should_pop
                self.repay_window.enabled = self.repay_window.should_pop

                self.player_info.should_pop = False
                self.loan_window.should_pop = False
                self.repay_window.should_pop = False

        # create an empty text entity that later can be changed
        text_entity = Text("")

        confirm_window = WindowPanel(
            scale = CONFIRM_WIN_SIZE,
            color = WINDOW_COLOR,
            position = CONFIRM_WIN_POS,
            text = text_entity,
            lock = Vec3(1, 1, 1),
            content = [
                    Button("Yes", on_click = function),
                    Button("No", on_click = close_confirm_window)],
            enabled = False)

        confirm_window.text_entity.size *= 0.9

        # scale the button and its position
        for button in confirm_window.content:
            button.scale *= 0.8

        # offset the position
        confirm_window.content[0].position = (0, -1.8)
        confirm_window.content[1].position = (0, -2.8)

        self.full_screen_window.append(confirm_window)

        return confirm_window

    def create_menu_window(self):

        def close_menu():
            self.click.play()
            self.menu_window.enabled = False

        def open_howto(): 
            self.click.play()
            self.htp_info.enabled = True
            self.menu_window.enabled = False

        def toggle_mute():
            self.click.play()
            if self.a.playing:
                self.a.stop()
            else:
                self.a.play()

        def restart_game():
            pass

        self.menu_window  = WindowPanel(
            scale =  MENU_WIN_SIZE,
            color = WINDOW_COLOR,
            position = MENU_WIN_POS,
            text = "Menu",
            lock = Vec3(1, 1, 1),
            content =  [
                Button("How to Play", on_click = open_howto),
                #Button("Option 2", on_click = 0),
                Button("Toggle Music", on_click = toggle_mute),
                Button("Return", on_click = close_menu)],
            enabled = False)

        self.menu_window.text_entity.size *= 0.9

        self.full_screen_window.append(self.menu_window)

        for button in self.menu_window.content:
            button.scale *= 0.8

        index = -1.8
        # automatically indexes button spacing for any amount of buttons
        for content in self.menu_window.content:
            content.position = (0, index)
            index -= 1

        return self.menu_window

    def create_howto(self):
        self.htp_textcontentfiller = []
        self.htp_textcontent = Text()
        self.i = 0
        
        def show_howto(): 
            self.click.play()
            self.htp_info.enabled = True

        def close_howto(): 
            self.click.play()
            self.htp_info.enabled = False

        def next_instruct():
            self.click.play()
            if self.i > (len(self.htp_textcontentfiller) - 2): 
                self.i = 0
            else: 
                self.i = self.i + 1 
            update_instruct(self.i)

        def prev_instruct():
            self.click.play()
            if self.i < 0: 
                self.i = len(self.htp_textcontentfiller) - 2
                update_instruct(self.i)
            else: 
                self.i = self.i - 1 
                update_instruct(self.i)

        def update_instruct(count): 
            self.htp_textcontent.text = self.htp_textcontentfiller[count]

        def read_htp():     
            with open('resources/HOWTOPLAY.txt') as f:
                data = f.read()
                data_list = data.split('\n\n')
                self.htp_textcontentfiller = data_list
        
        read_htp()
        update_instruct(0)

        self.htp_info = WindowPanel(
            scale = HOW_TO_SIZE,
            color = WINDOW_COLOR,
            position = HOW_TO_POS,
            lock = Vec3(1, 1, 1),
            text = "How to Play",
            content= [
                self.htp_textcontent, 
                Button("Next <image:resources/loan.png>", on_click = next_instruct),
                Button("Prev", on_click = prev_instruct),
                Button("Exit <image:resources/exit.png>", on_click = close_howto)
            ],
            enabled = False) 

        self.full_screen_window.append(self.htp_info)

    """
    Create an info UI used by all city, show population, 
    """
    def create_city_info(self):
        def update_store_info():
            self.click.play()
            if self.selected_city == None: return
            self.log.close()

            self.selected_city.show_store_info()

        def close_city_info():
            self.click.play()
            self.city_info.enabled = False
            self.dropdown.enabled = False

        self.population_entity = Text(
            "Population: ")
        self.country_entity = Text("Country: ")
        self.wealth_entity = Text("Wealth: ")
        self.description_entity = Text("Description: ")
        
        self.city_info = WindowPanel(
            scale = CITY_INFO_SIZE,
            color = WINDOW_COLOR,
            position = CITY_INFO_POS,
            lock = Vec3(1, 1, 1),
            content = [
                    self.population_entity,
                    self.country_entity,
                    self.wealth_entity,
                    self.description_entity],
            enabled = False,
            should_pop = False)
        # size of the title
        self.city_info.text_entity.size *= 0.9
        # size of each text in content
        for entity in self.city_info.content:
            if type(entity) == Text:
                entity.size *= 0.7
        
        # offset the position of the text
        self.city_info.content[1].position = (-0.48, -2)
        self.city_info.content[2].position = (-0.48, -2.7)
        self.city_info.content[3].position = (-0.48, -3.4)
        
        # dropdown menu
        self.dropdown = DropdownMenu("Manage City <image:resources/city.png>", 
            buttons = (
                DropdownMenuButton("Manage Store <image:resources/managestore.png>", tooltip = Tooltip(
                    "Manage the stores within this city", scale = 0.7),
                    on_click = update_store_info), 

                DropdownMenuButton("City Graph <image:resources/graph.png>", tooltip = Tooltip("Generate graph with relevant sales information>", scale = 0.7)),
                DropdownMenuButton("Nuke <image:resources/nuke.png>", tooltip = Tooltip("Begin Nuclear Armageddon", scale = 0.7)),

                DropdownMenuButton("Exit <image:resources/exit.png>", tooltip = Tooltip("Close this menu", scale = 0.7), on_click = close_city_info)),
                position = DROPDOWN_POS,
                enabled = False)

        self.dropdown.scale *= 1.2
        self.dropdown.position = (self.dropdown.position[0], self.dropdown.position[1] - 0.07)
    
    """
    An interface showing specific store info selected by the user.
    """
    def create_store_info(self):
        # process the transaction
        def buy_store():
            self.click.play()
            # get the store object that has been selected
            store = self.selected_city.stores[self.selected_store]

            # if it is someone else's store
            if store.owner in self.AI_list:
                store.owner.addCash(store.cost)
                store.owner.markets.remove(store)

            # deduct player's cash
            self.player.removeCash(store.cost, "buy")
            store.owner = self.player
            self.player.markets.append(store)
            self.update_player_value()

            # update the store info after buying
            self.selected_city.show_store_info()
            self.buy_confirm_window.enabled = False

            # update the player info if it was initially there
            self.player_info.enabled = self.player_info.should_pop
            self.loan_window.enabled = self.loan_window.should_pop
            self.repay_window.enabled = self.repay_window.should_pop

            self.player_info.should_pop = False
            self.loan_window.should_pop = False
            self.repay_window.should_pop = False

            # reset all slider value
            for slider in self.slider_entities:
                slider.value = 0
            self.repay_slider.value = 0
            self.loan_slider.value = 0

        # function being called when product is produced
        def produce_product():
            self.click.play()
            store = self.selected_city.stores[self.selected_store]

            # don't do anything if the store is already producing or owned by other
            if store.produced \
                or store.owner != self.player \
                or self.total_cost_entity.cost > self.player.cash \
                or self.total_cost_entity.cost == 0:
                return
                
            store.produced = True

            total_cost = 0
            # increase the value of each product
            for i, slider in enumerate(self.slider_entities):
                if slider.enabled:
                    # adjust product quantity
                    store.products[i].quantity += slider.value
                    total_cost += slider.value * store.products[i].cost

            # deducted player's money
            self.player.removeCash(total_cost, "produce")
            store.profitability -= total_cost

            self.update_player_value()
            self.selected_city.show_store_info()

        # confirmation window before buying store
        def show_confirm_window():
            self.click.play()
            for window in self.full_screen_window:
                window.enabled = False
            # get the store object that has been selected
            store = self.selected_city.stores[self.selected_store]

            if store.owner == self.player: return

            self.player_info.should_pop = self.player_info.enabled
            self.loan_window.should_pop = self.loan_window.enabled
            self.repay_window.should_pop = self.repay_window.enabled

            self.player_info.enabled = False
            self.loan_window.enabled = False
            self.repay_window.enabled = False
            # enable the window only when the player has enough money
            if self.player.getCash() >= store.cost and store.owner != self.player:
                self.buy_confirm_window.enabled = True
                # disable the store info for a while
                self.store_info.enabled = False
            self.buy_confirm_window.text = f"Do you want to buy {store.name} with ${round(store.cost): ,}?"

        # reset the value of the slider
        def reset_value():
            for entity in self.slider_entities:
                entity.value = 0

        # change the total cost text entity upon change on sliders
        def change_total_cost():
            # reset the cost of the total_cost_entity
            # this value will be formatted and used to display the total cost
            self.total_cost_entity.cost = 0
            # get the list of the product objects of the selected store
            products = self.selected_city.stores[self.selected_store].products
            # combine the cost of each slider
            for i, slider in enumerate(self.slider_entities):
                # only calculate the enabled slider
                if slider.enabled:
                    # get the index of the slider and put them into the total cost
                    self.total_cost_entity.cost += slider.value * products[i].cost
            
            self.selected_city.change_button_color()
                
            self.total_cost_entity.text = f"Total Cost: ${round(self.total_cost_entity.cost): ,}"

        def close_store_window():
            self.click.play()
            self.store_info.enabled = False
            reset_value()
        
        def show_store_window():
            self.click.play()
            self.store_info.enabled = True

        def next_store():
            self.click.play()
            reset_value()
            self.selected_store = self.selected_store + 1 \
                if self.selected_store < len(self.selected_city.stores) - 1 \
                    else 0
            self.selected_city.show_store_info()

        def previous_store():
            self.click.play()
            reset_value()
            self.selected_store = self.selected_store - 1 \
                if self.selected_store != 0 \
                    else len(self.selected_city.stores) - 1
            self.selected_city.show_store_info()

        # create a confirm window and pass in buy_store() that will be called back when click "Yes"
        self.buy_confirm_window = self.create_confirm_window(buy_store)

        self.owner_entity = Text("Owner: None", scale = 0.75)
        self.cost_entity = Text("Selling Price: ", scale = 0.75)
        self.profitability_entity = Text("Profitability: $0", scale = 0.75)
        self.total_cost_entity = Text("Total Cost: $0", scale = 0.75, cost = 0)
        self.product_entities = []
        self.slider_entities = []
        # a pair of product name and slider
        for i in range(5):
            self.product_entities.append(Text("Product: ", scale = 0.65))
            self.slider_entities.append(Slider(on_value_changed = change_total_cost))
            self.slider_entities[i].knob.scale *= 0.9
            
        # initalize sliders
        for entity in self.slider_entities:
            entity.max = 100
            entity.step = 1

        self.store_info = WindowPanel(
            scale = STORE_INFO_SIZE,
            # scale = STORE_INFO_SIZE,
            color = WINDOW_COLOR,
            position = STORE_INFO_POS,
            lock = Vec3(1, 1, 1),
            content = [
                    self.owner_entity,
                    self.cost_entity,
                    self.profitability_entity,
                    self.product_entities[0], self.slider_entities[0],
                    self.product_entities[1], self.slider_entities[1],
                    self.product_entities[2], self.slider_entities[2],
                    self.product_entities[3], self.slider_entities[3],
                    self.product_entities[4], self.slider_entities[4],
                    self.total_cost_entity,
                    Button(text = "Buy Store",
                        action = "buy",
                        tooltip = Tooltip("", scale = 0.7),
                        on_click = show_confirm_window,
                        scale = (0.6, 0.1)),
                    Button(text = "Produce Product",
                        action = "produce",
                        tooltip = Tooltip("", scale = 0.7),
                        on_click = produce_product,
                        scale = (0.6, 0.1)),
                    Button(text = "Next  <image:resources/next.png>",
                        action = "next",
                        tooltip = Tooltip("Next stores", scale = 0.7),
                        on_click = next_store,
                        scale = (0.6, 0.1)),
                    Button(text = "Previous  <image:resources/prev.png>",
                        action = "previous",
                        tooltip = Tooltip("Previous stores", scale = 0.7),
                        on_click = previous_store,
                        scale = (0.7)),
                    Button(text = "Exit  <image:resources/exit.png>",
                        action = "exit",
                        tooltip = Tooltip("Exit this menu", scale = 0.7),
                        on_click = close_store_window,
                        scale = (0.6, 0.1))],
            enabled = False,
            should_pop = False)

        self.store_info.text_entity.size *= 0.9

    """
    A method that should be called every time when:
    1. Player's cash updates
    2. Player's income updates
    3. Player's expenses updates
    4. Number of stores owned updates
    """
    def update_player_value(self):
        # update the cash tab
        self.cash_tab.text_entity.text = f'Cash: ${round(self.player.getCash()): ,}'

        # update the info tab
        # get the player
        player = self.all_player[self.selected_player]
        # get the total number of store
        total_store = 0
        for city in w.global_cities:
            for store in city.stores:
                total_store += 1
        self.player_info.text_entity.text = f"Player Info [{self.selected_player + 1}/{len(self.all_player)}]"
        self.info_title_entity.text = f"  {player.name}: {str(self.turn.current_year)}, Quarter {self.turn.q_index + 1}"
        self.info_income_entity.text = f"    Income\n\n \
            Stores Owned: {str(len(player.markets))}/{(total_store)}\n\n \
            Total Income: ${round(player.total_income): ,}"
        self.info_expense_entity.text = f"    Expense\n\n \
            Store Costs: ${round(player.store_cost): ,}\n\n \
            Production Costs: ${round(player.production_cost): ,}\n\n \
            Total Expenses: ${round(player.total_expense): ,}"
        self.info_balance_entity.text = f"    Balance\n\n \
            Cash: ${round(player.getCash()): ,}\n\n \
            Loan Amount: ${round(player.loan): ,}\n\n \
            Maturity Date: {player.maturity_date} Quarter(s) Away"

        # loan window
        self.loan_slider.value = 0
        self.repay_slider.value = 0
        # calculat the amount of loan that a player can borrow
        amount = 0
        for store in self.player.markets:
            amount += (store.cost + store.profitability) / 1.5
        amount = amount if amount > 0 else 0
        
        self.loan_slider.max = round(amount - self.player.loan) if self.player.cash > 0 else 0
        # prevent the loan slider go into negative number
        self.loan_slider.max = self.loan_slider.max if self.loan_slider.max > 0 else 0
        self.repay_slider.max = round(self.player.loan) if self.player.cash > self.player.loan else self.player.cash
        self.repay_slider.max = self.repay_slider.max if self.player.cash > 0 else 0

        # for button in self.store_info.content[-1]:
    def create_player_info(self):
        def show_player_info():
            self.click.play()
            self.player_info.enabled = True
            self.log.close()
            self.update_player_value()
            for window in self.full_screen_window:
                window.enabled = False

        def close_player_info():
            self.click.play()
            self.player_info.enabled = False
            self.loan_window.enabled = False
            self.repay_window.enabled = False

        def show_loan_window():
            self.click.play()
            self.selected_player = 0
            self.update_player_value()
            self.loan_window.enabled = True

        def show_repay_window():
            self.click.play()
            self.selected_player = 0
            self.update_player_value()
            self.repay_window.enabled = True

        def next_player():
            self.click.play()
            self.selected_player = self.selected_player + 1 \
                if self.selected_player < len(self.all_player) - 1 \
                    else 0
            show_player_info()

        def previous_player():
            self.click.play()
            self.selected_player = self.selected_player - 1 \
                if self.selected_player != 0 \
                    else len(self.all_player) - 1
            show_player_info()

        self.cash_tab = Button(
            position = CASH_TAB_POS,
            scale = CASH_TAB_SIZE,
            text = f'Cash: ${round(self.player.getCash()): ,}',
            on_click = show_player_info, 
            tooltip = Tooltip("Click to show your current information", scale = 0.7))

        self.cash_tab.text_entity.scale *= 0.6

        # the entity that has to be with the alignment
        self.info_title_entity = Text("\n")
        self.info_income_entity = Text("\n\n\n")
        self.info_expense_entity = Text("\n\n\n\n")
        self.info_balance_entity = Text("\n\n\n\n\n")

        self.player_info = WindowPanel(
            scale = PLAYER_INFO_SIZE,
            color = WINDOW_COLOR,
            position = PLAYER_INFO_POS,
            lock = Vec3(1, 1, 1),
            text = "                 ",
            content= [
                self.info_title_entity,
                self.info_income_entity,
                self.info_expense_entity,
                self.info_balance_entity,
                Button(
                    "Take Loan <image:resources/loan.png>",
                    tooltip = Tooltip("Borrow money", scale = 0.7),
                    on_click = show_loan_window,
                    scale = (0.6, 0.2)),
                Button(
                    "Repay Loan <image:resources/money.png>",
                    tooltip = Tooltip("Repay borrowed money before the loan sharks come get you", scale = 0.7),
                    on_click = show_repay_window,
                    scale = (0.6, 0.2)),  
                Button(
                    "Next <image:resources/next.png>",
                    on_click = next_player,
                    scale = (0.6, 0.2)),
                Button(
                    "Previous <image:resources/prev.png>",
                    on_click = previous_player,
                    scale = (0.6, 0.2)),
                Button(
                    "Exit <image:resources/exit.png>",
                    on_click = close_player_info,
                    scale = (0.6, 0.2))],
            enabled = False,
            should_pop = False)

        self.player_info.text_entity.size *= 0.9
        self.player_info.content[0].size *= 1.1

        for element in self.player_info.content:
            element.position = (element.position[0], element.position[1] - 0.3)
            if type(element) == Text:
                element.scale *= 0.7

        def close_loan_window():
            self.click.play()
            self.loan_window.enabled = False

        def get_loan():
            self.click.play()
            self.player.addCash(self.loan_slider.value, "loan")
            self.update_player_value()

        self.loan_slider = Slider(scale = 1.2)
        self.loan_slider.min = 0
        self.loan_slider.max = 0
        self.loan_slider.step = 1000

        self.loan_window = WindowPanel(
            scale = LOAN_PANEL_SIZE,
            color = WINDOW_COLOR,
            position = LOAN_PANEL_POS,
            lock = Vec3(1, 1, 1),
            text = "Loan Amount",
            content= [
                self.loan_slider,
                Button("Accept <image:resources/accept.png>", on_click = get_loan),
                Button("Exit <image:resources/exit.png>", on_click = close_loan_window)
            ],
            enabled = False,
            should_pop = False)

        self.loan_window.text_entity.size *= 0.7

        index = -2
        for content in self.loan_window.content:
            content.scale *= 0.8
            if type(content) == Slider:
                content.position = (-0.37, index)
                index -= 0.25
            else:
                index -= 1
                content.position = (0, index)

        def close_repay_window():
            self.click.play()
            self.repay_window.enabled = False

        def pay_loan():
            self.click.play()
            self.click.play()
            self.player.removeCash(self.repay_slider.value, "loan")
            self.update_player_value()

        self.repay_slider = Slider()
        self.repay_slider.min = 0
        self.repay_slider.max = 0
        self.repay_slider.step = 1000

        self.repay_window = WindowPanel(
            scale = LOAN_PANEL_SIZE,
            color = WINDOW_COLOR,
            position = REPAY_PANEL_POS,
            lock = Vec3(1, 1, 1),
            text = "Repay Loan Amount",
            content= [
                self.repay_slider,
                Button("Accept <image:resources/accept.png>", on_click = pay_loan),
                Button("Exit <image:resources/exit.png>", on_click = close_repay_window)
            ],
            enabled = False,
            should_pop = False)

        self.repay_window.text_entity.size *= 0.7

        index = -2
        for content in self.repay_window.content:
            content.scale *= 0.8
            if type(content) == Slider:
                content.position = (-0.37, index)
                index -= 0.25
            else:
                index -= 1
                content.position = (0, index)
       

    # updates the current turn text to show the next quarter and year if applicable
    def update_turn(self):
        self.current_turn.text = "Current Turn: \n    " + str(self.turn.current_year) + ", " + QUARTERS[self.turn.q_index]


    """
    Create different kinds of buttons in the world map.
    """
    def create_button(self):
        def return_to_map():
            self.click.play()
            for window in self.full_screen_window:
                window.enabled = False
            camera.animate_x(CAMERA_POS[0], duration = 1)
            camera.animate_y(CAMERA_POS[1], duration = 1)
            camera.animate_z(CAMERA_POS[2], duration = 1)
            # disable the window panel
            self.city_info.enabled = False
            self.store_info.enabled = False
            self.dropdown.enabled = False
            self.player_info.enabled = False
            self.loan_window.enabled = False
            self.repay_window.enabled = False
            self.selected_city = None

        def proceed_next_turn():
            self.click.play()
            # return to the world map if player decide to proceed
            return_to_map()
            self.turn.nextTurn()
            self.next_turn_confirm_window.enabled = False
            self.update_turn()
        
        # show the confirmation window while closing the store window
        def show_confirm_window():
            self.click.play()
            for window in self.full_screen_window:
                window.enabled = False
            self.next_turn_confirm_window.enabled = True
            self.next_turn_confirm_window.text = "Do you want to proceed to the next turn?"
            self.store_info.enabled = False
            self.city_info.enabled = False
            self.player_info.enabled = False
            self.loan_window.enabled = False
            self.repay_window.enabled = False
            self.dropdown.enabled = False
        
        # create the confirmation window
        self.next_turn_confirm_window = self.create_confirm_window(proceed_next_turn)
        self.full_screen_window.append(self.next_turn_confirm_window)

        def show_menu_window():
            self.click.play()
            for window in self.full_screen_window:
                window.enabled = False
            self.store_info.enabled = False
            self.city_info.enabled = False
            self.player_info.enabled = False
            self.loan_window.enabled = False
            self.repay_window.enabled = False
            self.dropdown.enabled = False

            # enable the menu window
            self.menu_window.enabled = True

        self.menu_window = self.create_menu_window()

        # create "back to world" button
        back_to_world = Button(
            position = BACK_TO_WORLD_POS,
            scale = BACK_TO_WORLD_SIZE,
            text = "Back to World",
            on_click = return_to_map, 
            tooltip = Tooltip("Close all menus and return to map", scale = 0.7), 
            icon='resources/return.png', text_origin=(0,0.27))
        # scale the text of the button
        back_to_world.text_entity.scale *= 0.7
        back_to_world.icon.scale_x = 0.39
        back_to_world.icon.scale_y = 0.535
        back_to_world.icon.y = -0.2

        next_turn = Button(
            position = NEXT_TURN_POS,
            scale = NEXT_TURN_SIZE,
            text = "Next Turn",
            on_click = show_confirm_window, 
            tooltip = Tooltip("Speed up time to the next quarter", scale = 0.7), 
            icon='resources/nextturnicon.png', text_origin=(0,0.27))
        # scale the text of the button
        next_turn.text_entity.scale *= 0.7
        next_turn.icon.scale_x = 0.15
        next_turn.icon.scale_y = 0.243
        next_turn.icon.y = -0.2

        show_menu = Button(
            position = MENU_BUTTON_POS,
            scale = MENU_BUTTON_SIZE,
            text = "Menu",
            on_click = show_menu_window,
            tooltip = Tooltip("Open the menu to see options", scale = 0.7))
        # scale the text of the button
        show_menu.text_entity.scale *= 0.7

