import random
import json

from kivy.uix.screenmanager import Screen
from kivy.animation import Animation
from kivy.properties import StringProperty, NumericProperty
from kivy.uix.carousel import Carousel
from kivy.clock import Clock
from kivy.metrics import dp
from widgets.widgets import TeamLabel, CloseIcon, GameCard, DictionaryCarouselItem

from constants.team_namings import TEAM_NAMES

class MenuScreen(Screen):
    pass


class ConfigScreen(Screen):
    title = StringProperty()
    button_text = StringProperty()
    to_screen = StringProperty()


class TeamConfigScreen(ConfigScreen):
    title = "У запеклій грі зійдуться:"
    button_text = "До налаштувань"
    to_screen = "game_config"
    
    team_list = []
    team_height = dp(60)
    
    def on_kv_post(self, instance):
        for i in range(2):
            self.add_team(with_animation=False)
        self.toggle_close_icons()
        
        
    def add_team(self, with_animation=True):
        if len(self.team_list) > 4:
            return
    
        new_team_name = random.choice([name for name in TEAM_NAMES if name not in self.team_list])
        self.team_list.append(new_team_name)
        new_team = TeamLabel(text=new_team_name, height=self.team_height)
        new_team.ids.close_icon_button_container.add_widget(CloseIcon(on_press=self.remove_team))
        
        if with_animation:
            new_team.opacity = 0
            new_team.height = 0
            
            print(new_team.size)

            self.ids.team_list.add_widget(new_team)
            animation = Animation(opacity=1,
                                  height=self.team_height,
                                  d=.3,
                                  t="in_out_quad")
            animation.start(new_team)
        else:
            self.ids.team_list.add_widget(new_team)
        
        if len(self.team_list) == 3:
            self.toggle_close_icons(True)
        elif len(self.team_list) == 5:
            self.toggle_add_team_button(show=False)
    
    def remove_team(self, instance):
        team_to_delete = instance.parent.parent
        
        try:
            self.team_list.remove(instance.parent.parent.text)
            team_to_delete.ids.close_icon_button_container.clear_widgets()
        except ValueError:
            pass
        
        animation = Animation(opacity=0,
                              height=0,
                              d=.3,
                              t="in_out_quad")
        
        animation.bind(on_complete=lambda anim, wid: self.ids.team_list.remove_widget(wid))
        animation.start(team_to_delete)
        
        if len(self.team_list) == 2:
            self.toggle_close_icons()
        elif len(self.team_list) == 4:
            self.toggle_add_team_button(show=True)
    
    
    def toggle_add_team_button(self, show=False):
        if show:
            animation = Animation(opacity=1,
                                  height=self.team_height,
                                  d=.3,
                                  t="in_out_quad")
            animation.start(self.ids.add_button_container)
        else:
            animation = Animation(opacity=0,
                                  height=0,
                                  d=.3,
                                  t="in_out_quad")
            animation.start(self.ids.add_button_container)
        
    
    
    def toggle_close_icons(self, show=False):
        for child in self.ids.team_list.children:
            if show and not child.ids.close_icon_button_container.children:
                child.ids.close_icon_button_container.add_widget(CloseIcon(
                    on_press=self.remove_team
                ))
            elif not show:
                child.ids.close_icon_button_container.clear_widgets()
        

class GameConfigScreen(ConfigScreen):
    title = "Гра відбудеться у таких умовах:"
    button_text = "ГРАТИ"
    to_screen = "game_config"
    dictionaries = []
    
    round_duration = NumericProperty(60)
    selected_dictionary = StringProperty("")    
    selected_dictionary_index = NumericProperty(0)


    def on_enter(self):
        with open("./constants/dicts.json", encoding="utf-8") as f:
            dicts = json.load(f)
            
            for key, value in dicts.items():
                self.dictionaries.append({"title": key, "desc": value["description"]})
            self.fill_dictionaries()


    def change_round_duration(self, delta):
        if self.round_duration + delta > 0 and self.round_duration + delta <= 180:
            self.round_duration = self.round_duration + delta


    def select_dictionary(self, carousel):
        if carousel.index == len(self.dictionaries) - 1:
            return
        self.selected_dictionary_index = carousel.index
        self.selected_dictionary = carousel.current_slide.ids.dict_name.text
        self.hide_dictionaries()


    def show_dictionaries(self, button):
        dict_layout = self.ids.dictionaries_layout
        dict_label = self.ids.dictionaries_label
        carousel = dict_layout.ids.carousel
        
        dict_layout.y = dict_label.y - dict_label.height - 20
        
        button.opacity = 0
        Animation(height=100, d=.3).start(dict_layout.parent)
        Animation(opacity=1, d=.3).start(dict_layout.ids.drop_down_box)
    
    
    def fill_dictionaries(self):
        carousel = self.ids.dictionaries_layout.ids.carousel
        for idx, dictionary in enumerate(self.dictionaries):
            carousel.add_widget(DictionaryCarouselItem(
                    title=dictionary["title"],
                    description=dictionary["desc"],
                    on_press=lambda _: self.select_dictionary(carousel)
                )
            )
    
    
    def change_dict(self, to_right=True):
        pass
    
    
    def hide_dictionaries(self):
        self.ids.dictionaries_button.opacity = 1
        dict_layout = self.ids.dictionaries_layout
        
        Animation(height=0, d=.3).start(dict_layout.parent)
        Animation(opacity=0, d=.3).start(dict_layout.ids.drop_down_box)
        


class RoundScreen(Screen):
    round_time = 5
    time_left = round_time
    timer_event = None
    
    def on_kv_post(self, instance):
        self.generate_card(first=True)
        # pass

    def generate_card(self, first=False):
        if first:
            self.ids["game_layout"].add_widget(GameCard(title="Почати"))
        else:
            self.start_timer()
            self.ids["game_layout"].add_widget(GameCard(title="Карта"))
        
    def remove_current_card(self, instance):
        self.ids["game_layout"].remove_widget(instance)
        self.generate_card()
        
    def start_timer(self):
        self.timer_event = Clock.schedule_interval(self._minus_second, 1)
        
    def _minus_second(self, dt):
        self.time_left = str(int(self.time_left) - 1)
        self.ids.timer.text = f"{self.time_left}"
        
        if self.time_left == "0":
            Clock.unschedule(self.timer_event)
            self.parent.current = "menu"
