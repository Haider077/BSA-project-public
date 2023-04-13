from turtle import position
from ursina import *                    # Import the ursina engine
import world
from interface import WorldInterface
import utils
import simulation as s
from settings import *

class App(Ursina):
    def __init__(self):
        self.app = Ursina()                          # Initialise your Ursina app
        window.title = 'BSA simulation project'
        window.borderless = False
        window.fullscreen = False
        window.fps_counter.enabled = True
        # add this to have editor version of camera
        # EditorCamera()
        self.init_camera()
        #self.a = Audio('resources/superbased.mp3', pitch=1, loop=True, autoplay=True)
    def run(self):
        world.createWorld()
        world_interface = WorldInterface()
        world.create_city(world_interface)
        world_interface.log.log_ui()
        self.app.run()
        #self.a.play()

    def init_camera(self):
        camera.position = CAMERA_POS
        camera.rotation_x = CAMERA_ROTATION_X
        window.size = RESOLUTION

# this update method will be called every loop
def update():
    pass
    
if __name__ == '__main__':
    app = App()
    app.run()