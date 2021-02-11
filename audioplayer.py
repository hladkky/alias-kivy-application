'''
AudioPlayer module.

Module that includes class AudioPlayer to load and play sounds during the game.
'''


from kivy.core.audio import SoundLoader


class AudioPlayer():
    '''
    Audioplayer class to load and play sounds

    Methods
    -------
    play_sound(sound):
        play sound based on `sound` parameter
    '''

    def __init__(self):
        self.ticking = SoundLoader.load('./assets/sounds/ticking.wav')
        self.alarm = SoundLoader.load('./assets/sounds/alarm.wav')
        self.minus = SoundLoader.load('./assets/sounds/minus.wav')
        self.plus = SoundLoader.load('./assets/sounds/plus.wav')
        self.sound = None

    def play_sound(self, sound):
        '''
        Play sound based on `sound` choics

        Parameters
        ----------
        sound : str
            choice what sound to play
        '''
        if sound == 'plus':
            self.sound = self.plus
        elif sound == 'minus':
            self.sound = self.minus
        elif sound == 'alarm':
            self.sound = self.alarm
        elif sound == 'ticking':
            self.sound = self.ticking

        if self.sound:
            self.sound.volume = 0
            self.sound.play()
