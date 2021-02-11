'''
Round screen
'''

from kivy.uix.screenmanager import Screen
from kivy.properties import NumericProperty
from kivy.clock import Clock
from kivy.animation import Animation
from kivy.metrics import dp
from kivy.cache import Cache

from audioplayer import AudioPlayer

from screens.submit_round import SubmitRoundScreen
from screens.submit_last_word import SubmitLastWordScreen

from widgets.widgets import (
    GameCard
)


class RoundScreen(Screen):
    '''
    Screen with cards with words to guess

    Attributes
    ----------
    timer_event : ClockEvent
        event that is called each second to reduce round time left
    time_left : NumericPropery
        seconds to the end of round
    audio_player : AudioPlayer
        instance of `AudioPlayer` to play sound when the round is going to end
    words : list[tuple(str, bool)]
        list of words shown during the round and if it was guessed
    main_game : MainGameScreen
        instance of active `MainGameScreen`

    Methods
    -------
    on_kv_post(_):
        kivy method

    generate_card(first):
        create card with consecutive word in the main game dicitionary

    remove_current_card(card, guessed):
        remove card from the screen after it was swiped

    start_timer():
        start timer of the round

    _minus_second(_):
        take a second in the timer

    to_submit_screen():
        go to submit screen
    '''
    timer_event = None
    time_left = NumericProperty()
    audio_player = AudioPlayer()
    words = []

    def __init__(self, main_game, **kwargs):
        super().__init__(**kwargs)
        self.main_game = main_game
        self.time_left = main_game.round_duration
        self.words = []

    def on_kv_post(self, _):
        '''
        Kivy method overriden to generate first default card on the screen
        '''
        self.add_widget(Cache.get('images', 'round_background'), 20)
        self.generate_card(first=True)

    def generate_card(self, first=False):
        '''
        Generate card with consecutive word from the main game dictionary

        Parameters
        ----------
        first : bool, optional
            is generated card first or not, by default False
        '''
        if len(self.ids["game_layout"].children) < 2:
            if first:
                self.ids.game_layout.add_widget(
                    GameCard(
                        title="Почати",
                        is_first=True,
                        round_screen=self
                    )
                )
            else:
                if not self.timer_event:
                    self.start_timer()
                    self.remove_widget(self.ids.on_start_round)
                try:
                    next_word = self.main_game.dictionary[self.main_game.dict_idx]
                except IndexError:
                    self.main_game.dict_idx = 0
                    next_word = self.main_game.dictionary[self.main_game.dict_idx]

                self.ids["game_layout"].add_widget(
                    GameCard(title=next_word, round_screen=self))
                self.main_game.dict_idx += 1

    def remove_current_card(self, card, guessed):
        '''
        Remove current card from the screen after swipe

        Parameters
        ----------
        card : GameCard
            instance of the word card

        guessed : bool
            is word displayed on the card is guessed or not
        '''
        if card in self.ids["game_layout"].children:
            self.ids["game_layout"].remove_widget(card)
            self.words.append((card.title, guessed))

    def start_timer(self):
        '''
        Start timer of the round
        '''
        self.timer_event = Clock.schedule_interval(self._minus_second, 1)
        timer_anim = Animation(width=dp(0), d=self.main_game.round_duration)
        timer_anim.start(self.ids.timer_bar_top)
        timer_anim.start(self.ids.timer_bar_bottom)

    def _minus_second(self, _):
        '''
        Take a second from the timer
        '''
        self.time_left -= 1
        self.ids.timer.text = f"{self.time_left}"

        if self.time_left == 3:
            self.audio_player.play_sound('ticking')

        if self.time_left == 0:
            self.audio_player.play_sound('alarm')
            Clock.unschedule(self.timer_event)
            self.to_submit_screen()

    def to_submit_screen(self):
        '''
        Route to the round submit screen
        '''
        submit_screen = SubmitRoundScreen(
            words=self.words[1:]
        )
        self.manager.add_widget(submit_screen)
        if self.main_game.last_word:
            submit_last_word_screen = SubmitLastWordScreen(
                word=self.main_game.dictionary[self.main_game.dict_idx - 1]
            )
            self.manager.add_widget(submit_last_word_screen)
            self.manager.switch_to(submit_last_word_screen)
        else:
            self.manager.switch_to(submit_screen)
