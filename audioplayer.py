from kivy.core.audio import SoundLoader


class AudioPlayer():
    def __init__(self):
        self.ticking = SoundLoader.load('./assets/sounds/ticking.wav')
        self.alarm = SoundLoader.load('./assets/sounds/alarm.wav')
        self.minus = SoundLoader.load('./assets/sounds/minus.wav')
        self.plus = SoundLoader.load('./assets/sounds/plus.wav')
        self.sound = None

    def play_sound(self, sound):
        if sound == 'plus':
            self.sound = self.plus
        elif sound == 'minus':
            self.sound = self.minus
        elif sound == 'alarm':
            self.sound = self.alarm
        elif sound == 'ticking':
            self.sound = self.ticking

        if self.sound:
            self.sound.volume = 1
            self.sound.play()
