'''
Main game screen
'''

import json

from kivy.app import App
from kivy.properties import NumericProperty
from kivy.metrics import dp

from screens.background import BackgroundScreen
from screens.round import RoundScreen
from screens.winner import WinnerScreen

from widgets.widgets import (
    TeamLabel
)


class MainGameScreen(BackgroundScreen):
    '''
    Main screen of the active game

    Attributes
    ----------
    round_duration : NumericProperty
        duration of the round in seconds
    current_round : NumericProperty
        current round of the game
    current_turn : NumericProperty
        current turn of the round
    points_to_win : NumericProperty
        required amount of points to win the game
    teams : list[str]
        list of team names
    dictionary_name : str
        chosen dictionary for the game
    dict_idx : int
        current index of chosen dictionary
    penalty : bool
        whether to use a penalty for a skipped word or not
    last_word : str
        last word of the round
    score : list[int]
        score of the current game
    dictionary : list[str]
        dictionary of words for the current game

    Methods
    -------
    on_pre_enter():
        kivy method

    on_kv_post(_):
        kivy method

    load_configuration(round_duration, teams, dictionary_name, dict_idx, penalty,
                       last_word, points_to_win, score, current_round, current_turn):
        load all necessary parameters for the game

    update_score(team_label, delta):
        update amount of points for specified team

    get_current_team():
        return current turn team

    to_next_rount():
        go to round screen

    end_current_round():
        end current round of the game

    change_turn():
        change turn or round of the game

    check_end_of_game():
        check winning condition

    to_winner_screen():
        go to winner screen
    '''
    round_duration = NumericProperty(0)
    current_round = NumericProperty(1)
    current_turn = NumericProperty(0)
    points_to_win = NumericProperty(0)
    teams = []
    dictionary_name = ''
    dict_idx = 0
    penalty = False
    last_word = ''
    score = []
    dictionary = []

    def on_pre_enter(self):
        '''
        Kivy method overriden to set current team turn
        '''
        self.ids.current_turn.text = self.get_current_team()

    def on_kv_post(self, _):
        '''
        Kivy method overriden to bind function to the screen button
        '''
        self.ids.screen_bottom_button.ids.button.bind(
            on_press=self.to_next_round)

    def load_configuration(self, round_duration, teams, dictionary_name, dict_idx, penalty,
                           last_word, points_to_win, score, current_round, current_turn):
        '''
        Load main game parameters

        Parameters
        ----------
        round_duration : int
            duration of the round in seconds
        teams : list[str]
            list of team names
        dictionary_name : str
            chosen dictionary for the game
        dict_idx : int
            current index of chosen dictionary
        penalty : bool
            whether to use a penalty for a skipped word or not
        last_word : str
            last word of the round
        points_to_win : int
            required amount of points to win the game
        score : list[int]
            score of the current game
        current_round : int
            current round of the game
        current_turn : int
            current turn of the round
        '''
        self.round_duration = 4  # round_duration
        self.dictionary_name = dictionary_name
        self.teams = teams
        self.penalty = penalty
        self.last_word = last_word
        self.points_to_win = 2  # points_to_win
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

    def update_score(self, team_label, delta):
        '''
        Update score for one team with updates placed in delta

        Parameters
        ----------
        team_label : str
            team name for which updates are performing
        delta : int
            integer two update amount of points of specified team.
            Equals -1 or 1
        '''
        team_name = team_label.text
        team_index = self.teams.index(team_name)
        self.score[team_index] += delta
        team_label.ids.score_label.text = str(self.score[team_index])

    def get_current_team(self):
        '''
        Return current turn team name
        '''
        return self.teams[self.current_turn]

    def to_next_round(self, _):
        '''
        Route to the round screen
        '''
        self.manager.add_widget(RoundScreen(main_game=self))
        self.manager.current = "round"

    def end_current_round(self, cur_team_points, second_team):
        '''
        End current round and update game score

        Parameters
        ----------
        cur_team_points : int
            points earned by current turn team
        second_team : str or None
            team that guessed last word.
            If str, then add 1 point for the team.
            If None, then no teams guessed last word
        '''
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
        '''
        Change turn of the current turn or round.
        If round is over check the winning condition.
        '''
        self.current_turn += 1

        try:
            current_team_turn = self.get_current_team()
        except IndexError:
            self.current_turn = 0
            self.current_round += 1
            current_team_turn = self.get_current_team()
            self.check_end_of_game()

        self.ids.current_turn.text = current_team_turn

    def check_end_of_game(self):
        '''
        Check winning condition.
        And if so, go to the winner screen.
        '''
        if self.points_to_win <= max(self.score):
            if sum(max(self.score) == team_score for team_score in self.score) == 1:
                self.to_winner_screen()

    def to_winner_screen(self):
        '''
        Route to the winner screen.
        '''
        winner_screen = WinnerScreen(
            winner_team=self.teams[
                self.score.index(max(self.score))
            ]
        )

        # save dictionary index to the app store
        App.get_running_app().save_dict_idx(self.dictionary_name, self.dict_idx)

        # clear some configuration parameters
        self.teams.clear()
        self.score.clear()
        self.dictionary.clear()

        # and clear team labels
        self.ids.teams.clear_widgets()

        self.manager.add_widget(winner_screen)
        self.manager.current = winner_screen.name
