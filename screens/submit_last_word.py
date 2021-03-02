'''
Last word submit screen.
'''

from kivy.properties import StringProperty

from screens.background import BackgroundScreen

from widgets.widgets import (
    TeamLabelSubmitLastWord
)


class SubmitLastWordScreen(BackgroundScreen):
    '''
    Screen for choosing the team who guessed last word of the round

    Attributes
    ----------
    word : StringProperty
        last word of the round
    
    guessed_team : str
        team that guessed last word
    
    main_game : MainGameScreen
        instance of the main game screen

    Methods
    -------
    on_kv_post(_):
        kivy method

    on_pre_enter():
        kivy method

    change_guessed_team(checkbox, value):
        change the team that guessed the word

    to_submit_screen(_):
        go to the submit screen
    '''
    word = StringProperty()
    guessed_team = None

    def __init__(self, word, **kwargs):
        super().__init__(**kwargs)
        self.word = word
        self.main_game = None

    def on_kv_post(self, _):
        '''
        Kivy method overriden to bind the function to the screen button
        '''
        self.ids.screen_bottom_button.ids.button.bind(
            on_press=self.to_submit_screen)

    def on_pre_enter(self):
        '''
        Kivy method overriden to get all teams from the `MainGameScreen`
        and place it on the screen with radio buttons
        '''
        self.main_game = self.manager.get_screen("main_game")

        for team in self.main_game.teams:
            team_label = TeamLabelSubmitLastWord(team=team)
            team_label.ids.check_word.bind(
                active=self.change_guessed_team
            )
            self.ids.team_list.add_widget(team_label)

    def change_guessed_team(self, checkbox, value):
        '''
        Change the team who guessed the word

        Parameters
        ----------
        checkbox: MDCheckbox
            checkbox that has been pressed
        value : bool
            value of the checkbox
        '''
        self.guessed_team = checkbox.parent.parent.team if value else None
        self.ids.screen_bottom_button.button_text = "Далі" if self.guessed_team else "Ніхто"

    def to_submit_screen(self, _):
        '''
        Route to the submit screen
        '''
        submit_round_screen = self.manager.get_screen("submit_round")
        self.manager.switch_to(submit_round_screen)
        submit_round_screen.add_last_word_team(
            word=self.word,
            guessed_team=self.guessed_team
        )
