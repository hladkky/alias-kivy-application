'''
Configuration screen.
'''

from kivy.properties import StringProperty

from screens.background import BackgroundScreen


class ConfigScreen(BackgroundScreen):
    '''
    Configuration screen.
    Used as template with title and screen button.

    Attributes
    ----------
    title: StringProperty
        title of the screen

    button_text: StringProperty
        text of the screen button
    '''
    title = StringProperty()
    button_text = StringProperty()
