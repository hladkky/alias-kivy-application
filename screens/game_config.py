'''
Game configuration screen.
'''

import json

from kivy.app import App
from kivy.properties import NumericProperty, StringProperty
from kivy.metrics import dp
from kivy.animation import Animation

from screens.config import ConfigScreen

from widgets.widgets import (
    DictionaryCarouselItem
)


class GameConfigScreen(ConfigScreen):
    '''
    Screen where game options are choosen and new main game is created.

    Attributes
    ----------
    dictionaries : list[dict]
        list of available dictionaries with information about each one

    round_duration : int
        round duration in seconds

    selected_dictionary : str
        name of the selected dictionary

    selected_dictionary_index : int
        index of the selected dictionary

    Methods
    -------
    on_kv_post(_):
        kivy method

    change_round_duration(delta):
        change game round duration

    select_dictionary(carousel):
        select game dictionary

    show_dictionaries():
        display all the dictionaries available in the game

    fill_dictionaries():
        load all dictionaries shown on the screen

    toggle_carousel_buttons():
        toggle carousel button when the carousel appear or disappear

    hide_dictionaries():
        remove from the screen all the dictionaries available in the game

    start_main_game(self, _):
        start new main game
    '''
    dictionaries = []
    round_duration = NumericProperty(60)
    selected_dictionary = StringProperty("")
    selected_dictionary_index = None

    def on_kv_post(self, _):
        '''
        Kivy method overridden to bind function to the screen button and
        load all available game dictionaries from the file
        '''
        self.ids.screen_bottom_button.ids.button.bind(
            on_press=self.start_main_game)
        with open("./constants/dicts.json", encoding="utf-8") as f:
            dicts = json.load(f)
            for key, value in dicts.items():
                self.dictionaries.append({
                    "title": key, "name": value["name"],
                    "desc": value["description"],
                    "volume": value["volume"]
                })
        self.fill_dictionaries()

    def change_round_duration(self, delta):
        '''
        Change round duration game option

        Parameters
        ----------
        delta : int
            changes that should be applied to round duration
        '''
        if self.round_duration + delta > 0 and self.round_duration + delta <= 180:
            self.round_duration = self.round_duration + delta

    def select_dictionary(self, carousel):
        '''
        Select game dictionary for new main game

        Parameters
        ----------
        carousel : Carousel
            instance of the kivy Carousel
        '''
        if self.dictionaries[carousel.index]["name"]:
            self.selected_dictionary = carousel.current_slide.ids.dict_name.text
            self.selected_dictionary_index = carousel.index
            self.hide_dictionaries()

    def show_dictionaries(self, _):
        '''
        Open carousel with dictionaries to choose
        '''
        dict_layout = self.ids.dictionaries_layout
        dict_label = self.ids.dictionaries_label

        dict_layout.y = dict_label.y - dict_label.height - 20

        anim = Animation(height=dp(100), d=.3)
        anim.bind(on_complete=lambda anim, wid: self.toggle_carousel_buttons())
        anim.start(dict_layout.parent)

    def fill_dictionaries(self):
        '''
        Fill kivy Carousel with items with dictionaries
        '''
        carousel = self.ids.dictionaries_layout.ids.carousel
        for _, dictionary in enumerate(self.dictionaries):
            carousel.add_widget(
                DictionaryCarouselItem(
                    title=dictionary["title"],
                    description=dictionary["desc"],
                    amount_of_words=dictionary["volume"],
                    on_press=lambda _: self.select_dictionary(carousel)
                )
            )

    def toggle_carousel_buttons(self):
        '''
        Toggle carousel button
        '''
        self.ids.dictionaries_open.disabled = not self.ids.dictionaries_open.disabled
        self.ids.carousel_right.disabled = not self.ids.carousel_right.disabled
        self.ids.carousel_left.disabled = not self.ids.carousel_left.disabled
        self.ids.dictionaries_open.opacity = int(
            not self.ids.dictionaries_open.opacity)
        self.ids.carousel_right.opacity = int(
            not self.ids.carousel_right.opacity)
        self.ids.carousel_left.opacity = int(
            not self.ids.carousel_left.opacity)

    def hide_dictionaries(self):
        '''
        Hide carousel with dictionaries to choose
        '''
        dict_layout = self.ids.dictionaries_layout
        anim = Animation(height=0, d=.3)
        anim.bind(on_complete=lambda anim, wid: self.toggle_carousel_buttons())
        anim.start(dict_layout.parent)

    def start_main_game(self, _):
        '''
        Start main game and call App creating main game method
        '''
        if self.selected_dictionary_index is not None:
            App.get_running_app().create_main_game(
                round_duration=self.round_duration,
                selected_dictionary=self.dictionaries[self.selected_dictionary_index]["name"],
                teams=self.manager.get_screen("team_config").team_list,
                penalty=self.ids.penalty_checkbox.active,
                last_word=self.ids.last_word_checkbox.active,
                points_to_win=int(self.ids.points_to_win_label.text)
            )
