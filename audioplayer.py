from kivy.core.audio import SoundLoader


class AudioPlayer():
    def __init__(self):
        self.ticking = SoundLoader.load('./assets/sounds/ticking.mp3')
        self.alarm = SoundLoader.load('./assets/sounds/alarm.mp3')
        self.minus = SoundLoader.load('./assets/sounds/minus.mp3')
        self.plus = SoundLoader.load('./assets/sounds/plus.mp3')
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

        self.sound.volume = 1
        self.sound.play()
