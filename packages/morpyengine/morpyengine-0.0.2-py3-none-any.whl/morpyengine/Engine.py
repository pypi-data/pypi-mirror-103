import sdl2
import sdl2.ext
from morpyengine.Constants import *


class Engine:
    def __init__(self, window_title="My Engine", width=500, height=500):
        """
        :param window_title:
        :param width:
        :param height:
        """
        self.window_title = window_title
        self.width = width
        self.height = height
        self.loop_state = LOOP_STATE_STOPPED
        self.window = None

    def setup(self):
        """
        Setup the Engine to build an app around it
        :return:
        """
        pass

    def update(self):
        """
        Updating the Engine at each loop
        :return:
        """
        pass

    def set_loop_state(self, state):
        """
        Setting the Loop State
        :param state:
        :return:
        """
        if state == LOOP_STATE_RUNNING or state == LOOP_STATE_STOPPED or state == LOOP_STATE_PAUSED:
            self.loop_state = state

    def handle_events(self, events):
        """
        Handling the SDL events
        :param events:
        :return:
        """
        for event in events:
            if event.type == sdl2.SDL_QUIT:
                self.set_loop_state(LOOP_STATE_STOPPED)
                break

    def get_surface(self):
        """
        Get the main Window surface
        :return:
        """
        return self.window.get_surface()

    def run(self):
        """
        Start application and running the update loop
        :return integer:
        """
        # Initialize SDL2 Lib
        sdl2.ext.init()
        # Create and show the main Window
        self.window = sdl2.ext.Window(self.window_title, size=(self.width, self.height))
        self.window.show()
        # Setup the application
        self.setup()
        # Set loop state on Running
        self.set_loop_state(LOOP_STATE_RUNNING)
        # Running the update Loop
        while self.loop_state != LOOP_STATE_STOPPED:
            self.handle_events(sdl2.ext.get_events())
            self.update()
            self.window.refresh()

        # Exiting the SDL2
        sdl2.ext.quit()

        return 0
