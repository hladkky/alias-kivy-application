from kivy.uix.screenmanager import Screen
from kivy.properties import NumericProperty
from kivy.clock import Clock
from kivy.animation import Animation
from kivy.metrics import dp

from audioplayer import AudioPlayer

from screens.submit_round import SubmitRoundScreen
from screens.submit_last_word import SubmitLastWordScreen

from widgets.widgets import (
    GameCard
)


class RoundScreen(Screen):
    timer_event = None
    time_left = NumericProperty()
    audio_player = AudioPlayer()
    words = []
    main_game = None

    def on_kv_post(self, _):
        self.generate_card(first=True)

    def on_pre_enter(self):
        self.main_game = self.manager.get_screen("main_game")
        self.time_left = 4  # self.main_game.round_duration
        self.words = []

    def generate_card(self, first=False):
        if first:
            self.ids.game_layout.add_widget(GameCard(title="Почати", is_first=True))
        else:
            if not self.timer_event:
                self.start_timer()
                self.remove_on_start_image()
            try:
                next_word = self.main_game.dictionary[self.main_game.dict_idx]
            except IndexError:
                self.main_game.dict_idx = 0
                next_word = self.main_game.dictionary[self.main_game.dict_idx]

            self.ids["game_layout"].add_widget(GameCard(title=next_word))
            self.main_game.dict_idx += 1

    def remove_on_start_image(self):
        self.remove_widget(self.ids.on_start_round)

    def remove_current_card(self, instance, guessed):
        self.ids["game_layout"].remove_widget(instance)
        self.words.append((instance.title, guessed))
        self.generate_card()

    def start_timer(self):
        self.timer_event = Clock.schedule_interval(self._minus_second, 1)
        timer_anim = Animation(width=dp(0), d=self.main_game.round_duration)
        timer_anim.start(self.ids.timer_bar_top)
        timer_anim.start(self.ids.timer_bar_bottom)

    def _minus_second(self, _):
        self.time_left -= 1
        self.ids.timer.text = f"{self.time_left}"

        if self.time_left == 3:
            self.audio_player.play_sound('ticking')

        if self.time_left == 0:
            self.audio_player.play_sound('alarm')
            Clock.unschedule(self.timer_event)
            self.to_submit_screen()

    def to_submit_screen(self):
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
