from kivy.app import App
from kivy.properties import StringProperty

from screens.config import ConfigScreen


class WinnerScreen(ConfigScreen):
    title = "ПЕРЕМОЖЦІ"
    button_text = "Завершити гру"
    winner_team = StringProperty()

    def __init__(self, winner_team, **kwargs):
        super().__init__(**kwargs)
        self.winner_team = winner_team

    def on_kv_post(self, _):
        self.ids.screen_bottom_button.ids.button.bind(
            on_press=self.end_main_game
        )

    def end_main_game(self, _):
        App.get_running_app().delete_current_game()
        self.manager.switch_to("menu")
