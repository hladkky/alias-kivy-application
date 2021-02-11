'''
Round submit screen
'''

from kivy.properties import StringProperty, NumericProperty

from screens.background import BackgroundScreen
from screens.submit_last_word import SubmitLastWordScreen

from widgets.widgets import (
    WordLabel,
    WordLabelWithTeam
)


class SubmitRoundScreen(BackgroundScreen):
    '''
    Screen that appear after round is over to check all guessed words during the round.

    Attributes
    ----------
    word_label_with_team : WordLabelWithTeam
        label that consists of last work and team that guessed it.
        Visible only if `last_word` is True in `MainGameScreen`.
    main_team : StringProperty
        the team name that has played the round
    main_team_points : NumericProperty
        points of the team that has played the round
    second_team : StringProperty
        the team name that guessed last word and is not main_team.
        Is being used only if `last_word` is True in `MainGameScreen`.
    second_team_points : NumericProperty
        points of the team that guessed last word and is not main_team.
        Is being used only if `last_word` is True in `MainGameScreen`.
    first_enter : bool
        is it first enter of the screen
    guessed_team : str
        team that guessed last word.
        Is being used only if `last_word` is True in `MainGameScreen`.
    words : list[str]
        words that were during the round
    main_team_words : list[int]
        array, first value is amount of guessed words, second value - not guessed.
    last_word : str
        last_word of the round

    Methods
    -------
    on_kv_post(_):
        kivy method

    on_pre_enter():
        kivy method

    to_next_screen(_):
        route to the game configuration screen

    on_enter():
        kivy method

    to_submit_last_word_screen():
        go to the last word submit screen

    add_last_word_team(word, guessed_team):
        add label with the last word and the guessed team

    reward_last_word(guessed_team):
        reward team that guessed last word with 1 point

    update_points(_, value):
        add or remove point from main_team_point based on value

    calculate_point(is_penalty):
        calculate main_team_points

    end_turn():
        end current turn
    '''
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
        '''
        Kivy method overriden to bind the function to the screen button
        '''
        self.ids.screen_bottom_button.ids.button.bind(on_press=self.end_turn)

    def on_pre_enter(self):
        '''
        Kivy method overriden to get last word and main team of the round from the `MainGameScreen`
        '''
        main_game = self.manager.get_screen("main_game")
        self.last_word = main_game.dictionary[main_game.dict_idx - 1]
        self.main_team = main_game.get_current_team()

        if self.first_enter:
            self.first_enter = False
            self.calculate_points(is_penalty=main_game.penalty)

    def to_submit_last_word_screen(self):
        '''
        Route to last word submit screen
        '''
        if self.word_label_with_team:
            self.ids.words_to_submit.remove_widget(self.word_label_with_team)
        submit_last_word_screen = SubmitLastWordScreen(
            word=self.last_word
        )
        # if guessed team was the main team
        if self.guessed_team == self.main_team:
            self.main_team_points -= 1
        self.manager.add_widget(submit_last_word_screen)
        self.manager.current = "submit_last_word"

    def add_last_word_team(self, word, guessed_team):
        '''
        Add label with the last word and the guessed team on the screen

        Parameters
        ----------
        word : str
            last word

        guessed_team : str
            team who guessed last word
        '''
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
        '''
        Give a point to the team, who guessed last word

        Parameters
        ----------
        guessed_team : str
            team who guessed last word
        '''
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
        '''
        Update current score with 1 point

        Parameters
        ----------
        value : bool
            value that represent adding or removing one word from the list of guessed words
        '''
        self.main_team_points += 2 * (1 if value else -1)

    def calculate_points(self, is_penalty):
        '''
        Calculate point based on the word_list from round screen

        Parameters
        ----------
        is_penalty : bool
            use penalty for skipped word or not
        '''
        self.main_team_points = \
            self.main_team_words[1] - \
            self.main_team_words[0] * is_penalty

    def end_turn(self, _):
        '''
        End current turn
        '''
        main_game = self.manager.get_screen('main_game')
        self.manager.switch_to(main_game)
        main_game.end_current_round(self.main_team_points, self.second_team)
