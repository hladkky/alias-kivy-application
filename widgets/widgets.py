from kivy.uix.scatter import Scatter
from kivy.properties import StringProperty, NumericProperty, BooleanProperty
from kivy.animation import Animation

from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.button import MDIconButton, MDFlatButton
from kivymd.uix.behaviors import RectangularRippleBehavior

from audioplayer import AudioPlayer


class FontLabel(MDLabel):
    pass


class BoldFontLabel(MDLabel):
    pass


class TeamLabel(MDBoxLayout):
    text = StringProperty()
    height = NumericProperty()


class CloseIcon(MDIconButton):
    pass


class TextButton(MDFlatButton):
    pass


class OutlineButton(MDFlatButton, RectangularRippleBehavior):
    pass


class DropDownLayout(MDFloatLayout):
    pass


class DictionaryCarouselItem(OutlineButton):
    title = StringProperty()
    description = StringProperty()


class GameCard(Scatter):
    start_position = None
    title = StringProperty()
    audio_player = AudioPlayer()
    is_first = BooleanProperty(False)

    def on_touch_down(self, touch):
        super().on_touch_down(touch)
        self.start_position = self.pos

    def on_touch_up(self, touch):
        super().on_touch_up(touch)

        try:
            bias = (self.pos[1] - self.start_position[1]) / self.size[1]
            print(bias)
            if bias > .5:
                self.card_disappear_animation(True)
                if not self.is_first:
                    self.audio_player.play_sound('plus')
            elif bias < -.5:
                self.card_disappear_animation(False)
                if not self.is_first:
                    self.audio_player.play_sound('minus')
            else:
                Animation(
                    pos=self.start_position,
                    d=.1
                ).start(self)
        except (ZeroDivisionError, TypeError):
            pass

    def card_disappear_animation(self, to_top):
        destination_pos = (
            self.parent.width - self.width,
            self.parent.y + (self.parent.height if to_top else -self.height)
        )
        anim = Animation(
            pos=destination_pos,
            scale=.5,
            d=.1
        )
        anim.bind(
            on_complete=lambda anim, wid: self.remove_self(to_top)
        )
        anim.start(self)

    def remove_self(self, point):
        try:
            self.parent.parent.remove_current_card(self, point)
        except AttributeError:
            pass


class WordLabel(MDBoxLayout):
    word = StringProperty()
    checked = BooleanProperty()


class TeamLabelSubmitLastWord(MDBoxLayout):
    team = StringProperty()


class WordLabelWithTeam(MDBoxLayout):
    word = StringProperty()
    team = StringProperty()
