'''
Alias application.

Alias is a board game, where the objective of the players is to explain words to each other.
Learn more here: https://en.wikipedia.org/wiki/Alias_(board_game)

This application is created to simulate board game to have fun with friends.
The main specification is that this game is totally ukrainian.

Author : Hladkko © Yaroslav Hladkyi
'''

import json
from random import shuffle

from kivy.utils import platform
from kivy.lang.builder import Builder
from kivy.loader import Loader
from kivy.core.window import Window
from kivy.config import Config
from kivy.storage.jsonstore import JsonStore
from kivy.uix.screenmanager import ScreenManagerException
from kivy.properties import BooleanProperty
from kivy.cache import Cache

from kivymd.app import MDApp

from widgets.widgets import TextButton, Dialog


class AliasApp(MDApp):
    '''
    Alias application class

    ...

    Attributes
    ----------
    store : JsonStore
        Instance of application store
    sm : ScreenManager
        Instance of screen manager
    active_game : BooleanProperty
        Indicator if active game exists
    dict_idxs : dict
        dict with dictionaries names and indexes of current word in them

    Methods
    -------
    create_main_game(round_duration, selected_dictionary, teams, penalty,
                     last_word, points_to_win):
        create instance of MainGameScreen and swith to it

    to_game_config():
        switch to the team config screen

    load_main_game():
        load active game configuration from the `store` and switch to it

    save_current_game():
        save configuration of active game to the `store` and toggle `active_game` indicator

    delete_current_game():
        remove configuration of active game from the `store` and toggle `active_game` indicator

    on_start():
        kivy method

    on_pause():
        kivy method

    on_stop():
        kivy method

    build():
        kivy method
    '''
    store = JsonStore('app_store.json')
    sm = None
    active_game = BooleanProperty(False)
    dict_idxs = None

    def create_main_game(self, round_duration, selected_dictionary, teams,
                         penalty, last_word, points_to_win):
        '''
        Create main game of the application

        Parameters
        ----------
        round_duration : int
            duration of one round in the game
        selected_dictionary : str
            selected dictionary for game words
        teams : list
            list of team names
        penalty : bool
            penalty for skipped word
        last_word : str
            word in the round after time is expired
        points_to_win : int
            amount of points to win the game
        '''
        main_game = self.sm.get_screen('main_game')
        main_game.load_configuration(
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
        self.sm.current = 'main_game'
        self.active_game = True

    def to_game_config(self):
        '''
        Route to team config screen with dialog box if `active_game` is True
        '''
        def drop_game_and_create_new():
            self.delete_current_game()
            dialog.dismiss()
            self.to_game_config()

        if self.active_game:
            dialog = Dialog(
                title='Створити нову гру?',
                text='Дані про поточну гру буде втрачено.',
                buttons=[
                    TextButton(
                        text="[size=16sp]Назад[size=16sp]",
                        on_release=lambda _: dialog.dismiss()
                    ),
                    TextButton(
                        text="[size=16sp]Так[size=16sp]",
                        on_release=lambda _: drop_game_and_create_new()
                    )
                ],
            )
            dialog.open()
        else:
            self.sm.current = "team_config"

    def load_main_game(self):
        '''
        Load main game of the application
        '''
        active_game_cofig = self.store.get('active_game')
        main_game = self.sm.get_screen('main_game')
        main_game.load_configuration(**active_game_cofig)
        self.sm.current = 'main_game'

    def save_current_game(self):
        '''
        Save main game of the application
        '''
        main_game = self.sm.get_screen('main_game')
        self.save_dict_idx(main_game.dicitionary_name, main_game.dict_idx)
        self.store.put('active_game', **{
            key: getattr(main_game, key)
            for key in (
                'round_duration',
                'dictionary_name',
                'dict_idx',
                'teams',
                'penalty',
                'last_word',
                'points_to_win',
                'score',
                'current_round',
                'current_turn',
            )
        })

    def save_dict_idx(self, current_dict, current_dict_idx):
        dict_idxs = self.store.get('dicts_idxs')
        dict_idxs[current_dict] = current_dict_idx
        self.store.put('dicts_idxs', **dict_idxs)

    def delete_current_game(self):
        '''
        Delete main game of the application
        '''
        try:
            self.store.delete('active_game')
        except KeyError:
            pass
        self.active_game = False

    def on_start(self):
        try:
            self.store.get('active_game')
            self.active_game = True
        except KeyError:
            pass

        try:
            self.dict_idxs = self.store.get('dicts_idxs')
        except KeyError:
            with open('./constants/words.json', encoding='utf-8') as f:
                dicts = json.load(f)
                idxs = {}
                for dictionary_name, words in dicts.items():
                    shuffle(words)
                    dicts[dictionary_name] = words
                    idxs[dictionary_name] = 0
            with open('./constants/words.json', 'w', encoding='utf-8') as f:
                json.dump(dicts, f)
            self.store.put('dicts_idxs', **idxs)

        self.sm.screens[0].continue_button_active = bool(self.active_game)

    def on_pause(self):
        if self.active_game:
            self.save_current_game()
        return True

    def on_stop(self):
        self.on_pause()

    def build(self):
        self.theme_cls.theme_style = 'Dark'
        self.sm = Builder.load_file('main.kv')

        # Cache.append(
        #     'images',
        #     'main_background'
        # )
        # FitImage(source="assets/imgs/back.png")

        return self.sm


Cache.register('images', limit=10)

Loader.num_workers = 4  # for smoother user experience
Loader.loading_image = './assets/imgs/main.png'  # loading image for async images

# To avoid app shutdown by pressing 'return' on phone
Config.set('kivy', 'exit_on_escape', '0')

if platform == 'win':  # if running on desktop
    Window.size = (330, 600)

if __name__ == '__main__':
    AliasApp().run()
