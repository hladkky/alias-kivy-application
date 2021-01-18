import time
from datetime import datetime

from kivy.lang.builder import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, WipeTransition

from kivymd.app import MDApp

from screens.screens import MenuScreen


class AliasApp(MDApp):    
    def build(self):
        screen = Builder.load_file('main.kv')
        sm = ScreenManager(transition=WipeTransition())

        return screen
    
    def on_pause(self):
        return True
        
    def on_stop(self):
        pass
        # with open('logs/log.log', 'a') as f:
        #     f.write(f'stop at {datetime.now()}\n')
        
    def on_start(self):
        pass
        # with open('logs/log.log', 'a') as f:
        #     f.write(f'start at {datetime.now()}\n')


app = AliasApp()
if __name__ == '__main__':
    app.run()
