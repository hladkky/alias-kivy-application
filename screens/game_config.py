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
    title = "Гра відбудеться у таких умовах:"
    button_text = "ГРАТИ"
    next_button = None
    dictionaries = []

    round_duration = NumericProperty(60)
    selected_dictionary = StringProperty("")
    selected_dictionary_index = 0

    def on_kv_post(self, _):
        self.ids.screen_bottom_button.ids.button.bind(
            on_press=self.start_main_game)

    def on_enter(self):
        with open("./constants/dicts.json", encoding="utf-8") as f:
            dicts = json.load(f)
            for key, value in dicts.items():
                self.dictionaries.append(
                    {"title": key, "name": value["name"], "desc": value["description"]})
            self.fill_dictionaries()

    def change_round_duration(self, delta):
        if self.round_duration + delta > 0 and self.round_duration + delta <= 180:
            self.round_duration = self.round_duration + delta

    def select_dictionary(self, carousel):
        if self.dictionaries[carousel.index]["name"]:
            self.selected_dictionary = carousel.current_slide.ids.dict_name.text
            self.selected_dictionary_index = carousel.index
            self.hide_dictionaries()

    def show_dictionaries(self, button):
        dict_layout = self.ids.dictionaries_layout
        dict_label = self.ids.dictionaries_label

        dict_layout.y = dict_label.y - dict_label.height - 20

        button.opacity = 0
        Animation(height=dp(100), d=.3).start(dict_layout.parent)
        Animation(opacity=1, d=.3).start(dict_layout.ids.drop_down_box)

    def fill_dictionaries(self):
        carousel = self.ids.dictionaries_layout.ids.carousel
        for _, dictionary in enumerate(self.dictionaries):
            carousel.add_widget(
                DictionaryCarouselItem(
                    title=dictionary["title"],
                    description=dictionary["desc"],
                    on_press=lambda _: self.select_dictionary(carousel)
                )
            )

    def hide_dictionaries(self):
        self.ids.dictionaries_button.opacity = 1
        dict_layout = self.ids.dictionaries_layout

        Animation(height=0, d=.3).start(dict_layout.parent)
        Animation(opacity=0, d=.3).start(dict_layout.ids.drop_down_box)

    def start_main_game(self, _):
        if self.selected_dictionary_index is not None:
            App.get_running_app().create_main_game(
                round_duration=self.round_duration,
                selected_dictionary=self.dictionaries[self.selected_dictionary_index]["name"],
                teams=self.manager.get_screen("team_config").team_list,
                penalty=self.ids.penalty_checkbox.active,
                last_word=self.ids.last_word_checkbox.active,
                points_to_win=int(self.ids.points_to_win_label.text)
            )
