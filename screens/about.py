'''
About game screen.
'''

from screens.config import ConfigScreen


class AboutScreen(ConfigScreen):
    '''
    Screen that contains information about the game
    '''
    def on_kv_post(self, _):
        '''
        Kivy method overriden to show text and bind function to the screen button
        '''
        def back_to_menu():
            self.manager.current = 'menu'

        self.ids.screen_bottom_button.ids.button.bind(on_press=lambda _: back_to_menu())

        with open('constants/about_game.txt', encoding='utf-8') as f:
            self.ids.text_about.text = f.read()
