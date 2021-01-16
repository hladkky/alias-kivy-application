import time
from datetime import datetime

from kivy.lang.builder import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, CardTransition
from kivy.graphics import Color, Triangle, RoundedRectangle, Line, Rectangle, BorderImage
from kivy.core.window import Window
from kivy.properties import NumericProperty, StringProperty, ColorProperty
from kivy.config import Config
from kivy.clock import Clock
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.widget import Widget
from kivy.animation import Animation

from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.label import MDLabel, MDIcon
from kivymd.uix.card import MDCard
from kivymd.uix.button import MDFlatButton, MDIconButton, MDRectangleFlatButton, MDRoundFlatButton
from kivymd.uix.list import OneLineListItem
from kivymd.uix.behaviors import (
    RectangularRippleBehavior,
    BackgroundColorBehavior,
    RectangularElevationBehavior,
    RectangularRippleBehavior
)

from screens.screens import MenuScreen

from widgets.widgets import GameCard


class AliasApp(MDApp):    
    def build(self):
        screen = Builder.load_file('main.kv')
        sm = ScreenManager(transition=CardTransition())

        return screen
    
    def on_pause(self):
        with open('logs/log.log', 'a') as f:
            f.write(f'pause at {datetime.now()}\n')
        
    def on_stop(self):
        with open('logs/log.log', 'a') as f:
            f.write(f'stop at {datetime.now()}\n')
        
    def on_start(self):
        with open('logs/log.log', 'a') as f:
            f.write(f'start at {datetime.now()}\n')


if __name__ == '__main__':
    Window.size = (1080/3, 1920/3)
    AliasApp().run()
