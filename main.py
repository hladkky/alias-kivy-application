import json
from random import shuffle

from kivy.utils import platform
from kivy.lang.builder import Builder
from kivy.loader import Loader
from kivy.core.window import Window
from kivy.config import Config
from kivy.storage.jsonstore import JsonStore
from kivy.uix.screenmanager import ScreenManagerException

from kivymd.app import MDApp

from screens.main_game import MainGameScreen


class AliasApp(MDApp):
    store = JsonStore('app_store.json')
    sm = None
    active_game = False
    dict_idxs = None

    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.sm = Builder.load_file("main.kv")

        print(self.sm.screens)
        return self.sm

    def create_main_game(self, round_duration, selected_dictionary, teams,
                         penalty, last_word, points_to_win):
        self.sm.add_widget(
            MainGameScreen(
                round_duration=round_duration,
                dictionary_name=selected_dictionary,
                dict_idx=self.store.get('dicts_idxs')[selected_dictionary],
                teams=teams,
                penalty=penalty,
                last_word=last_word,
                points_to_win=points_to_win,
                score=[0 for _ in teams],
                current_round=1,
                current_turn=0
            )
        )
        self.sm.current = "main_game"
        # self.store.put('active_game', round_duration=round_duration,
        #                               selected_dictionary=selected_dictionary,
        #                               teams=teams)
        # self.is_active_game = True

    def delete_current_game(self):
        pass

    def on_start(self):
        try:
            self.store.get('active_game')
            self.active_game = True
        except KeyError:
            pass

        try:
            self.dict_idxs = self.store.get('dicts_idxs')
        except KeyError:
            with open("./constants/words.json", encoding="utf-8") as f:
                dicts = json.load(f)
                idxs = {}
                for d, words in dicts.items():
                    shuffle(words)
                    dicts[d] = words
                    idxs[d] = 0
            with open("./constants/words.json", "w", encoding="utf-8") as f:
                json.dump(dicts, f)
            self.store.put('dicts_idxs', **idxs)

        self.sm.screens[0].continue_button_active = bool(self.active_game)
        print('start')

    def on_pause(self):
        print('pause')
        return True

    def on_stop(self):
        print('stop')
        try:
            main_game = self.sm.get_screen("main_game")
            print(main_game.__dict__)
        except ScreenManagerException:
            print("no main game")
        # self.store.delete('active_game')


Loader.num_workers = 4
Loader.loading_image = './assets/imgs/main.png'

Config.set('kivy', 'exit_on_escape', '0')  # To avoid app shutdown by pressing 'return' on phone

print(platform)
if platform == 'win':
    Window.size = (330, 600)

if __name__ == "__main__":
    AliasApp().run()
