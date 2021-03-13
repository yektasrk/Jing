from pygame import mixer

class Player:
    def __init__(self):
        mixer.init()
        self.root_path = "sounds"

    def play(self, soundfile):
        sound_file = mixer.Sound(self.root_path + "/" + soundfile)
        sound_file.play()



