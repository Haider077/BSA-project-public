from ursina import *                    # Import the ursina engine
from settings import *
import textwrap


#class event 
#will use a list to store a log of up to 100 items, and only 100 items 
class Logger():
    

    def __init__(self, world_interface):     
        self.log_remover = 100 
        self.archivelogs = []
        self.logString = ""
        self.displayIndex = 0
        self.turn = ""
        self.world_ui = world_interface
        self.wordwrap = 80

    def handleLogTurn(self,Turn):
        self.logString = ""
        self.turn = Turn

    def create_log_string(self):
        for i in self.archivelogs :
            self.logString += self.turn + ": Q" + i + "\n"

    def log (self, message): 
        # self.message = f"{message} + \n" 
        # self.archivelogs.append(message)
        # self.create_log_string()
        wrapper = textwrap.TextWrapper(width = self.wordwrap)
        self.logString += self.turn + " : " +  wrapper.fill(text = message) + "\n"
        
    def return_log(self): 
        return self.archivelogs

    def write_log_file(self): 
        f = open("logfile.txt", "a")
        for i in range(len(self.archivelogs)): 
            f.write(self.archivelogs[i])
        f.close()
    
    def erase_log_history(self): 
        if len(self.archivelogs == 100): 
            self.write_log_file() 
            del self.archivelogs[100]

    def update_log(self):
        self.log_content.text = self.logString
        #self.log_content.max_lines = len(self.logString.split("\n")) - int(len(self.logString.split("\n"))/20)
        self.log_content.scroll = 0

    def toggleVis(self):
        self.log_content.enabled =  not self.log_content.enabled
        self.logText.enabled = not self.logText.enabled

    def open(self):
        self.log_content.enabled =  True
        self.logText.enabled = True

    def close(self):
        self.log_content.enabled =  False
        self.logText.enabled = False
            
    def log_ui(self):
        self.click = Audio("resources/confirmation_001.ogg", pitch=1, loop=False, autoplay=False)
        def toggleVisLocal():
            self.click.play()
            # if the window has not opened, then open
            if not self.log_content.enabled:
                self.world_ui.store_info.should_pop = self.world_ui.store_info.enabled
                self.world_ui.store_info.enabled = False
                self.world_ui.player_info.should_pop = self.world_ui.player_info.enabled
                self.world_ui.player_info.enabled = False
                self.world_ui.loan_window.should_pop = self.world_ui.loan_window.enabled
                self.world_ui.loan_window.enabled = False
                self.world_ui.repay_window.should_pop = self.world_ui.repay_window.enabled
                self.world_ui.repay_window.enabled = False
            # if the window is opened, then close
            else:
                should_open = True
                for window in self.world_ui.full_screen_window:
                    if window.enabled:
                        should_open = False
                
                if should_open:
                    self.world_ui.store_info.enabled = self.world_ui.store_info.should_pop
                    self.world_ui.store_info.should_pop = True
                    self.world_ui.player_info.enabled = self.world_ui.player_info.should_pop
                    self.world_ui.player_info.should_pop = True
                    self.world_ui.loan_window.enabled = self.world_ui.loan_window.should_pop
                    self.world_ui.loan_window.should_pop = True
                    self.world_ui.repay_window.enabled = self.world_ui.repay_window.should_pop
                    self.world_ui.repay_window.should_pop = True
                    
            self.log_content.enabled =  not self.log_content.enabled
            self.logText.enabled = not self.logText.enabled

        self.b = Button(
            text = "Log",
            position = (-.8,-0.35),
            scale=MENU_BUTTON_SIZE,
            on_click=toggleVisLocal)
        self.b.text_entity.scale *= 0.7

        self.logText = Text(
            text = "Log",
            position = (-.45,-0.25),
            scale = 1,
            background_color=color.black66,
            enabled = False)
        self.log_content = TextField(
            text = self.logString,
            max_lines = 30,
            color=color.black,
            position = (-.45,-0.3),
            scale=(0.6,.6),
            register_mouse_input = False,
            word_wrap = 20,
            enabled  = False,
            should_pop = False)
        self.log_content.bg.scale_x = 1.6
        self.log_content.bg.scale_y = 0.5
        self.log_content.cursor.enabled = False
        self.log_content.bg.color = color.black66
        self.log_content.bg.origin = (-0.44,0.29)
        self.log_content.text_entity.color = color.azure
