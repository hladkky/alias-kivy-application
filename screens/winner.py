'''
Winner screen.
'''

from kivy.app import App
from kivy.properties import StringProperty

from screens.config import ConfigScreen


class WinnerScreen(ConfigScreen):
    '''
    Screen that appear when one of team has reached the winning points and show it

    Attributes
    ----------
    winner_team : StringProperty
        team that won the game

    Methods
    -------
    on_kv_post(_):
        kivy method

    end_main_game(_):
        end current game
    '''
    winner_team = StringProperty()

    def __init__(self, winner_team, **kwargs):
        super().__init__(**kwargs)
        self.winner_team = winner_team

    def on_kv_post(self, _):
        '''
        Kivy method overriden to bind the function to the screen button
        '''
        self.ids.screen_bottom_button.ids.button.bind(
            on_press=self.end_main_game
        )

    def end_main_game(self, _):
        '''
        End current game and go to menu screen
        '''
        App.get_running_app().delete_current_game()
        menu_screen = self.manager.get_screen("menu")
        self.manager.switch_to(menu_screen)
