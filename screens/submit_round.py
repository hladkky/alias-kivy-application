from kivy.properties import StringProperty, NumericProperty

from screens.background import BackgroundScreen
from screens.submit_last_word import SubmitLastWordScreen

from widgets.widgets import (
    WordLabel,
    WordLabelWithTeam
)


class SubmitRoundScreen(BackgroundScreen):
    word_label_with_team = None
    main_team = StringProperty()
    main_team_points = NumericProperty()
    second_team = StringProperty()
    second_team_points = NumericProperty()
    first_enter = True
    guessed_team = None

    def __init__(self, words, **kwargs):
        super().__init__(**kwargs)
        self.words = words
        self.main_team_words = [0, 0]
        self.last_word = None
        for word, checked in self.words:
            word_label = WordLabel(word=word, checked=checked)
            word_label.ids.check_word.bind(active=self.update_points)
            self.ids.words_to_submit.add_widget(word_label)
            self.main_team_words[int(checked)] += 1

    def on_kv_post(self, _):
        self.ids.screen_bottom_button.ids.button.bind(on_press=self.end_turn)

    def on_pre_enter(self):
        main_game = self.manager.get_screen("main_game")
        self.last_word = main_game.dictionary[main_game.dict_idx - 1]
        self.main_team = main_game.get_current_team()

        if self.first_enter:
            self.first_enter = False
            self.calculate_points(is_penalty=main_game.penalty)

    def to_submit_last_word_screen(self):
        if self.word_label_with_team:
            self.ids.words_to_submit.remove_widget(self.word_label_with_team)
        submit_last_word_screen = SubmitLastWordScreen(
            word=self.last_word
        )
        if self.guessed_team == self.main_team:
            self.main_team_points -= 1
        self.manager.add_widget(submit_last_word_screen)
        self.manager.current = "submit_last_word"

    def add_last_word_team(self, word, guessed_team):
        self.guessed_team = guessed_team
        self.word_label_with_team = WordLabelWithTeam(
            word=word,
            team=guessed_team if guessed_team else "Ніхто"
        )
        self.word_label_with_team.ids.change_guessed_team.bind(
            on_press=lambda button: self.to_submit_last_word_screen()
        )

        self.ids.words_to_submit.add_widget(self.word_label_with_team)
        self.reward_last_word(guessed_team)

    def reward_last_word(self, guessed_team):
        main_game = self.manager.get_screen("main_game")
        self.main_team = main_game.get_current_team()
        if guessed_team and guessed_team != self.main_team:
            self.second_team = guessed_team
            self.second_team_points = 1
        else:
            self.second_team = ''
            self.second_team_points = 0
            if guessed_team == self.main_team:
                self.main_team_points += 1

    def update_points(self, _, value):
        self.main_team_points += 2 * (1 if value else -1)

    def calculate_points(self, is_penalty):
        self.main_team_points = \
            self.main_team_words[1] - \
            self.main_team_words[0] * is_penalty

    def end_turn(self, _):
        main_game = self.manager.get_screen('main_game')
        self.manager.switch_to(main_game)
        main_game.end_current_round(self.main_team_points, self.second_team)
        
    # def on_leave(self):
    #     self.manager.remove_widget(self)
        # try:
            
        # except AttributeError:
        #     pass
