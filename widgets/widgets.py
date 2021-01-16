from kivy.uix.scatter import Scatter
from kivy.properties import StringProperty, NumericProperty

from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.button import MDIconButton, MDFlatButton

from kivymd.uix.behaviors import (
    RectangularRippleBehavior,
    BackgroundColorBehavior,
    RectangularElevationBehavior,
    RectangularRippleBehavior
)
    

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
    title = StringProperty('Картка')

    def on_touch_down(self, touch):
        super().on_touch_down(touch)
        self.start_position = self.pos

    def on_touch_up(self, touch):
        super().on_touch_up(touch)

        try:
            if abs((self.pos[1] - self.start_position[1])/self.size[1]) > 1:
                self.parent.parent.remove_current_card(self)
        except ZeroDivisionError:
            pass

        self.pos = self.start_position
