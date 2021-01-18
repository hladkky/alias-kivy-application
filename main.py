import time
from datetime import datetime

from kivy.lang.builder import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window

from kivymd.app import MDApp

from screens.screens import MenuScreen


class AliasApp(MDApp):
    def build(self):
        sm = Builder.load_file("main.kv")
        return sm
    
    def on_pause(self):
        return True
        
    # def on_stop(self):
    #     pass
        
    # def on_start(self):
    #     pass


Window.size = (300, 600)
app = AliasApp()
if __name__ == "__main__":
    app.run()
