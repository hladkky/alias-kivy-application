'''
All custom widgets used in application
'''

from kivy.uix.scatter import Scatter
from kivy.properties import StringProperty, NumericProperty, BooleanProperty
from kivy.animation import Animation
from kivy.clock import Clock

from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.button import MDIconButton, MDFlatButton
from kivymd.uix.behaviors import RectangularRippleBehavior
from kivymd.uix.dialog import MDDialog

from audioplayer import AudioPlayer


class FontLabel(MDLabel):
    '''
    Custom primary label
    '''


class BoldFontLabel(MDLabel):
    '''
    Custom label with bold font
    '''


class ScreenTitle(MDFloatLayout):
    '''
    Title of the screen
    '''


class ScreenBottomButton(MDFloatLayout):
    '''
    Button at the bottom of the screen
    '''


class TeamLabel(MDBoxLayout):
    '''
    Label of one team on the `TeamConfigScreen`

    Attributes
    ----------
    text : StringProperty
        team naming
    height : NumericProperty
        height of the label
    '''
    text = StringProperty()
    height = NumericProperty()


class CloseIcon(MDIconButton):
    '''
    Custom close icon
    '''


class TextButton(MDFlatButton):
    '''
    Custom text button
    '''


class OutlineButton(MDFlatButton, RectangularRippleBehavior):
    '''
    Custom outline button with transparent background and border
    '''


class Dialog(MDDialog):
    '''
    Custom dialog window
    '''


class DropDownLayout(MDFloatLayout):
    '''
    Custom drop down layout with animation of height
    '''


class DictionaryCarouselItem(OutlineButton):
    '''
    Custom carousel item

    Attributes
    ----------
    title : StringProperty
        dictionary name
    description : StringProperty
        dictionary description
    amount_of_words : StringProperty
        dictionary volume
    '''
    title = StringProperty()
    description = StringProperty()
    amount_of_words = StringProperty()


class GameCard(Scatter):
    '''
    Swipeable game card with word to guess

    Attributes
    ----------
    start_position : tuple(float)
        default position of the card at the center of the screen
    title : StringProperty
        word on the card to guess
    audio_player : AudioPlayer
        instance of `AudioPlayer` to play sound when swipe
    is_first : bool
        is card first(default) or not
    round_screen : RoundScreen
        instance of active `RoundScreen` class

    Methods
    -------
    on_touch_up(touch):
        kivy method

    card_disappear_animation(to_top):
        dissapear card animation

    remove_self(point):
        remove card after dissapear animation
    '''
    start_position = None
    title = StringProperty()
    audio_player = AudioPlayer()
    is_first = BooleanProperty(False)

    def __init__(self, round_screen, **kwargs):
        super().__init__(**kwargs)
        self.round_screen = round_screen

    def on_kv_post(self, _):
        '''
        Kivy method overriden to assign start position
        '''
        def assign_start_position(pos):
            self.start_position = pos
        Clock.schedule_once(lambda _: assign_start_position(self.pos))

    def on_touch_up(self, touch):
        '''
        Kivy method overriden to handle swipe
        '''
        super().on_touch_up(touch)
        try:
            # relative bias
            bias = (self.pos[1] - self.start_position[1]) / self.size[1]

            # swipe a card a half size up
            if bias > .5:
                self.card_disappear_animation(True)
                if not self.is_first:
                    self.audio_player.play_sound('plus')
            # swipe down
            elif bias < -.5:
                self.card_disappear_animation(False)
                if not self.is_first:
                    self.audio_player.play_sound('minus')
            # otherwise return start position
            else:
                Animation(
                    pos=self.start_position,
                    d=0.1
                ).start(self)
        except (ZeroDivisionError, TypeError):
            pass

    def card_disappear_animation(self, to_top):
        '''
        Animate card dissapear when swipe

        Parameters
        ----------
        to_top : bool
            is swipe to top or not
        '''
        # to top or bottom of layout
        destination_pos = (
            self.parent.width / 2,
            self.parent.y + (self.parent.height if to_top else -self.height)
        )
        anim = Animation(
            pos=destination_pos,
            scale=.5,
            d=.1
        )
        anim.bind(
            on_start=lambda anim, wid: self.round_screen.generate_card()
        )
        anim.bind(
            on_complete=lambda anim, wid: self.remove_self(to_top)
        )
        anim.start(self)

    def remove_self(self, point):
        '''
        Remove self from the screen

        Parameters
        ----------
        point : int
            point for guessing word
        '''
        try:
            self.round_screen.remove_current_card(self, point)
        except AttributeError:
            pass


class WordLabel(MDBoxLayout):
    '''
    Custom word label used on the `SubmitRoundScreen`

    Attributes
    ----------
    word : StringProperty
        word shown in the round
    checked : BooleanProperty
        is word guessed or not
    '''
    word = StringProperty()
    checked = BooleanProperty()


class TeamLabelSubmitLastWord(MDBoxLayout):
    '''
    Custom team label used on the `SubmitLastWordScreen`

    Attributes
    ----------
    team : StringProperty
        team naming
    '''
    team = StringProperty()


class WordLabelWithTeam(MDBoxLayout):
    '''
    Custom label with last word and guessed team used on the `SubmitRoundScreen`

    Attributes
    ----------
    word : StringProperty
        last word of the round
    team : StringProperty
        team naming
    '''
    word = StringProperty()
    team = StringProperty()
