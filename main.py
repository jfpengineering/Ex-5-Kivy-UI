import os

#os.environ['DISPLAY'] = ":0.0"
#os.environ['KIVY_WINDOW'] = 'egl_rpi'

from kivy.app import App
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix import label
from kivy.uix.screenmanager import ScreenManager, Screen

from pidev.MixPanel import MixPanel
from pidev.kivy.PassCodeScreen import PassCodeScreen
from pidev.kivy.PauseScreen import PauseScreen
from pidev.kivy import DPEAButton
from pidev.kivy import ImageButton
from pidev.kivy.selfupdatinglabel import SelfUpdatingLabel
from kivy.uix.slider import Slider
from kivy.uix.widget import Widget
from kivy.animation import Animation

from datetime import datetime

time = datetime

MIXPANEL_TOKEN = "x"
MIXPANEL = MixPanel("Project Name", MIXPANEL_TOKEN)

SCREEN_MANAGER = ScreenManager()
MAIN_SCREEN_NAME = 'main'
ADMIN_SCREEN_NAME = 'admin'
OTHER_SCREEN_NAME = "other_screen"
ANOTHER_SCREEN_NAME = "another_screen"


class ProjectNameGUI(App):
    """
    Class to handle running the GUI Application
    """

    def build(self):
        """
        Build the application
        :return: Kivy Screen Manager instance
        """
        return SCREEN_MANAGER


Window.clearcolor = (1, 1, 1, 1)  # White


class MainScreen(Screen):
    """
    Class to handle the main screen and its associated touch events
    """
    toggle_btn = ObjectProperty(None)
    counter_btn = ObjectProperty(None)
    counter_label = ObjectProperty(None)
    motor_label = ObjectProperty(None)
    motor_btn = ObjectProperty(None)
    slider = ObjectProperty(None)
    slider_label = ObjectProperty(None)

    def pressed(self):
        """
        Function called on button touch event for button with id: testButton
        :return: None
        """
        print("Callback from MainScreen.pressed()")

    def admin_action(self):
        """
        Hidden admin button touch event. Transitions to passCodeScreen.
        This method is called from pidev/kivy/PassCodeScreen.kv
        :return: None
        """
        SCREEN_MANAGER.current = 'passCode'

    def toggle_text(self):
        if self.toggle_btn.text == "Toggle":
            self.toggle_btn.text = ""
        else:
            self.toggle_btn.text = "Toggle"

    def counter(self):
        i = int(self.counter_label.text)
        value = int(i+1)
        self.counter_label.text = str(value)

    def motor_toggle(self):
        if self.motor_label.text == "Motor OFF":
            self.motor_label.text = "Motor ON"
        else:
            self.motor_label.text = "Motor OFF"

    def slider_press(self):
        value = int(self.slider.value)
        self.slider_label.text = str(value)+" / 100"
        print(value)

    @staticmethod
    def other_screen_go_to():
        SCREEN_MANAGER.current = OTHER_SCREEN_NAME

class OtherScreen(Screen):

    animated_btn = ObjectProperty(None)

    def __init__(self, **kwargs):
        Builder.load_file('OtherScreen.kv')
        super(OtherScreen, self).__init__(**kwargs)

    @staticmethod
    def transition_back():
        SCREEN_MANAGER.current = MAIN_SCREEN_NAME

    def animate_it(self, widget, *kwargs):

        animate = Animation(size_hint = (.5, .25))
        animate += Animation(size_hint = (.25, .25))
        animate += Animation(pos_hint = {"center_x": .8})
        animate += Animation(pos_hint={"center_y": .8})
        animate += Animation(pos_hint={"center_x": .2})
        animate += Animation(pos_hint={"center_y": .25})
        animate += Animation(pos_hint={"center_x": .5})

        animate.start(widget)
        animate.bind(on_complete = self.change_bkgrnd)

    def change_bkgrnd(self, *args):

        self.animated_btn.background_normal="thumbs_up.jpg"
        SCREEN_MANAGER.current = ANOTHER_SCREEN_NAME


class AnotherScreen(Screen):

    animated_btn2 = ObjectProperty(None)

    def __init__(self, **kwargs):
        Builder.load_file('AnotherScreen.kv')
        super(AnotherScreen, self).__init__(**kwargs)

    def animate_it2(self, widget, *kwargs):

        animate = Animation(size_hint = (.5, .25))
        animate += Animation(size_hint = (.25, .25))
        animate += Animation(pos_hint = {"center_x": .8})
        animate += Animation(pos_hint={"center_y": .8})
        animate += Animation(pos_hint={"center_x": .2})
        animate += Animation(pos_hint={"center_y": .25})
        animate += Animation(pos_hint={"center_x": .5})

        animate.start(widget)
        animate.bind(on_complete = self.move_back)

    def move_back(self, *args):
        self.animated_btn2.background_normal = "coder.png"
        SCREEN_MANAGER.current = MAIN_SCREEN_NAME

class AdminScreen(Screen):
    """
    Class to handle the AdminScreen and its functionality
    """

    def __init__(self, **kwargs):
        """
        Load the AdminScreen.kv file. Set the necessary names of the screens for the PassCodeScreen to transition to.
        Lastly super Screen's __init__
        :param kwargs: Normal kivy.uix.screenmanager.Screen attributes
        """
        Builder.load_file('AdminScreen.kv')

        PassCodeScreen.set_admin_events_screen(ADMIN_SCREEN_NAME)  # Specify screen name to transition to after correct password
        PassCodeScreen.set_transition_back_screen(MAIN_SCREEN_NAME)  # set screen name to transition to if "Back to Game is pressed"

        super(AdminScreen, self).__init__(**kwargs)

    @staticmethod
    def transition_back():
        """
        Transition back to the main screen
        :return:
        """
        SCREEN_MANAGER.current = MAIN_SCREEN_NAME

    @staticmethod
    def shutdown():
        """
        Shutdown the system. This should free all steppers and do any cleanup necessary
        :return: None
        """
        os.system("sudo shutdown now")

    @staticmethod
    def exit_program():
        """
        Quit the program. This should free all steppers and do any cleanup necessary
        :return: None
        """
        quit()


"""
Widget additions
"""

Builder.load_file('main.kv')
SCREEN_MANAGER.add_widget(MainScreen(name=MAIN_SCREEN_NAME))
SCREEN_MANAGER.add_widget(OtherScreen(name=OTHER_SCREEN_NAME))
SCREEN_MANAGER.add_widget(AnotherScreen(name=ANOTHER_SCREEN_NAME))
SCREEN_MANAGER.add_widget(PassCodeScreen(name='passCode'))
SCREEN_MANAGER.add_widget(PauseScreen(name='pauseScene'))
SCREEN_MANAGER.add_widget(AdminScreen(name=ADMIN_SCREEN_NAME))

"""
MixPanel
"""


def send_event(event_name):
    """
    Send an event to MixPanel without properties
    :param event_name: Name of the event
    :return: None
    """
    global MIXPANEL

    MIXPANEL.set_event_name(event_name)
    MIXPANEL.send_event()


if __name__ == "__main__":
    # send_event("Project Initialized")
    # Window.fullscreen = 'auto'
    ProjectNameGUI().run()
