from kivy.properties import StringProperty

from screens.background import BackgroundScreen


class ConfigScreen(BackgroundScreen):
    title = StringProperty()
    button_text = StringProperty()
