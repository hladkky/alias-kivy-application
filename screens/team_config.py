import random

from kivy.metrics import dp
from kivy.animation import Animation

from screens.config import ConfigScreen

from widgets.widgets import (
    TeamLabel,
    CloseIcon,
)

from constants.team_namings import TEAM_NAMES


class TeamConfigScreen(ConfigScreen):
    title = "У запеклій грі зійдуться:"
    button_text = "До налаштувань"
    next_button = None

    team_list = []
    team_height = dp(60)

    def on_kv_post(self, _):
        self.ids.screen_bottom_button.ids.button.bind(
            on_press=self.to_next_screen)

    def to_next_screen(self, _):
        self.manager.current = "game_config"

    def on_enter(self):
        if not self.team_list:
            for _ in range(2):
                self.add_team()
        
        self.toggle_close_icons(show=False if len(self.team_list) == 2 else True)

        self.next_button = self.to_next_screen

    def add_team(self, with_animation=True):
        if len(self.team_list) > 4:
            return

        new_team_name = random.choice(
            [name for name in TEAM_NAMES if name not in self.team_list])
        self.team_list.append(new_team_name)
        new_team = TeamLabel(text=new_team_name, height=self.team_height)
        new_team.ids.close_icon_button_container.add_widget(
            CloseIcon(on_press=self.remove_team))

        if with_animation:
            new_team.opacity = 0
            new_team.height = 0

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
        team_to_delete = instance.parent.parent.parent

        try:
            self.team_list.remove(team_to_delete.text)
            team_to_delete.ids.close_icon_button_container.clear_widgets()
        except ValueError:
            pass

        animation = Animation(opacity=0,
                              height=0,
                              d=.3,
                              t="in_out_quad")

        animation.bind(on_complete=lambda anim,
                       wid: self.ids.team_list.remove_widget(wid))
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
