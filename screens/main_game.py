import json

from kivy.properties import NumericProperty
from kivy.metrics import dp

from screens.background import BackgroundScreen
from screens.round import RoundScreen
from screens.winner import WinnerScreen

from widgets.widgets import (
    TeamLabel
)


class MainGameScreen(BackgroundScreen):
    round_duration = NumericProperty(0)
    current_round = NumericProperty(1)
    current_turn = NumericProperty(0)

    def __init__(self, round_duration, teams, dictionary_name, dict_idx,
                 penalty, last_word, points_to_win, score, current_round,
                 current_turn, **kwargs):
        super().__init__(**kwargs)
        self.round_duration = round_duration
        self.teams = teams
        self.penalty = penalty
        self.last_word = last_word
        self.points_to_win = points_to_win
        self.dict_idx = dict_idx
        self.score = score
        self.current_turn = current_turn
        self.current_round = current_round

        with open("./constants/words.json", encoding="utf-8") as f:
            dicts = json.load(f)
            self.dictionary = dicts[dictionary_name]

        for i, team in enumerate(self.teams):
            label = TeamLabel(text=team, height=dp(60))
            label.ids.score_label.text = str(self.score[i])
            self.ids.teams.add_widget(label)

    def on_pre_enter(self):
        self.ids.current_turn.text = self.get_current_team()

    def on_kv_post(self, _):
        self.ids.screen_bottom_button.ids.button.bind(
            on_press=self.to_next_round)

    def update_score(self, team_label, delta):
        team_name = team_label.text
        team_index = self.teams.index(team_name)
        self.score[team_index] += delta
        team_label.ids.score_label.text = str(self.score[team_index])

    def get_current_team(self):
        return self.teams[self.current_turn]

    def to_next_round(self, _):
        self.manager.add_widget(RoundScreen())
        self.manager.current = "round"

    def end_current_round(self, cur_team_points, second_team):
        self.update_score(
            self.ids.teams.children[
                len(self.score) - 1 - self.current_turn
            ], cur_team_points
        )
        try:
            second_team_label_idx = self.teams.index(second_team)
            self.update_score(
                self.ids.teams.children[
                    len(self.score) - 1 - second_team_label_idx
                ], 1
            )
        except ValueError:
            pass
        self.change_turn()

    def change_turn(self):
        self.current_turn += 1
        self.ids.current_turn.text = self.get_current_team()

        if self.current_turn == len(self.teams):
            self.check_end_of_game()
            self.current_turn = 0
            self.current_round += 1

    def check_end_of_game(self):
        if self.points_to_win <= max(self.score):
            if sum(max(self.score) == team_score for team_score in self.score) == 1:
                self.to_winner_screen()

    def to_winner_screen(self):
        winner_screen = WinnerScreen(
            winner_team=self.teams[
                self.score.index(max(self.score))
            ]
        )
        self.manager.add_widget(winner_screen)
        self.manager.switch_to(winner_screen)
