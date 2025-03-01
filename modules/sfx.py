from ursina import *

class Sound():
    def __init__(self):
        self.key = Audio("sound/key.mp3",loop=False,autoplay=False)
        self.door = Audio("sound/door.mp3",loop=False,autoplay=False)
        self.jumpscare = Audio("sound/jumpscare.mp3",loop=False,autoplay=False)

    def play_key(self):
        self.key.play()

    def play_door(self):
        self.door.play()

    def play_jumpscare(self):
        self.jumpscare.play()